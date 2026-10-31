# Unreal Engine foundation (5.4 target)

This is an **Unreal-ready source project**, not a compiled or tested Unreal game. A PC with a licensed UE 5.4 installation and C++ toolchain is required to open, generate project files, compile and test it. Do not upload engine binaries or paid assets to GitHub.

1. Download the latest TN-Bus-3D artifact from GitHub Actions.
2. Unzip and import `TN_Bus.glb` through Unreal's Interchange importer if supported by your installed UE version, or export FBX from the BLEND source and import that.
3. Confirm axes, scale, materials and collisions in Unreal Editor; keep meshes in `Content/TNBus/`.
4. Create a vehicle pawn and configure physics/Chaos Vehicles in the editor when a PC is available. Godot driving code cannot be used directly in Unreal.
5. Use the village-road Godot scene as a *reference specification*, not an Unreal-compatible scene file.

No Unreal build is claimed in GitHub Actions. The free hosted runner does not include the Unreal Editor or its licensed engine distribution.
