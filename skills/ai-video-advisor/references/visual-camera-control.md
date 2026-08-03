---
template_id: skill-method-reference
template_version: "0.1.0"
feature_refs:
  - FEAT-0057
consumer_scope: skill-reference
applies_to:
  - skills/ai-video-advisor/references/visual-camera-control.md
template_uses:
  skill-method-reference: "0.1.0"
method: ai-video-advisor:visual-camera-control
---

# Visual Camera Control

Use this reference when a model-native video request includes arrows, a map,
an annotated asset, a camera path, a landmark orbit, or multiple required
perspectives of one location. It compiles human-friendly visual primitives into
provider-executable camera semantics and selects a generation topology before
spend.

```text
visual_camera_control(clean_identity, control_diagram?, perspective_anchors[],
                      maneuvers[], provider_constraints)
  -> CameraControlPacket + generated_clips + adherence_evidence
state: reads(source assets, storyboard or shot intent, live provider schema,
             prior adherence evidence); writes(prompt/input/result packets,
             trajectory.json, clips, adherence.md)
gates: reference_roles_bound; topology_selected_before_spend;
       every_maneuver_has_acceptance_check; continuity_handoffs_bound
fails: treats arrows as a complete prompt; overloads one short generation;
       confuses camera roll with translational orbit; claims deterministic geometry
```

## Use When

- A user draws arrows or a route over an image and expects the camera to follow
  it.
- One location must be shown from aerial, oblique, low, orbiting, top-down, or
  other ordered perspectives.
- A camera move must keep a landmark or product feature gaze-locked while the
  viewpoint translates.
- A prior generation looked cinematic but failed an exact path or terminal
  viewpoint.

Do not use this method for deterministic 3D camera animation, scroll-linked web
motion, or code-rendered scenes. Route those to `remotion`, a 3D owner, or the
frontend animation owner. Resource Bank can store source media, control images,
golden examples, prompts, and outputs; it does not own this executable method.

## Inputs

```text
camera_control_request:
  required:
    clean_identity:
      asset_ref: image or video without instructional marks
      identity_anchors: location, landmark, topology, lighting, time of day
    maneuvers:
      - id: stable maneuver identifier
        order: integer
        path: approach | curve | helix | orbit | fly_by | crane | retreat | custom
        altitude: start band -> end band
        orientation: yaw, pitch, roll, horizon behavior
        gaze: forward | landmark_lock | free | terminal_target
        speed: slow | moderate | fast | timed description
        terminal_state: required final framing and perspective
        acceptance: observable pass condition
    provider_constraints:
      candidate_family: optional until live discovery
      duration_seconds: total or per-clip budget
      aspect_ratio: requested output ratio
      resolution: requested output resolution
      audio_policy: provider_audio | master_audio | silent_asset
  optional:
    control_diagram:
      asset_ref: annotated image or map
      annotation_legend: colors, arrows, waypoints, labels, instruction-only marks
    perspective_anchors:
      - maneuver_id: owning maneuver
        role: start | end | identity | spatial_detail
        asset_ref: image or frame
    prior_attempt:
      result_ref: prior clip
      adherence_ref: clear, partial, and absent states
  source_refs:
    provenance: source URL, Resource Bank capture, project asset, or generated frame
    rights_note: reuse, inspired generation, or original generation boundary
```

## Workflow

1. **Compile the visual primitives.** Convert every mark and instruction into
   six semantic channels. Do not send an arrow-only prompt.

   ```text
   path        := ground track or spatial curve
   altitude    := vertical position and change
   orientation := yaw + pitch + roll + horizon recovery
   gaze        := where the optical axis points while the camera translates
   speed       := velocity, acceleration, and easing
   time        := maneuver order, duration, and terminal frame
   ```

   Bind the control diagram as instruction-only. Explicitly prohibit its lines,
   arrows, labels, numbers, circles, and typography from appearing in the
   generated world.

2. **Choose topology before spend.** Count independently testable camera
   states, not drawn waypoints.

   Use `single_shot` only when all requested movement is compatible:

   - one continuous route without self-crossing or reversal;
   - one stable gaze mode and no landmark orbit beyond 120 degrees;
   - no sequence that combines high, low, and an exact terminal perspective;
   - no more than two independently scored camera states;
   - the provider duration can show every state without compressing it; and
   - no prior single-shot adherence failure exists for the same shape.

   Use `chained_maneuvers` when any of these is true:

   - three or more independently scored camera states;
   - a landmark-locked orbit greater than 120 degrees;
   - self-crossing, reversing, or return-to-origin geometry;
   - high-to-low movement plus another exact terminal view;
   - distinct gaze modes must switch during the sequence;
   - the requested moves exceed the useful duration of one generation; or
   - a previous one-shot attempt marked any critical maneuver `partial` or
     `absent`.

   Split by geometric maneuver, not by every waypoint. Compatible approach
   curves may share a clip; a helix, landmark orbit, low fly-by, or exact
   crane-to-top-down move normally receives its own clip.
   A maneuver previously scored `partial` or `absent` always receives its own
   retry clip; do not merge it with an easier approach or exit move.

   Choose the output bundle slug during this step. A planning-only response
   still names the exact future `trajectory.json`, per-clip prompt/input/result,
   final clip, and `adherence.md` paths with `status: planned`. Do not open with
   `worked`, `pass`, or another completion claim while those artifacts are only
   proposed.

3. **Bind perspective anchors.** Keep one clean identity reference for the
   whole location. For each chained maneuver, require a start frame and an end
   frame or an explicit reason the live provider cannot accept both. The end
   frame of clip N becomes the start frame of clip N+1. When an exact terminal
   view matters, design or select that end frame before generation rather than
   asking prose alone to invent it.

   If required anchors do not exist, pause spend and route asset preparation to
   `asset-advisor` or `ai-image-advisor`. Do not generate several unrelated
   perspective stills and call them a continuous location.

4. **Compile one prompt per clip.** Keep the global identity anchors constant,
   but narrow each prompt to one geometric job.

   ```text
   CLIP <id> — <maneuver name>
   Reference roles: <clean identity, diagram, start, end, spatial detail>
   Start state: <position + altitude + orientation + gaze + framing>
   Camera movement: <translation path; distinguish orbit from roll/spin>
   Timing: <ordered phases inside this clip only>
   Terminal state: <observable final perspective and framing>
   Continuity: <identity, lighting, topology, velocity handoff>
   Instruction marks: disappear; never become physical or graphic elements
   Avoid: <cuts, montage, teleportation, topology drift, wrong gaze, wrong ending>
   ```

   Prefer observable language. For example, a valid orbit says the landmark
   stays near frame centre while the background rotates through the requested
   arc because the camera translates around it. “Dynamic circular movement” is
   not testable and permits an in-place roll.

5. **Capability- and spend-gate the provider.** Check the live schema for
   first frame, end frame, multiple references, duration, ratio, resolution,
   seed, audio, and watermark fields. Use image-to-video for a bounded anchored
   move and reference-to-video when multiple identity or spatial references are
   needed. Record the estimate and approval boundary before running external
   compute.

6. **Generate and hand off continuity.** For `single_shot`, save the clean
   input, diagram, compiled prompt, provider input, result, and clip together.
   For `chained_maneuvers`, generate the cheapest faithful maneuver first,
   inspect adherence, and continue only when its terminal frame can seed the
   next clip. Do not batch all clips before the hardest geometric move passes.
   Disable provider audio when a later Remotion or master-audio plan owns the
   mix.

7. **Judge geometry, not vibes.** Freeze an acceptance rubric before
   generation. Score each maneuver `clear`, `partial`, or `absent`, then check
   hard failures:

   - editorial cut or teleportation inside a continuous clip;
   - instructional-mark leakage;
   - landmark, location, or topology collapse;
   - an orbit that is only roll, spin, pan, or fly-by;
   - a terminal view that does not match its anchor; or
   - a generic forward move replacing the requested geometry.

   A beautiful clip that misses a critical maneuver is a failed control result.
   Preserve failed clips and their adherence notes as regression evidence.

## Output Shape

```text
CameraControlPacket:
  method: ai-video-advisor:visual-camera-control
  topology: single_shot | chained_maneuvers
  identity_anchors: []
  control_diagram:
    asset_ref:
    instruction_only: true
    legend:
  maneuvers:
    - id:
      clip_id:
      semantic_channels:
        path:
        altitude:
        orientation:
        gaze:
        speed:
        time:
      start_frame:
      end_frame:
      prompt_ref:
      provider_input_ref:
      acceptance:
  continuity:
    frame_handoffs: []
    invariant_identity: []
    audio_policy:
  clip_plan:
    - clip_id:
      maneuver_ids: []
      start_frame:
      end_frame:
      handoff_to:
      prompt_path:
      input_path:
      result_path:
      final_clip_path:
  evidence:
    result_refs: []
    contact_sheets: []
    adherence_ref:
    maneuver_evidence:
      - maneuver_id:
        acceptance: observable geometry rule, including gaze and translation when relevant
        score_scale: [clear, partial, absent]
        score: pending | clear | partial | absent
        evidence_path:
        failed_clip_retention_path: predeclared for every maneuver
  blockers: []
```

Save the project-bound bundle as:

```text
output/ai-video-advisor/<slug>/
  trajectory.json
  control-diagram.png        # when supplied
  references/
  clips/<clip-id>/
    prompt.md
    input.json
    result.json
    final.mp4
    start-frame.png
    end-frame.png
  final.mp4                  # after accepted assembly
  contact-sheet.jpg
  adherence.md
  notes.md
```

## Quality Gates

- The topology decision is recorded before provider execution, with the exact
  condition that selected it.
- Planning-only packets name exact bundle paths as `planned`; completion claims
  require those paths to exist and the adherence report to be inspected.
- Chained packets expand every clip's start frame, end frame, prompt, input,
  result, final clip, evidence, and failure-retention path. Wildcards such as
  `clips/<clip-id>/` are not an exact bundle contract.
- Every maneuver has one observable acceptance statement and evidence after
  generation.
- Every chained clip has an explicit frame handoff; missing anchors block
  spend rather than silently becoming isolated generations.
- The clean identity reference and annotated control diagram have different,
  explicit roles.
- An orbit is accepted only when the camera translates around a gaze-locked
  landmark; roll, spin, pan, and fly-by do not substitute.
- The final report says `pass`, `partial`, or `fail`; visual quality alone does
  not override trajectory adherence.

## Positive Example

```text
request: high aerial -> corkscrew dive -> low fly-by -> 270-degree Ferris-wheel
         orbit -> exact top-down crane-out

topology: chained_maneuvers
reason: five independently scored states + >120-degree landmark orbit +
        high/low/exact-terminal combination

clips:
  01_approach_dive: aerial start -> low aligned pier entrance
  02_low_flyby:     low entrance -> Ferris-wheel approach
  03_orbit:         landmark-locked start -> 270-degree translated end frame
  04_crane_out:     orbit exit -> designed near-vertical top-down frame
```

## Bad Output

- “Follow the arrows and make an insane cinematic drone shot” with no semantic
  compilation, topology decision, anchors, or acceptance checks.
- Five distinct perspective changes placed in one 10-second prompt because the
  provider technically allows ten seconds.
- Several unrelated perspective images submitted as references without start
  and end roles or location-continuity invariants.
- Calling a rolling fly-by a completed 270-degree orbit.
- Deleting a failed clip instead of preserving it as a regression example.
