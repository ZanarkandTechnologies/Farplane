# Three.js Workflows

## 1. Simple Rotating Cube (R3F)
```javascript
import { Canvas, useFrame } from '@react-three/fiber';

function Box() {
  const meshRef = useRef();
  useFrame((state, delta) => (meshRef.current.rotation.x += delta));
  return (
    <mesh ref={meshRef}>
      <boxGeometry />
      <meshStandardMaterial color="orange" />
    </mesh>
  );
}
```

## 2. Loading GLTF Models
Use the `useGLTF` hook from Drei for efficient model loading.
```javascript
const { scene } = useGLTF('/model.gltf');
return <primitive object={scene} />;
```

