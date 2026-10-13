---
kind: technique-catalog
owner: skills/ml-autoresearch
status: active
created_at: 2026-10-13
---

# Technique catalog: efficient inference for small models

Load this as the `technique_catalog` input when a campaign's primary metric is
latency, throughput, model size, or on-device cost (browser WebGPU, mobile,
edge). Each entry is a candidate hypothesis source, not a recommendation: the
source stage turns an entry into a tree node only when its precondition matches
the profiled bottleneck, and the node still needs its own expected observation,
falsifier, and receipt. Append verified outcomes to **Field results**; never
edit an entry to match a single campaign.

## 1. Diagnose the bottleneck before choosing

| Signal | Bottleneck | Points to |
| --- | --- | --- |
| Summed kernel time far below wall time | dispatch / CPU overhead | fewer ops, graph capture, fusion, caching |
| Wall time tracks FLOPs or channel width | kernel-bound | width, resolution, precision |
| Large tensors, low arithmetic intensity (cost volumes, gathers) | memory-bound | fewer channels at the op, lower resolution, fused kernels |
| Output read back to CPU every frame | readback stall | keep tensors on GPU, IO binding |
| Same inputs recomputed every frame | redundant work | caching, temporal reuse |

Profile per op type and per model part (GPU timestamps), and microbench the
runtime's fusion behaviour (e.g. N small convs with and without activations)
before trusting a FLOP or node count.

## 2. Catalog

| Family | Technique | Mechanism | Applies when | Typical gain | Failure modes | Sources |
| --- | --- | --- | --- | --- | --- | --- |
| Measurement | Interleaved baseline timing | candidate and baseline in alternating blocks, report the ratio | shared or noisy machines | removes most load drift | ratios still drift between sessions; load inflates them for overhead-bound models | campaign practice |
| Caching | Cache static-input branches | encode inputs that do not change (a fixed garment, prompt, style, background) once | live video with a fixed conditioning input | the branch's whole cost per frame | stale cache when the input changes; verify exact output match | LiveVVT 2608.26714 (garment memory built once) |
| Caching | Keyframe + feature propagation | heavy branch on keyframes, cheap warp of features in between | video, motion moderate | 1.5-2x on non-keyframes | lag or ghosting on fast motion | Deep Feature Flow 1611.07715 |
| Caching | Similarity skip | skip or reuse output when the frame barely changed (probabilistic gate) | static-heavy streams | 2-2.4x GPU load on static input | flicker if the gate is a hard threshold | StreamDiffusion 2312.12491 |
| Caching | Deep-feature reuse across steps or frames | reuse high-level features, recompute shallow ones | U-Net-like models with stable deep features | 2.3x (diffusion steps) | quality drift; needs a video evaluator | DeepCache 2312.00858 |
| Caching | Temporally distributed sub-networks | split a deep encoder into N shallow parts, one per frame, fuse | recurrent streams | up to ~N on the split part | needs retraining | TDNet 2004.01800 |
| Sparsity | Frame-difference convs | compute only where pixels changed | static camera | 3-7x with custom kernels | browsers lack sparse kernels | Skip-Convolutions 2104.11487; DeltaCNN 2203.03996 |
| Structure | Prune whole stages or pyramid levels | remove the finest or least-used levels, upsample the result | multi-scale designs where fine levels dominate cost | large | alignment or detail loss; check per-level quality | campaign practice |
| Structure | Channel narrowing with sliced warm start | build narrower layers, copy leading slices of pretrained weights, fine-tune | wide heads or pyramids | grows with removed channels | concat inputs need per-half slicing; some parts (decoders) break | DepGraph / Torch-Pruning 2301.12900 |
| Structure | Lower-resolution sub-branch | run a smooth-output branch (flow, alignment) at reduced resolution | branch outputs are low-frequency | ~resolution^2 on that branch | odd sizes can break index-based ops | campaign practice; RVM downsample_ratio 2108.11515 |
| Distillation | Distill on teacher outputs only | student matches the teacher on the hard (unpaired) task | self-reconstruction losses leak a shortcut | quality recovers after cuts | a paired reconstruction loss can teach "copy the input" | campaign practice |
| Distillation | Patient, consistent distillation | same augmented view to teacher and student, long schedules | narrow students that fail at short budgets | closes much of the gap | needs a larger time budget (a frozen-budget change) | Beyer et al. 2106.05237 |
| Distillation | Intermediate-feature / multi-layer distillation | match teacher features, not just outputs | image-to-image students | up to 40x fewer MACs reported | layer matching choices | OMGD 2108.06908; CVPR 2021 "Teachers Do More Than Teach"; Wavelet KD (CVPR 2022) |
| Precision | fp16 weights and activations | halve memory traffic | GPU runtimes with fp16 support | ~1.3-2x | some runtime versions compute fp16 wrongly; check against fp32/CPU | campaign practice |
| Precision | int8 / int4 | integer kernels | only where the runtime has integer conv kernels | large where supported | ORT-web 1.30 WebGPU has no QLinearConv/ConvInteger: int8 only shrinks downloads | ORT v1.30 source |
| Re-param | RepVGG / MobileOne branch merging | train multi-branch, deploy one conv | launch-bound or depthwise-heavy nets | fewer ops; dense 3x3 often faster than depthwise | retraining | RepVGG 2101.03697; MobileOne 2206.04040 |
| Architecture | Mobile backbones | MobileNetV4 UIB, RepViT, FastViT, EfficientViT | redesign is allowed | hardware-dependent | tuned for NPU/CPU; on WebGPU pick by layer count and measure | 2404.10518; 2307.09283 |
| Runtime | Graph capture | record the command list once, replay | launch-bound, static shapes, all ops on GPU | 1.3-2x when overhead dominates | ORT-web binds IO once: feed the same GPU buffers (writeBuffer), pre-allocate outputs | ORT-web 1.30 `wasm-core-impl.ts` |
| Runtime | Keep tensors on the GPU | GPU preprocessing, output drawn without readback | live rendering | 1-3 ms per frame plus no stall | not visible in benchmarks that read back | ORT IO binding docs |
| Runtime | Session flags | NHWC layout, validationMode disabled, bucket buffer cache | cheap A/B | 0-15% (unverified) | layout transposes around NCHW-only ops | ORT WebGPU EP docs |
| Runtime | Alternative runtimes | LiteRT.js (WebGPU via ML Drift), WebNN, ExecuTorch + Core ML | the current runtime is the limit | claimed up to 3x (LiteRT.js on M4) | op coverage (e.g. grid_sample) and maturity | Google blog 2026-07-09; WebNN OT Chrome 145-147 |
| Runtime | Custom fused kernels | fuse memory-bound chains (cost volume + warp) into one shader | profiling shows a dominant memory-bound chain | potentially large | engineering cost; correctness | practitioner reports (unverified for vision) |

## 3. Field results

Append one line per verified campaign outcome: model class, change, result,
evaluator, and the receipt it came from. Keep project names generic.

- 2026-10-13, DM-VTON-class try-on student, ORT-web 1.30 WebGPU, 256x192:
  - Cost volume kept only at the 2 coarsest levels: 1.84x zero-shot, quality unchanged.
  - Half-resolution warp: 2.77x zero-shot; misaligned until a distill-only fine-tune (3.4x, guards pass).
  - Skipping the finest pyramid step: passes after fine-tuning at 4 of 5 steps; fails at 3 of 5 in a 20-min budget.
  - Narrower pyramids, 256 to 128 and to 96 channels: no measurable quality loss after a 20-min sliced-warm-start fine-tune; about 1.08x per step.
  - Narrower refine heads, generator and pyramid backbones: failed the quality guards at a 20-min budget; untested with longer distillation.
  - Caching the fixed garment branch: exact output match, 430 to 372 ops per frame; about 1.05x per frame (6.28x vs the teacher, one unloaded run).
  - Narrow-pyramid student held quality across two training seeds (paired LPIPS 0.0962 / 0.0972).
  - Activations fused (a small conv costs about 25 µs to launch). Graph capture failed when fed new CPU tensors per run.
  - A paired reconstruction loss let the student keep the original clothes: paired metric improved, unpaired FID worsened. Likely, confounded by step count.
  - Best verified result: about 5.6x vs the teacher, with paired LPIPS and unpaired FID inside the guards.
