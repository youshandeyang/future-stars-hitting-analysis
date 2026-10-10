# V3 Release Preparation Checks

Checked on 2026-10-10 in an isolated Linux x86-64 environment using Python 3.12.14. These checks assess software behavior, not measurement validity or coaching effectiveness.

## Passed

- Parsed the Python source and notebook structure; notebook execution counts and outputs are empty.
- Ten geometry unit tests using synthetic points: interior angles, missing/degenerate points, directed bearing wrap, image-relative torso lean, translation, and uniform scale.
- Nine pipeline tests using generated blank videos and mocked landmarks: CSV/video export, expected angle values, missing input, writer failure, invalid frame rate/dimensions, CSV failure, pose initialization failure, and direct/batch input-output collisions (some checks share a test).
- Real MediaPipe Heavy model smoke test on a generated 12-frame clip containing only a moving circle. Output decoded to 12 frames; CSV had 12 rows with matching frame/time sequence and empty angle values, as expected without a person. No youth or other personal media was used.
- `pip check` reported no broken requirements.

## Environment

Direct dependencies tested: MediaPipe 0.10.21, opencv-contrib-python 4.11.0.86 (cv2 4.11.0), NumPy 1.26.4, and pandas 3.0.6. The complete observed package set is recorded in requirements-lock-py312-linux.txt. The runtime obtains model weights separately; the repository does not redistribute them.

## Not established

Successful pose detection on real swings; landmark or angle accuracy; agreement with physical measurements; camera repeatability; event-label reliability; validity of the six-category rubric; coaching benefit; causal attribution; other operating systems/interpreters; or end-to-end execution in Colab.

The public CSV is synthetic illustration data, not a result of the smoke test or participant research. Passing these checks does not turn the prototype into a validated model.
