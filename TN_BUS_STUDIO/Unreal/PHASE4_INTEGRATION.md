# Phase 4 Unreal integration contract

Unreal is an **editor-ready source foundation**, not a compiled or gameplay-verified port. The Godot prototype is the gameplay reference, not a binary-compatible project.

## Shared Blender asset

- Source: `TN_BUS_STUDIO/Blender/generate_bus.py`; GitHub Actions artifact `TN-Bus-3D` contains `TN_Bus.blend` and `TN_Bus.glb`.
- Import GLB with Unreal Interchange when supported, otherwise export FBX from BLEND using Blender. Confirm metres/centimetres scale, forward axis, pivot, mesh normals and material slots in UE 5.4 Editor.
- Create collision bodies and wheel bones/meshes separately; the GLB is a visual model and is **not** a rigged Chaos vehicle.

## Gameplay parity checklist (to implement and test on a compatible PC)

1. Create a Chaos vehicle pawn with wheel blueprints, suspension, engine torque, braking and speed-sensitive steering; enable Chaos Vehicles plugin in Unreal Editor.
2. Implement handbrake and closed-door movement interlock; disallow opening doors above 0.1 m/s.
3. Recreate Route 001 with Village Stop, Agricultural Market and Town Terminal. Stop completion requires bus within 8 m, stationary and doors open.
4. Track deterministic passenger counts and route HUD, then replace counters with animated boarding after core gameplay is tested.
5. Test controls, collisions, asset import, packaging and mobile performance in Unreal Editor. GitHub Actions does not compile UE or package an Android APK.

Godot coordinates and scene scripts are reference data; do not import GDScript as Unreal C++ or Blueprints.
