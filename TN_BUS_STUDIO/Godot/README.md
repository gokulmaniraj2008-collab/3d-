# TN Bus Simulator — Godot 4.3

A lightweight arcade prototype with a Tamil Nadu-inspired village road. Open `TN_Bus_Simulator/project.godot` in Godot 4.3 and press **Play**. The project uses the GL Compatibility renderer.

## Driving controls

| Action | Keyboard | Touchscreen |
| --- | --- | --- |
| Accelerate | W / Up | GO |
| Reverse | S / Down | — |
| Steer | A/D or Left/Right | ◀ / ▶ |
| Brake | Space | STOP |

The follow camera and speed display are created by `scripts/world.gd`. The bus is driven by `scripts/bus.gd`; this is arcade movement, not realistic vehicle dynamics. The project is not yet an Android APK.

## Village environment

`scripts/village_road.gd` builds the scene deterministically with Godot primitives: two-lane road and markings, dirt shoulders, paddy fields, irrigation canals, coconut trees, houses, utility poles and a roadside bus shelter. Ground, houses, trunks and poles have collision; decorative geometry does not. This is an illustrative village, not a map of a specific real location.

## Bus asset and automated checks

When `assets/TN_Bus.glb` is available and imported, the game loads the Blender-generated bus. Otherwise, it uses a simple fallback bus. The **Validate Godot TN Bus Simulator** workflow validates the JSON model settings, runs Blender, verifies exported files, copies the GLB into this project, imports in Godot 4.3, runs `tests/smoke_test.gd` and uploads `TN-Bus-Godot-Project` **only if all steps succeed**.

On Android, download the project ZIP from a successful GitHub Actions run and keep the included asset directory. Viewing the PNG preview is possible on your phone; running/editing the Godot project requires a compatible Godot environment.
