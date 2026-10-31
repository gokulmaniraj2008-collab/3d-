"""Strict scene specification validation shared by planner and Blender compiler."""
import json
import math
import re

TYPES = {"box", "cylinder", "sphere", "plane"}
COLORS = {"wood": (0.45, 0.24, 0.1, 1), "metal": (0.12, 0.14, 0.17, 1), "green": (0.08, 0.35, 0.15, 1), "white": (0.9, 0.9, 0.87, 1), "glass": (0.22, 0.45, 0.56, 1), "black": (0.035, 0.04, 0.05, 1), "red": (0.65, 0.06, 0.04, 1), "blue": (0.08, 0.22, 0.65, 1)}
FIELDS = {"id", "type", "dimensions", "position", "rotation", "material"}
def vector(value, n, low, high):
    if not isinstance(value, list) or len(value) != n or any(type(v) not in (int, float) or not math.isfinite(v) or not low <= v <= high for v in value):
        raise ValueError("Invalid numeric vector")
    return value

def validate(data):
    if not isinstance(data, dict) or set(data) != {"schemaVersion", "sceneName", "objects"} or data["schemaVersion"] != 2:
        raise ValueError("Invalid scene root or schema version")
    if not isinstance(data["sceneName"], str) or not 1 <= len(data["sceneName"]) <= 80:
        raise ValueError("Invalid scene name")
    objects = data["objects"]
    if not isinstance(objects, list) or not 1 <= len(objects) <= 40:
        raise ValueError("Scene must have 1–40 objects")
    seen = set()
    for obj in objects:
        if not isinstance(obj, dict) or set(obj) != FIELDS:
            raise ValueError("Invalid object fields")
        ident = obj["id"]
        if not isinstance(ident, str) or not re.fullmatch(r"[A-Za-z][A-Za-z0-9_-]{0,39}", ident) or ident in seen:
            raise ValueError("Invalid or duplicate object ID")
        seen.add(ident)
        if obj["type"] not in TYPES or obj["material"] not in COLORS:
            raise ValueError("Unsupported geometry or material")
        vector(obj["dimensions"], 3, 0.02, 15)
        vector(obj["position"], 3, -20, 20)
        vector(obj["rotation"], 3, -6.284, 6.284)
    return data

def load(path):
    with open(path, encoding="utf-8") as file:
        return validate(json.load(file))
