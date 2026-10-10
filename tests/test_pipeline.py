"""Synthetic I/O checks with mocked pose landmarks; no real youth data or network.

These test pipeline behavior, not MediaPipe detection quality or biomechanics.
Requires the pinned project dependencies. Run from the repository root with:
    python -m unittest discover -s tests -v
"""
import contextlib
import importlib.util
import io
from pathlib import Path
import tempfile
import sys
from types import SimpleNamespace
import unittest
from unittest import mock

import cv2
import numpy as np
import pandas as pd

SOURCE = Path(__file__).resolve().parents[1] / 'src' / 'process_hitting_video.py'
spec = importlib.util.spec_from_file_location('hitting_pipeline', SOURCE)
pipeline = importlib.util.module_from_spec(spec)
spec.loader.exec_module(pipeline)


class SyntheticPose:
    def __init__(self, **kwargs):
        pass

    def process(self, rgb_frame):
        points = [SimpleNamespace(x=0.5, y=0.5, visibility=1.0) for _ in range(33)]
        for index, xy in {11:(0.4,0.2), 12:(0.6,0.2), 13:(0.3,0.3), 14:(0.7,0.3),
                          15:(0.2,0.2),16:(0.8,0.2),23:(0.4,0.5),24:(0.6,0.5),
                          25:(0.4,0.7),26:(0.6,0.7),27:(0.2,0.7),28:(0.8,0.7)}.items():
            points[index].x, points[index].y = xy
        return SimpleNamespace(pose_landmarks=SimpleNamespace(landmark=points))

    def close(self):
        pass


class PipelineTests(unittest.TestCase):
    def setUp(self):
        self.directory = tempfile.TemporaryDirectory()
        self.root = Path(self.directory.name)
        self.input = self.root / 'synthetic.mp4'
        writer = cv2.VideoWriter(str(self.input), cv2.VideoWriter_fourcc(*'mp4v'), 30, (320,240))
        self.assertTrue(writer.isOpened())
        for _ in range(4):
            writer.write(np.full((240,320,3),64,dtype=np.uint8))
        writer.release()
        self.video = self.root / 'annotated.mp4'
        self.csv = self.root / 'telemetry.csv'

    def tearDown(self):
        self.directory.cleanup()

    def run_pipeline(self, input_path=None):
        with contextlib.redirect_stdout(io.StringIO()):
            return pipeline.process_video(str(input_path or self.input), str(self.video), str(self.csv))

    def test_mocked_pose_exports_geometry_and_decodable_video(self):
        with mock.patch.object(pipeline.mp.solutions.pose, 'Pose', SyntheticPose):
            self.assertTrue(self.run_pipeline())
        df = pd.read_csv(self.csv)
        self.assertEqual(df['frame'].tolist(), [0,1,2,3])
        self.assertEqual(df['time_sec'].tolist(), [0.0,0.033,0.067,0.1])
        self.assertTrue(np.allclose(df['L_knee_deg'],90.0))
        self.assertTrue(np.allclose(df['R_knee_deg'],90.0))
        self.assertTrue(np.allclose(abs(df['shoulder_line_deg']),180.0))
        self.assertTrue(np.allclose(df['torso_lean_deg'],0.0))
        cap = cv2.VideoCapture(str(self.video))
        frames = 0
        while cap.read()[0]:
            frames += 1
        cap.release()
        self.assertEqual(frames,4)

    def test_missing_input_fails(self):
        self.assertFalse(self.run_pipeline(self.root/'not_present.mp4'))
        self.assertFalse(self.csv.exists())

    def test_writer_open_failure_is_reported(self):
        writer = mock.Mock()
        writer.isOpened.return_value = False
        with mock.patch.object(pipeline.cv2,'VideoWriter',return_value=writer):
            self.assertFalse(self.run_pipeline())
        writer.release.assert_called_once()

    def test_invalid_frame_rate_is_rejected(self):
        cap = mock.Mock()
        cap.isOpened.return_value = True
        cap.get.side_effect = lambda prop: {
            cv2.CAP_PROP_FRAME_WIDTH:320,cv2.CAP_PROP_FRAME_HEIGHT:240,
            cv2.CAP_PROP_FPS:float('nan'),cv2.CAP_PROP_FRAME_COUNT:4
        }[prop]
        with mock.patch.object(pipeline.cv2,'VideoCapture',return_value=cap):
            self.assertFalse(self.run_pipeline())
        cap.release.assert_called_once()

    def test_nonfinite_dimensions_are_rejected(self):
        cap = mock.Mock()
        cap.isOpened.return_value = True
        cap.get.side_effect = lambda prop: {
            cv2.CAP_PROP_FRAME_WIDTH:float('nan'),cv2.CAP_PROP_FRAME_HEIGHT:240,
            cv2.CAP_PROP_FPS:30,cv2.CAP_PROP_FRAME_COUNT:4
        }[prop]
        with mock.patch.object(pipeline.cv2,'VideoCapture',return_value=cap):
            self.assertFalse(self.run_pipeline())
        cap.release.assert_called_once()

    def test_csv_failure_is_reported(self):
        with mock.patch.object(pipeline.mp.solutions.pose, 'Pose', SyntheticPose):
            with mock.patch.object(pipeline.pd.DataFrame,'to_csv',side_effect=OSError('synthetic write failure')):
                self.assertFalse(self.run_pipeline())
        self.assertFalse(self.csv.exists())

    def test_direct_input_output_collision_preserves_input(self):
        before = self.input.read_bytes()
        with contextlib.redirect_stdout(io.StringIO()):
            result = pipeline.process_video(str(self.input), str(self.input), str(self.csv))
        self.assertFalse(result)
        self.assertEqual(self.input.read_bytes(), before)

    def test_batch_input_output_collision_preserves_inputs(self):
        second_input = self.root / 'synthetic_analyzed.mp4'
        second_input.write_bytes(self.input.read_bytes())
        before = {p:p.read_bytes() for p in (self.input, second_input)}
        with mock.patch.object(sys, 'argv', ['process_hitting_video.py', '--input_dir', str(self.root), '--output_dir', str(self.root)]):
            with contextlib.redirect_stderr(io.StringIO()):
                with self.assertRaises(SystemExit) as error:
                    pipeline.main()
        self.assertEqual(error.exception.code,2)
        self.assertEqual({p:p.read_bytes() for p in before},before)

    def test_pose_initialization_failure_is_reported(self):
        with mock.patch.object(pipeline.mp.solutions.pose,'Pose',side_effect=RuntimeError('synthetic initialization failure')):
            self.assertFalse(self.run_pipeline())
        self.assertFalse(self.csv.exists())


if __name__ == '__main__':
    unittest.main()
