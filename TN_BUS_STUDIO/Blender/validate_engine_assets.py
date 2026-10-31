"""Validate the shared Blender GLB for both Godot and Unreal import workflows."""
import json, os, struct
root=os.path.abspath(os.path.join(os.path.dirname(__file__),"..","Shared_Assets"))
path=os.path.join(root,"TN_Bus.glb")
with open(path,"rb") as f: raw=f.read()
assert raw[:4]==b"glTF" and struct.unpack_from("<I",raw,4)[0]==2
assert struct.unpack_from("<I",raw,8)[0]==len(raw), "GLB length mismatch"
length,kind=struct.unpack_from("<I4s",raw,12)
assert kind==b"JSON"
doc=json.loads(raw[20:20+length])
assert doc.get("meshes") and doc.get("materials"), "Missing mesh or material"
assert doc.get("scenes") and doc.get("nodes"), "Missing scene or nodes"
assert len(raw)>10000, "GLB suspiciously small"
manifest={"source":"Blender/generate_bus.py","asset":"TN_Bus.glb","format":"glTF 2.0 binary","mesh_count":len(doc["meshes"]),"material_count":len(doc["materials"]),"bytes":len(raw),"targets":{"godot":"Import GLB into res://assets/","unreal":"Import GLB using supported Interchange importer or convert BLEND to FBX in Blender; configure vehicle physics separately","web":"Serve as model-viewer asset"}}
with open(os.path.join(root,"engine_manifest.json"),"w") as f: json.dump(manifest,f,indent=2)
print(json.dumps(manifest,indent=2))
