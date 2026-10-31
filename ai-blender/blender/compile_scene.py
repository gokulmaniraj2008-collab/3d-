"""Trusted Blender compiler for validated Phase 2 JSON, never executes model code."""
import argparse
import math
import os
import sys
from pathlib import Path

import bpy
from mathutils import Vector

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "phase2"))
from scene import COLORS, load

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--scene", required=True)
    parser.add_argument("--output", required=True)
    args = parser.parse_args(sys.argv[sys.argv.index("--") + 1:] if "--" in sys.argv else [])
    data = load(args.scene)
    os.makedirs(args.output, exist_ok=True)
    bpy.ops.object.select_all(action="SELECT")
    bpy.ops.object.delete(use_global=False)
    mats = {}
    for name, color in COLORS.items():
        mat = bpy.data.materials.new(name)
        mat.diffuse_color = color
        mats[name] = mat
    for item in data["objects"]:
        kind = item["type"]
        if kind == "box":
            bpy.ops.mesh.primitive_cube_add(size=1)
        elif kind == "cylinder":
            bpy.ops.mesh.primitive_cylinder_add(vertices=24, radius=0.5, depth=1)
        elif kind == "sphere":
            bpy.ops.mesh.primitive_uv_sphere_add(segments=24, ring_count=12, radius=0.5)
        else:
            bpy.ops.mesh.primitive_plane_add(size=1)
        obj = bpy.context.object
        obj.name = item["id"]
        obj.location = item["position"]
        obj.rotation_euler = item["rotation"]
        obj.dimensions = item["dimensions"]
        obj.data.materials.append(mats[item["material"]])
    bpy.ops.object.camera_add(location=(8, -11, 8))
    camera = bpy.context.object
    camera.rotation_euler = (Vector((0, 0, 0.8)) - camera.location).to_track_quat("-Z", "Y").to_euler()
    bpy.context.scene.camera = camera
    bpy.ops.object.light_add(type="AREA", location=(1, -4, 8))
    bpy.context.object.data.energy = 1200
    bpy.context.object.data.size = 8
    scene = bpy.context.scene
    scene.render.engine = "CYCLES"
    scene.cycles.samples = 12
    scene.cycles.use_denoising = False
    scene.render.resolution_x = 640
    scene.render.resolution_y = 480
    scene.render.resolution_percentage = 100
    scene.render.image_settings.file_format = "PNG"
    bpy.ops.wm.save_as_mainfile(filepath=os.path.abspath(os.path.join(args.output, "scene.blend")))
    bpy.ops.export_scene.gltf(filepath=os.path.abspath(os.path.join(args.output, "scene.glb")), export_format="GLB", export_draco_mesh_compression_enable=False)
    scene.render.filepath = os.path.abspath(os.path.join(args.output, "scene.png"))
    bpy.ops.render.render(write_still=True)
    for suffix in ("blend", "glb", "png"):
        assert os.path.getsize(os.path.join(args.output, "scene." + suffix)) > 100
    print("Phase 2 generated", len(data["objects"]), "objects")

if __name__ == "__main__":
    main()
