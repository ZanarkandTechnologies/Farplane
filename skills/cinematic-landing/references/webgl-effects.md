# WebGL Effects: Shaders, R3F, and PostProcessing

> **When to use**: Adding distinctive visual effects like ASCII rendering, glitch effects, or custom shaders to your landing page.

## Architecture Overview

```
┌─────────────────────────────────────┐
│           React Component           │
│  ┌───────────────────────────────┐  │
│  │      R3F Canvas               │  │
│  │  ┌─────────────────────────┐  │  │
│  │  │   Scene (meshes, etc.)  │  │  │
│  │  └─────────────────────────┘  │  │
│  │  ┌─────────────────────────┐  │  │
│  │  │   EffectComposer        │  │  │
│  │  │   └─ Custom Effects     │  │  │
│  │  └─────────────────────────┘  │  │
│  └───────────────────────────────┘  │
└─────────────────────────────────────┘
```

---

## Basic R3F Scene Setup

```tsx
"use client"

import { Canvas } from "@react-three/fiber"
import { EffectComposer } from "@react-three/postprocessing"
import { Suspense } from "react"

export function WebGLScene() {
  return (
    <div style={{ width: "100%", height: "100vh" }}>
      <Canvas
        camera={{ position: [0, 0, 5], fov: 50 }}
        style={{ background: "transparent" }}
        gl={{
          alpha: true,           // Transparent background
          antialias: false,      // Disable for performance
          stencil: false,
          depth: false,
          powerPreference: "high-performance"
        }}
        dpr={1}                  // Fixed DPR for consistency
        frameloop="always"
      >
        <Suspense fallback={null}>
          <SceneContent />
        </Suspense>

        <EffectComposer multisampling={0}>
          {/* Custom effects go here */}
        </EffectComposer>
      </Canvas>
    </div>
  )
}
```

---

## Video Texture in R3F

Use `useVideoTexture` from Drei for video backgrounds:

```tsx
import { useVideoTexture } from "@react-three/drei"

function VideoPlane() {
  const texture = useVideoTexture("/assets/video.mp4", {
    muted: true,
    loop: true,
    start: true,
    playsInline: true,
  })
  
  return (
    <mesh scale={[1, 1, 1]}>
      {/* 16:9 aspect ratio */}
      <planeGeometry args={[16, 9]} />
      <meshBasicMaterial map={texture} toneMapped={false} transparent />
    </mesh>
  )
}
```

---

## Custom PostProcessing Effect Template

Create reusable shader effects by extending PostProcessing's `Effect` class:

```tsx
"use client"

import { forwardRef, useMemo } from "react"
import { Effect, BlendFunction } from "postprocessing"
import { Uniform, Vector2 } from "three"

// Fragment shader (GLSL)
const fragmentShader = `
uniform float time;
uniform vec2 resolution;
uniform float intensity;

void mainImage(const in vec4 inputColor, const in vec2 uv, out vec4 outputColor) {
  // Sample the input texture
  vec4 color = texture(inputBuffer, uv);
  
  // Apply your effect
  // Example: simple color shift
  color.rgb = mix(color.rgb, vec3(1.0, 0.5, 0.0), intensity * 0.1);
  
  outputColor = color;
}
`

// Module-level state for uniforms
let _time = 0

class CustomEffectImpl extends Effect {
  constructor(options: { intensity?: number; resolution?: Vector2 }) {
    const { intensity = 1.0, resolution = new Vector2(1920, 1080) } = options

    super("CustomEffect", fragmentShader, {
      blendFunction: BlendFunction.NORMAL,
      uniforms: new Map([
        ["time", new Uniform(0)],
        ["resolution", new Uniform(resolution)],
        ["intensity", new Uniform(intensity)],
      ]),
    })
  }

  update(_renderer: any, _inputBuffer: any, deltaTime: number) {
    _time += deltaTime
    this.uniforms.get("time")!.value = _time
  }
}

// React wrapper component
export interface CustomEffectProps {
  intensity?: number
  resolution?: Vector2
}

export const CustomEffect = forwardRef<any, CustomEffectProps>((props, ref) => {
  const { intensity = 1.0, resolution = new Vector2(1920, 1080) } = props

  const effect = useMemo(
    () => new CustomEffectImpl({ intensity, resolution }),
    [intensity, resolution]
  )

  return <primitive ref={ref} object={effect} dispose={null} />
})

CustomEffect.displayName = "CustomEffect"
```

---

## ASCII Effect (Production Example)

A complete ASCII rendering effect with multiple styles:

```tsx
const fragmentShader = `
uniform float cellSize;
uniform bool colorMode;
uniform int asciiStyle;

// ASCII character rendering based on brightness
float getChar(float brightness, vec2 p, int style) {
  vec2 grid = floor(p * 4.0);
  float val = 0.0;
  
  if (style == 0) { // Standard - Technical symbols
    if (brightness < 0.2) val = (grid.x == 1.0 && grid.y == 1.0) ? 1.0 : 0.0;
    else if (brightness < 0.4) val = (grid.x == grid.y || grid.x + grid.y == 3.0) ? 1.0 : 0.0;
    else if (brightness < 0.6) val = (grid.x == 1.0 || grid.x == 2.0 || grid.y == 1.0 || grid.y == 2.0) ? 1.0 : 0.0;
    else val = 1.0;
  } 
  else if (style == 2) { // Minimal - clean X characters
    if (brightness < 0.05) return 0.0;
    bool onDiag1 = (grid.x == grid.y);
    bool onDiag2 = (grid.x + grid.y == 3.0);
    return (onDiag1 || onDiag2) ? 1.0 : 0.0;
  }
  else if (style == 3) { // Blocks/Dots - Round circles
    if (brightness < 0.1) return 0.0;
    float dist = length(p - 0.5);
    float radius = brightness * 0.45;
    return smoothstep(radius, radius - 0.05, dist);
  }
  return val;
}

void mainImage(const in vec4 inputColor, const in vec2 uv, out vec4 outputColor) {
  // Calculate cell coordinates
  vec2 cellCount = resolution / cellSize;
  vec2 cellCoord = floor(uv * cellCount);
  vec2 cellUV = (cellCoord + 0.5) / cellCount;
  
  // Sample center of cell
  vec4 cellColor = texture(inputBuffer, cellUV);
  float brightness = dot(cellColor.rgb, vec3(0.299, 0.587, 0.114));
  
  // Get local UV within cell
  vec2 localUV = fract(uv * cellCount);
  float charValue = getChar(brightness, localUV, asciiStyle);
  
  // Output
  vec3 finalColor = colorMode ? cellColor.rgb * charValue : vec3(brightness * charValue);
  outputColor = vec4(finalColor, cellColor.a);
}
`
```

### PostFX Uniform Options

```typescript
interface PostFXOptions {
  // CRT Effects
  scanlineIntensity: number    // 0-1, adds horizontal lines
  scanlineCount: number        // Number of scanlines
  curvature: number            // Screen curve distortion
  
  // Animation
  targetFPS: number            // 0 = smooth, >0 = stepped animation
  jitterIntensity: number      // Random position jitter
  jitterSpeed: number          // Jitter animation speed
  
  // Interactive
  mouseGlowEnabled: boolean    // Glow follows cursor
  mouseGlowRadius: number      // Glow size in pixels
  mouseGlowIntensity: number   // Glow brightness
  
  // Post-processing
  vignetteIntensity: number    // Dark corners
  vignetteRadius: number       // Vignette spread
  aberrationStrength: number   // Chromatic aberration
  
  // Noise & Glitch
  noiseIntensity: number       // Film grain
  noiseScale: number           // Grain size
  glitchIntensity: number      // Random glitch strips
  glitchFrequency: number      // How often glitches occur
  
  // Color
  colorPalette: number         // 0=original, 1=green, 2=amber, 3=cyan
  brightnessAdjust: number     // -1 to 1
  contrastAdjust: number       // 0 to 2
}
```

---

## Image Texture in R3F

For static images instead of video:

```tsx
import { useTexture } from "@react-three/drei"
import { useThree } from "@react-three/fiber"

function ImagePlane({ src }: { src: string }) {
  const texture = useTexture(src)
  const { viewport } = useThree()

  return (
    <mesh scale={[viewport.width, viewport.height, 1]}>
      <planeGeometry args={[1, 1]} />
      <meshBasicMaterial map={texture} transparent alphaTest={0.1} />
    </mesh>
  )
}
```

---

## Mouse Tracking for Effects

```tsx
import { useState, useEffect, useRef } from "react"
import { Vector2 } from "three"

export function InteractiveScene() {
  const containerRef = useRef<HTMLDivElement>(null)
  const [mousePos, setMousePos] = useState(new Vector2(0, 0))
  const [resolution, setResolution] = useState(new Vector2(1920, 1080))

  useEffect(() => {
    const handleMouseMove = (e: MouseEvent) => {
      if (containerRef.current) {
        const rect = containerRef.current.getBoundingClientRect()
        const x = e.clientX - rect.left
        // Flip Y for shader UV space (bottom-up)
        const y = rect.height - (e.clientY - rect.top)
        setMousePos(new Vector2(x, y))
      }
    }

    const handleResize = () => {
      if (containerRef.current) {
        const rect = containerRef.current.getBoundingClientRect()
        setResolution(new Vector2(rect.width, rect.height))
      }
    }

    const container = containerRef.current
    if (container) {
      container.addEventListener("mousemove", handleMouseMove)
      window.addEventListener("resize", handleResize)
      handleResize() // Initial
    }

    return () => {
      container?.removeEventListener("mousemove", handleMouseMove)
      window.removeEventListener("resize", handleResize)
    }
  }, [])

  return (
    <div ref={containerRef} style={{ width: "100%", height: "100vh" }}>
      <Canvas>
        <EffectComposer>
          <CustomEffect resolution={resolution} mousePos={mousePos} />
        </EffectComposer>
      </Canvas>
    </div>
  )
}
```

---

## Reusable WebGL Component Pattern

Create configurable components with sensible defaults:

```tsx
interface AsciiBridgeProps {
  src: string
  cellSize?: number
  targetFPS?: number
  resolutionScale?: number
  style?: "standard" | "dense" | "minimal" | "blocks"
}

export function AsciiBridge({
  src,
  cellSize = 8,
  targetFPS = 15,
  resolutionScale = 0.5,
  style = "minimal"
}: AsciiBridgeProps) {
  const containerRef = useRef<HTMLDivElement>(null)
  const [resolution, setResolution] = useState(new Vector2(1920, 1080))

  useEffect(() => {
    const updateSize = () => {
      if (containerRef.current) {
        const rect = containerRef.current.getBoundingClientRect()
        if (rect.width > 0 && rect.height > 0) {
          setResolution(new Vector2(
            Math.floor(rect.width * resolutionScale),
            Math.floor(rect.height * resolutionScale)
          ))
        }
      }
    }

    updateSize()
    window.addEventListener("resize", updateSize)
    const timer = setTimeout(updateSize, 100) // Delayed for layout

    return () => {
      window.removeEventListener("resize", updateSize)
      clearTimeout(timer)
    }
  }, [resolutionScale])

  return (
    <div ref={containerRef} className="w-full h-full">
      <Canvas
        camera={{ position: [0, 0, 5], fov: 50 }}
        gl={{ alpha: true, antialias: false, powerPreference: "high-performance" }}
        dpr={1}
      >
        <Suspense fallback={null}>
          <ImagePlane src={src} />
        </Suspense>

        <EffectComposer multisampling={0}>
          <AsciiEffect
            style={style}
            cellSize={cellSize}
            color={true}
            resolution={resolution}
            postfx={{ targetFPS, noiseIntensity: 0.03 }}
          />
        </EffectComposer>
      </Canvas>
    </div>
  )
}
```

---

## Performance Tips

1. **Resolution Scaling**: Use `resolutionScale < 1` for effects (0.5 = half resolution)
2. **DPR**: Set `dpr={1}` to prevent high-DPI scaling issues
3. **Multisampling**: Use `multisampling={0}` in EffectComposer
4. **Frameloop**: Use `frameloop="demand"` if not animating constantly
5. **Dispose**: Always include `dispose={null}` on primitive effects
6. **Lazy Loading**: Wrap scenes in `<Suspense>` with null fallback

---

## Gotchas

1. **"use client"**: All R3F components must be client-side
2. **SSR**: Canvas will error during SSR—wrap in dynamic import if needed
3. **Uniform Updates**: Use module-level variables, not React state, for frequent updates
4. **Shader Compilation**: First render may stutter—preload shaders if critical
5. **Mobile**: WebGL effects can drain battery—consider disabling on mobile

