# Known Limitations

Current limitations include:
- 2D perspective / foreshortening
- Camera placement sensitivity
- Landmark occlusion by the bat or body
- Pose-detection errors during fast motion
- Youth body-size and maturity differences
- Small sample size
- Subjective elements in the six-category rubric
- No direct causal proof that one drill caused one observed improvement
- Reference ranges are not universal youth standards

We will update this file as new failure cases appear.

## Runtime and implementation limitations

- The script calls the legacy `mp.solutions.pose` API. MediaPipe maintainers confirm that current packages removed the Solutions API and recommend migration to Tasks: https://github.com/google-ai-edge/mediapipe/issues/6200.
- MediaPipe v0.10.21's official build source exports `solutions`, and its published wheels target Python 3.9-3.12. The release smoke test uses Python 3.12; compatibility with other interpreters/platforms has not been checked: https://github.com/google-ai-edge/mediapipe/blob/v0.10.21/setup.py and https://pypi.org/project/mediapipe/0.10.21/.
- Direct dependencies are pinned to the versions observed in the release smoke test. The full observed Linux/Python 3.12 environment is recorded in requirements-lock-py312-linux.txt. Colab execution and other platforms have not been verified; Colab may not offer a compatible Python version.
- The writer requests `mp4v`, not H.264. Startup is checked and the synthetic smoke output was decoded, but runtime encoding errors on other systems still need investigation; do not rely only on a printed success message.
- Release guards reject invalid frame rates/dimensions, zero decoded frames, writer failures, colliding batch basenames, and any output path overlapping an input; known per-video failures produce a nonzero exit status. Decoder end-of-file cannot reliably be distinguished from a mid-stream decode failure, and outputs from failed runs may be partial. Re-running the same basename can overwrite prior outputs; choose a new private output directory for each run.
- Coordinate rounding occurs before geometry. Line bearings depend on anatomical left/right ordering and wrap at +/-180 degrees; they are not camera-independent shoulder or hip tilt. See measurement_method.md.
- There is no automatic event detection, multi-view synchronization/fusion, six-category scoring, AI report service, or retest evaluation in the included script. Those belong to the described review method or future work.
- No accuracy, measurement-reliability, camera-repeatability, or coaching-outcome validation was run for this release. Passing software checks does not validate measurements or coaching recommendations.

See release_checks.md for the narrow software checks actually performed. The real detector was exercised on a non-person clip, so that smoke test covers the missing-pose path, not successful landmark detection on a swing.
