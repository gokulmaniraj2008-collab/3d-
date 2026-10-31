# AI Blender Studio — Phase 1

An additive, phone-first procedural modelling prototype. Existing TN Bus Studio assets, simulator and viewers are untouched.

## Run
Open `ai-blender/index.html` on a static host, select a preset, and download a scene JSON. From GitHub Actions, open **AI Blender Phase 1**, select a preset, and run the workflow. Download the `ai-blender-<preset>` artifact containing a native BLEND, GLB and preview PNG.

Supported presets: cube, chair, table. The workflow uses deterministic, reviewed Blender Python; it does **not** execute arbitrary prompt-generated code, call paid AI services or claim general text-to-3D yet. JSON generated in the UI is a specification preview for future integration, not an automatic workflow input.

## Android 3D preview
Open `ai-blender/preview.html` from the deployed static site. Download a Phase 2 GitHub Actions artifact ZIP, extract it on your phone, and select `scene.glb`. The viewer validates the GLB 2.0 header and file size, uses a temporary local object URL, and supports orbit, pinch zoom, camera reset and clearing the model. It does not upload the file, call Gemini or modify the TN Bus simulator. The external model-viewer library needs network access. Preview is a separate page, not automatically populated by GitHub artifact downloads.

## Local smoke test
`blender -b -t 2 --python ai-blender/blender/generate.py -- --preset chair --output /tmp/ai-blender`
`python3 ai-blender/tests/validate_glb.py /tmp/ai-blender/chair.glb`

No existing bus assets are replaced. GitHub-hosted runners and artifacts remain subject to account quotas.
