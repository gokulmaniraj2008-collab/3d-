"""Validate user-editable bus settings without executing prompt text."""
import json
import os

DEFAULTS = {
    "body_color": [0.12, 0.34, 0.18],
    "roof_color": [0.83, 0.79, 0.63],
    "seat_color": [0.055, 0.15, 0.27],
    "seat_rows": 7,
    "roof_vents": 3,
    "destination": "TAMIL NADU",
    "preview_samples": 24,
}
def load_config(path=None):
    path = path or os.environ.get("BUS_CONFIG", os.path.join(os.path.dirname(__file__), "bus_config.json"))
    with open(path, encoding="utf-8") as handle:
        supplied = json.load(handle)
    if not isinstance(supplied, dict):
        raise ValueError("Bus config must be a JSON object")
    unknown = set(supplied) - set(DEFAULTS)
    if unknown:
        raise ValueError("Unknown bus config keys: " + ", ".join(sorted(unknown)))
    config = dict(DEFAULTS)
    config.update(supplied)
    for key in ("body_color", "roof_color", "seat_color"):
        value = config[key]
        if not isinstance(value, list) or len(value) != 3 or any(type(v) not in (int, float) or not 0 <= v <= 1 for v in value):
            raise ValueError(key + " must be three RGB numbers from 0 to 1")
    for key, low, high in (("seat_rows", 1, 7), ("roof_vents", 0, 3), ("preview_samples", 8, 64)):
        value = config[key]
        if type(value) is not int or not low <= value <= high:
            raise ValueError("%s must be an integer from %s to %s" % (key, low, high))
    if not isinstance(config["destination"], str) or not 1 <= len(config["destination"]) <= 40 or any(ord(c) < 32 for c in config["destination"]):
        raise ValueError("destination must be 1-40 printable characters")
    return config
