"""Optional free-tier hosted model adapter. Never runs AI-generated Python."""
import argparse
import json
import os
import pathlib
import sys
import urllib.error
import urllib.request
from scene import validate

INSTRUCTION = """You are a procedural Blender scene planner. Return ONLY a JSON object, no markdown.
Exact root keys: schemaVersion (integer 2), sceneName (string), objects (array).
Each object must have exactly id, type, dimensions, position, rotation, material.
type is one of box,cylinder,sphere,plane. dimensions and position are arrays of 3 numbers in meters; rotation is 3 radians.
Materials: wood,metal,green,white,glass,black,red,blue. Create 1 to 40 simple geometric objects.
Use positive dimensions between 0.02 and 15, positions between -20 and 20. Unique short ASCII IDs.
Build a recognizable but simplified object. No code, scripts, URLs, external assets, or extra fields.
"""
def generate(prompt, model, key):
    if not key:
        raise ValueError("GEMINI_API_KEY missing; use the example fixture workflow mode")
    if not 3 <= len(prompt.strip()) <= 500:
        raise ValueError("Prompt must be 3–500 characters")
    if not model or not all(c.isalnum() or c in "-_." for c in model):
        raise ValueError("Invalid model identifier")
    url = "https://generativelanguage.googleapis.com/v1beta/models/" + model + ":generateContent"
    payload = {"system_instruction": {"parts": [{"text": INSTRUCTION}]}, "contents": [{"parts": [{"text": prompt}]}], "generationConfig": {"responseMimeType": "application/json", "temperature": 0.2}}
    request = urllib.request.Request(url, data=json.dumps(payload).encode(), headers={"Content-Type": "application/json", "x-goog-api-key": key}, method="POST")
    try:
        with urllib.request.urlopen(request, timeout=35) as response:
            raw = response.read(200000)
    except urllib.error.HTTPError as exc:
        raise RuntimeError("Hosted model request failed (HTTP %s). Check key, model and free-tier quota." % exc.code) from None
    data = json.loads(raw)
    text = data["candidates"][0]["content"]["parts"][0]["text"]
    return validate(json.loads(text))

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--prompt", required=True)
    parser.add_argument("--output", required=True)
    args = parser.parse_args()
    scene = generate(args.prompt, os.getenv("GEMINI_MODEL", "gemini-2.5-flash"), os.getenv("GEMINI_API_KEY", ""))
    pathlib.Path(args.output).parent.mkdir(parents=True, exist_ok=True)
    pathlib.Path(args.output).write_text(json.dumps(scene, indent=2), encoding="utf-8")
    print("Validated scene saved; objects:", len(scene["objects"]))

if __name__ == "__main__":
    main()
