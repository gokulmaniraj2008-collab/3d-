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

## Phase 2: configurable prompt-directed builds (Android friendly)

**This is prompt-directed, not an unattended AI agent.** Tell ChatGPT what you want changed, review its proposed JSON/source changes in a PR, and let GitHub Actions run the free Blender/Godot tools. No API key, subscription or phone-side Blender installation is required. GitHub Actions limits and artifact expiry still apply.

1. On your phone, open `TN_BUS_STUDIO/Blender/bus_config.json` in GitHub and tap the pencil (or ask ChatGPT to edit it in a branch). Only change the JSON values, not Python code.
2. Supported settings: `body_color`, `roof_color`, `seat_color` (three RGB numbers 0–1); `seat_rows` (1–7); `roof_vents` (0–3); `destination` (1–40 printable characters); `preview_samples` (8–64). These settings are checked before Blender starts. Destination text uses Blender's bundled font; use Latin characters for reliable rendering.
3. Open your PR and view its **Checks** tab. The Blender workflow validates settings, exports the editable BLEND, portable GLB and PNG preview, verifies file signatures and uploads `TN-Bus-3D`. The Godot workflow imports the generated GLB, runs the simulator smoke test and uploads `TN-Bus-Godot-Project` on success.
4. Tap **Actions**, open the successful run, scroll to **Artifacts** and download the ZIP to Android. Unzip with your phone's file manager. PNG previews open on Android; BLEND requires Blender on a supported computer, and the Godot project requires Godot to play. The project is not an Android APK.
5. If a check fails, open the failed job log and send the error to ChatGPT. Do not merge until both workflows pass. The generated binaries are build artifacts, not source commits.

**Example prompt:** "Set my TN Bus Studio body to dark green [0.05,0.22,0.10], roof cream [0.85,0.8,0.65], 6 passenger seat rows and 2 roof vents. Update bus_config.json in a PR, preserve all files and verify both Actions builds."

**Safety:** The workflow reads a fixed, validated JSON schema and does not execute arbitrary prompt text, shell commands or user-supplied Python.
