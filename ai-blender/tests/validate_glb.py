"""Check GLB header and required Blender outputs without third-party packages."""
import json
import pathlib
import struct
import sys

path = pathlib.Path(sys.argv[1])
data = path.read_bytes()
assert len(data) >= 20 and data[:4] == b"glTF", "Invalid GLB magic"
version, length = struct.unpack_from("<II", data, 4)
assert version == 2 and length == len(data), "Invalid GLB header"
chunk_length, chunk_type = struct.unpack_from("<I4s", data, 12)
assert chunk_type == b"JSON" and 20 + chunk_length <= len(data), "Missing JSON chunk"
doc = json.loads(data[20:20 + chunk_length])
assert doc.get("meshes") and doc.get("nodes"), "No mesh or nodes"
print("Validated GLB 2.0:", path, "meshes:", len(doc["meshes"]))
