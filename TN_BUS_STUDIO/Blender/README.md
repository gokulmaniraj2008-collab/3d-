# Configurable Blender generator

`bus_config.json` is the small, reviewable interface for prompt-directed changes. Ask ChatGPT to change only supported values, or edit JSON directly from GitHub on Android. `bus_config.py` validates the schema; `validate_config.py` runs without Blender. The generator `generate_bus.py` uses these settings to build the stylized bus, and `validate_outputs.py` checks the generated file sizes and basic signatures.

From the repository root:

```sh
python3 TN_BUS_STUDIO/Blender/validate_config.py
blender -b -t 2 --python-exit-code 1 --python TN_BUS_STUDIO/Blender/generate_bus.py
python3 TN_BUS_STUDIO/Blender/validate_outputs.py
```

Outputs are written to `TN_BUS_STUDIO/Shared_Assets/` by default; `BUS_CONFIG` and `BUS_OUTPUT` environment variables may override their paths. Settings include three RGB colour lists (numbers from 0 to 1), `seat_rows` 1–7, `roof_vents` 0–3, printable `destination` 1–40 characters and `preview_samples` 8–64. Use Latin text for the most reliable bundled-font rendering. Config changes are not arbitrary Python execution.

The GLB is a portable interchange asset, not proof that a target game engine or Unreal import succeeds. Review CI logs and only use artifacts from successful runs.
