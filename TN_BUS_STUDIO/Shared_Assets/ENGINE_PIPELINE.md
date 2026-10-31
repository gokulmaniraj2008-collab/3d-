# One Blender bus, two game engines, one web viewer

Generate with `blender -b -t 2 --python-exit-code 1 --python TN_BUS_STUDIO/Blender/generate_bus.py`. Run `python3 TN_BUS_STUDIO/Blender/validate_engine_assets.py` after generation. The GLB, BLEND, preview PNG and generated engine_manifest.json are workflow artifacts.

- Godot 4.3: copy TN_Bus.glb into Godot/TN_Bus_Simulator/assets/ and run the headless editor import and smoke test. The web export uses this same asset.
- Unreal 5.4: use the same GLB with a supported Interchange importer, or open the BLEND in Blender and export FBX. Inspect units, axes, materials, collision, skeleton and wheel separation manually. The Unreal source project is not compiled by hosted CI.
- Web: publish the generated GLB to ai-3d-studio/models/TN_Bus.glb for the existing model viewer.

Do not mistake sharing geometry for sharing driving code: GDScript and Unreal C++/Blueprint require separate implementations. Do not commit generated BLEND/GLB into source directories unless the publishing workflow intentionally does so.
