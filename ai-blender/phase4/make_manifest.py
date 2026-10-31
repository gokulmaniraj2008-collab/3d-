"""Prepare a bounded public gallery payload from a validated Blender build."""
import argparse
import json
import shutil
import struct
from pathlib import Path

MAX_BYTES = 50 * 1024 * 1024

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--source", required=True)
    parser.add_argument("--output", required=True)
    parser.add_argument("--run-id", required=True, type=int)
    parser.add_argument("--sha", required=True)
    args = parser.parse_args()
    source = Path(args.source) / "scene.glb"
    if not source.is_file() or not 20 <= source.stat().st_size <= MAX_BYTES:
        raise ValueError("GLB missing or exceeds gallery size limit")
    with source.open("rb") as handle:
        magic, version, length = struct.unpack("<4sII", handle.read(12))
    if (magic, version, length) != (b"glTF", 2, source.stat().st_size):
        raise ValueError("Invalid GLB 2.0 header")
    if len(args.sha) != 40 or any(ch not in "0123456789abcdef" for ch in args.sha):
        raise ValueError("Invalid source commit")
    output = Path(args.output)
    output.mkdir(parents=True, exist_ok=True)
    shutil.copyfile(source, output / "scene.glb")
    manifest = {"schemaVersion": 1, "runId": args.run_id, "sourceSha": args.sha,
                "file": "scene.glb", "bytes": length}
    (output / "latest.json").write_text(json.dumps(manifest, indent=2) + "\n", encoding="utf-8")

if __name__ == "__main__":
    main()
