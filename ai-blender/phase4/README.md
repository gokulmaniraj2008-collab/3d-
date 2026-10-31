# Phase 4 — automatic public model gallery

After merging this PR, run **Actions → AI Blender Phase 2 → Run workflow** on **main**, choosing example or prompt. A successful build uploads its usual 7-day artifact, then a separate main-only publish job copies only the validated `scene.glb` and minimal `latest.json` to the isolated `ai-blender-gallery` branch. The Android viewer's **Load latest AI-generated model** button reads those files without a ZIP download. The first successful manual run creates the gallery branch automatically. PR builds never publish.

**Privacy:** the gallery is public and keeps the latest GLB in Git history; do not generate sensitive/private content. The prompt, API key, BLEND and render are not copied to the gallery. Free GitHub Actions/storage and Gemini quotas remain subject to their providers' limits. The repository must stay public for anonymous raw-file access. The viewer still supports local file loading.

**Security:** build job has read-only repository permissions; the publish job gets contents:write only for a manual run on main after a successful build. The Gemini key is scoped to the prepare step rather than exposed job-wide. Publishing touches a dedicated branch, never main or any TN Bus simulator/model/viewer path. Only the most recently completed published run is shown.

**Verify after merge:** trigger example mode on main, check build and publish jobs, confirm `ai-blender-gallery/latest.json` and `scene.glb`, open `/ai-blender/preview.html` and tap Load latest AI-generated model. Test touch rotation, zoom, reset, clear and local GLB fallback. A GitHub PR preview alone cannot publish a model.
