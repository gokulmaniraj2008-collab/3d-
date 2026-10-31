"""Check generated assets are present and structurally plausible."""
import json
import os
import struct
from pathlib import Path

out = Path(os.environ.get("BUS_OUTPUT", "TN_BUS_STUDIO/Shared_Assets"))
blend, glb, png = (out / name for name in ("TN_Bus.blend", "TN_Bus.glb", "TN_Bus_preview.png"))
for path in (blend, glb, png):
    if not path.is_file() or path.stat().st_size < 100:
        raise SystemExit("Missing or empty artifact: " + str(path))
with glb.open("rb") as stream:
    header = stream.read(12)
    if len(header) != 12 or header[:4] != b"glTF" or struct.unpack_from("<I", header, 4)[0] != 2 or struct.unpack_from("<I", header, 8)[0] != glb.stat().st_size:
        raise SystemExit("Invalid GLB header or length")
with png.open("rb") as stream:
    if stream.read(8) != b"\x89PNG\r\n\x1a\n":
        raise SystemExit("Invalid PNG signature")
if not blend.read_bytes()[:7] == b"BLENDER":
    raise SystemExit("Invalid BLEND signature")
print("Verified BLEND, GLB and PNG:", json.dumps({p.name: p.stat().st_size for p in (blend, glb, png)}))
