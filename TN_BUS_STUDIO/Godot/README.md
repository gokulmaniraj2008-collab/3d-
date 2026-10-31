# TN Bus Simulator (Godot 4.3)

Open `TN_Bus_Simulator/project.godot` in Godot 4.3 and press Play. Use **W / Up** to accelerate, **S / Down** to reverse, **A/D or Left/Right** to steer, and **Space** to brake. On touchscreens use the ◀ ▶ GO STOP buttons. The camera follows the bus on a simple road.

The game loads `assets/TN_Bus.glb` if imported; otherwise it creates a simple procedural bus so the project can still run without downloaded assets. The **Validate Godot TN Bus Simulator** GitHub Actions workflow generates the GLB using Blender, imports it in headless Godot, runs the smoke test and uploads the complete project ZIP. The simulator is an arcade prototype, not a realistic vehicle physics simulation. Android APK export is not implemented yet.
