# TN Bus Simulator (Godot 4.3)

Open `TN_Bus_Simulator/project.godot` in Godot 4.3 and press Play. Use **W / Up** to accelerate, **S / Down** to reverse, **A/D or Left/Right** to steer, and **Space** to brake. On touchscreens use the ◀ ▶ GO STOP buttons. The camera follows the bus on a simple road.

The game loads `assets/TN_Bus.glb` if imported; otherwise it creates a simple procedural bus so the project can still run without downloaded assets. The **Validate Godot TN Bus Simulator** GitHub Actions workflow generates the GLB using Blender, imports it in headless Godot, runs the smoke test and uploads the complete project ZIP. The simulator is an arcade prototype, not a realistic vehicle physics simulation. Android APK export is not implemented yet.

## Tamil Nadu village road

The default simulator now builds a deterministic, Tamil Nadu-inspired rural scene in `scripts/village_road.gd`: two-lane road, markings, shoulders, paddy fields, irrigation canals, coconut palms, roadside houses, utility poles and a bus shelter. Geometry is generated using Godot primitives, so no paid textures or external assets are required. The ground, houses, tree trunks and poles have collisions; decorative features do not. The existing bus controls and Blender GLB workflow remain unchanged. The smoke test additionally checks that the village scene and bus stop exist.
