import copy
import json
import pathlib
import sys
import unittest
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1]))
from scene import validate

FIXTURE = json.loads((pathlib.Path(__file__).resolve().parents[1] / "examples/study-table.json").read_text())
class SceneTests(unittest.TestCase):
    def test_valid(self):
        self.assertEqual(len(validate(FIXTURE)["objects"]), 5)
    def test_reject_code(self):
        bad = copy.deepcopy(FIXTURE)
        bad["objects"][0]["script"] = "print('unsafe')"
        with self.assertRaises(ValueError): validate(bad)
    def test_reject_duplicate(self):
        bad = copy.deepcopy(FIXTURE)
        bad["objects"][1]["id"] = "top"
        with self.assertRaises(ValueError): validate(bad)
    def test_reject_nonfinite(self):
        bad = copy.deepcopy(FIXTURE)
        bad["objects"][0]["position"][0] = float("nan")
        with self.assertRaises(ValueError): validate(bad)
    def test_reject_too_many(self):
        bad = copy.deepcopy(FIXTURE)
        bad["objects"] *= 9
        with self.assertRaises(ValueError): validate(bad)
if __name__ == "__main__":
    unittest.main()
