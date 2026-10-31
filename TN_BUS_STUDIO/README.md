# TN BUS STUDIO 🚌

Phone-first, prompt-directed 3D asset pipeline. ChatGPT edits the Blender Python source in this repository; GitHub Actions runs Blender in the cloud. No paid AI API is required. This is **not** an autonomous prompt-processing bot: send the prompt in ChatGPT and request a reviewed repository change.

## How to build on Android
1. Merge the setup PR into main.
2. Open **Actions → Build TN Bus 3D → Run workflow**.
3. Download the **TN-Bus-3D** artifact from the completed run.
4. The ZIP contains `TN_Bus.blend`, `TN_Bus.glb`, and `TN_Bus_preview.png`.

The first model is a stylized approximation, not an exact photo reconstruction. The GLB is intended as the shared starting asset for Godot and Unreal. FBX export and game logic are future tasks, not implemented here. GitHub Actions usage and artifact retention follow GitHub account terms.

## Prompt example
"Update TN_BUS_STUDIO/Blender/generate_bus.py to make the front windscreen taller and add a Tamil destination sign. Preserve other repository files, open a PR and verify the build."

## Structure
- Blender/generate_bus.py — editable procedural model
- Shared_Assets — generated at build time; do not commit large binaries
- Godot — planned Godot simulator
- Unreal — planned Unreal scene
