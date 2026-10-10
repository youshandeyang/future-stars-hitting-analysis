"""Geometry-only checks using synthetic points; no video, model, or network.

Load only the three reviewed geometry functions so these tests require NumPy,
but do not import or initialize MediaPipe, OpenCV, or pandas.
"""
import ast
from pathlib import Path
import unittest
import numpy as np

SOURCE = Path(__file__).resolve().parents[1] / 'src' / 'process_hitting_video.py'
FUNCTION_NAMES = {
    'calculate_3point_angle',
    'calculate_line_tilt_angle',
    'calculate_torso_lean_angle',
}
tree = ast.parse(SOURCE.read_text())
functions = [n for n in tree.body if isinstance(n, ast.FunctionDef) and n.name in FUNCTION_NAMES]
assert {n.name for n in functions} == FUNCTION_NAMES
namespace = {'np': np}
exec(compile(ast.Module(body=functions, type_ignores=[]), str(SOURCE), 'exec'), namespace)
angle = namespace['calculate_3point_angle']
bearing = namespace['calculate_line_tilt_angle']
lean = namespace['calculate_torso_lean_angle']


class GeometryTests(unittest.TestCase):
    def test_right_angle(self):
        self.assertAlmostEqual(angle((1, 0), (0, 0), (0, 1)), 90.0, places=5)

    def test_straight_angle(self):
        self.assertAlmostEqual(angle((-1, 0), (0, 0), (1, 0)), 180.0, places=5)

    def test_zero_angle(self):
        self.assertAlmostEqual(angle((1, 0), (0, 0), (2, 0)), 0.0, places=5)

    def test_missing_points(self):
        self.assertIsNone(angle(None, (0, 0), (1, 0)))
        self.assertIsNone(bearing(None, (0, 0)))
        self.assertIsNone(lean((0, 0), None))

    def test_degenerate_points(self):
        self.assertIsNone(angle((0, 0), (0, 0), (1, 0)))
        self.assertIsNone(bearing((0, 0), (0, 0)))
        self.assertIsNone(lean((0, 0), (0, 0)))

    def test_directed_horizontal_bearings(self):
        self.assertAlmostEqual(bearing((1, 0), (0, 0)), 0.0)
        self.assertAlmostEqual(abs(bearing((0, 0), (1, 0))), 180.0)

    def test_directed_vertical_bearings(self):
        self.assertAlmostEqual(bearing((0, -1), (0, 0)), 90.0)
        self.assertAlmostEqual(bearing((0, 1), (0, 0)), -90.0)

    def test_upright_torso(self):
        self.assertAlmostEqual(lean((0, 0), (0, 1)), 0.0)

    def test_lean_sign_is_image_direction(self):
        self.assertAlmostEqual(lean((1, 0), (0, 1)), 45.0)
        self.assertAlmostEqual(lean((-1, 0), (0, 1)), -45.0)

    def test_translation_and_uniform_scale(self):
        self.assertAlmostEqual(angle((10, 20), (10, 10), (20, 10)), 90.0, places=5)
        self.assertAlmostEqual(lean((12, 8), (10, 10)), 45.0)


if __name__ == '__main__':
    unittest.main()
