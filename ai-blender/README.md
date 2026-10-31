# AI Blender Studio — Phase 1

An additive, phone-first procedural modelling prototype. Existing TN Bus Studio assets, simulator and viewers are untouched.

## Run
Open `ai-blender/index.html` on a static host, select a preset, and download a scene JSON. From GitHub Actions, open **AI Blender Phase 1**, select a preset, and run the workflow. Download the `ai-blender-<preset>` artifact containing a native BLEND, GLB and preview PNG.

Supported presets: cube, chair, table. The workflow uses deterministic, reviewed Blender Python; it does **not** execute arbitrary prompt-generated code, call paid AI services or claim general text-to-3D yet. JSON generated in the UI is a specification preview for future integration, not an automatic workflow input.

## Local smoke test
`blender -b -t 2 --python ai-blender/blender/generate.py -- --preset chair --output /tmp/ai-blender`
`python3 ai-blender/tests/validate_glb.py /tmp/ai-blender/chair.glb`

No existing bus assets are replaced. GitHub-hosted runners and artifacts remain subject to account quotas.
