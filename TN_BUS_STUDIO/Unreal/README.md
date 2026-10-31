# Unreal integration — planned

TN Bus Studio currently produces a portable `TN_Bus.glb` from Blender and a Godot 4.3 arcade prototype. **No Unreal Engine scene, Unreal build, packaged game or automated Unreal validation is implemented yet.**

Future work: test importing a compatible mesh (or convert via Blender to a suitable interchange format), assign Unreal materials, create a vehicle setup and build a scene on a supported desktop environment. The existing GitHub Actions workflows validate Blender and Godot only. Do not interpret a successful GLB build as a verified Unreal import.
