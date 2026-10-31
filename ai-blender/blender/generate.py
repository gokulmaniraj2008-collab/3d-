"""Deterministic Blender 3D preset generator; no untrusted code execution."""
import argparse
import math
import os
import sys

import bpy


def cube(name, location, scale, material):
    bpy.ops.mesh.primitive_cube_add(size=1, location=location)
    obj = bpy.context.object
    obj.name = name
    obj.dimensions = scale
    bpy.ops.object.transform_apply(location=False, rotation=False, scale=True)
    obj.data.materials.append(material)
    bevel = obj.modifiers.new("Soft edges", "BEVEL")
    bevel.width = 0.035
    bevel.segments = 2
    obj.modifiers.new("Weighted normals", "WEIGHTED_NORMAL")
    return obj


def material(name, rgba):
    mat = bpy.data.materials.new(name)
    mat.diffuse_color = rgba
    return mat


def build(preset):
    bpy.ops.object.select_all(action="SELECT")
    bpy.ops.object.delete(use_global=False)
    wood = material("Warm wood", (0.44, 0.23, 0.10, 1))
    accent = material("Blue accent", (0.10, 0.38, 0.67, 1))
    if preset == "cube":
        cube("Rounded cube", (0, 0, 0.5), (1, 1, 1), accent)
    elif preset in ("chair", "table"):
        width = 1.2 if preset == "chair" else 2.0
        depth = 1.1 if preset == "chair" else 1.2
        height = 0.75
        cube("Seat" if preset == "chair" else "Tabletop", (0, 0, height), (width, depth, 0.12), wood)
        for x in (-width / 2 + 0.12, width / 2 - 0.12):
            for y in (-depth / 2 + 0.12, depth / 2 - 0.12):
                cube("Leg", (x, y, height / 2 - 0.04), (0.11, 0.11, height - 0.08), wood)
        if preset == "chair":
            cube("Backrest", (0, depth / 2 - 0.06, 1.22), (width, 0.12, 0.85), accent)
    else:
        raise ValueError("Unsupported preset")
    bpy.ops.object.camera_add(location=(3.5, -4.5, 3.0))
    camera = bpy.context.object
    from mathutils import Vector
    camera.rotation_euler = (Vector((0, 0, 0.65)) - camera.location).to_track_quat("-Z", "Y").to_euler()
    bpy.context.scene.camera = camera
    bpy.ops.object.light_add(type="AREA", location=(1, -3, 5))
    bpy.context.object.data.energy = 650
    bpy.context.object.data.shape = "DISK"
    bpy.context.object.data.size = 5
    scene = bpy.context.scene
    scene.render.engine = "CYCLES"
    scene.cycles.samples = 16
    scene.render.resolution_x = 640
    scene.render.resolution_y = 480
    scene.render.resolution_percentage = 100


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--preset", choices=["cube", "chair", "table"], required=True)
    parser.add_argument("--output", required=True)
    args = parser.parse_args(sys.argv[sys.argv.index("--") + 1:] if "--" in sys.argv else [])
    os.makedirs(args.output, exist_ok=True)
    build(args.preset)
    bpy.ops.wm.save_as_mainfile(filepath=os.path.join(args.output, args.preset + ".blend"))
    bpy.ops.export_scene.gltf(filepath=os.path.join(args.output, args.preset + ".glb"), export_format="GLB", use_selection=False)
    bpy.context.scene.render.filepath = os.path.join(args.output, args.preset + ".png")
    bpy.ops.render.render(write_still=True)
    for ext in ("blend", "glb", "png"):
        path = os.path.join(args.output, args.preset + "." + ext)
        assert os.path.getsize(path) > 100, path
        print("Generated", path)


if __name__ == "__main__":
    main()
