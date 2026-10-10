# Movement Measurement Method

## Current state

MediaPipe Pose provides body landmarks. The current project code converts selected image-plane landmark coordinates into simple 2D measurements.

Current outputs include:
- Left / right knee angle
- Left / right elbow angle
- Shoulder-line tilt
- Hip-line tilt
- Torso lean
- Frame index / timestamp

## Important limitation

These are **2D video-derived measurements**. They are not validated 3D joint kinematics, ground-reaction forces, joint torques, or energy-transfer measurements.

## Planned additions
- Event labels: Stance, Load, Foot Plant, Launch, Contact, Extension, Finish
- Stride direction
- Head / hip drift
- Selected hand or bat-path proxies
- Swing-to-swing repeatability metrics
- Explicit landmark confidence / missing-data reason flags

## Implemented conventions

The code converts normalized landmark x/y coordinates to integer pixels before measuring. Pixel rounding, perspective, camera roll, occlusion, and detector error affect the result. No metric calibration or 3D reconstruction is performed.

Knee and elbow values are interior three-point angles from 0 to 180 degrees. Shoulder and hip values are directed right-to-left segment bearings from -180 to 180 degrees, computed with `atan2(-dy, dx)` on anatomical left/right landmarks. They are not normalized small-angle tilts; reversing the image direction can produce a value near 180 degrees for a horizontal segment. Anatomical left/right is not automatically lead/trail. Compare only with a consistent camera and orientation, and do not average wrapped bearings as ordinary numbers.

Torso lean is the shoulder-midpoint to hip-midpoint segment relative to image vertical. Positive values lean toward image right. Image vertical is not calibrated gravity.

Landmarks below visibility 0.4 are omitted. A metric whose required landmarks are absent is exported as an empty CSV value. This heuristic is not a validated confidence estimate. The CSV does not retain landmark confidence or distinguish why a value is missing.

Frame numbers are zero-based. Time is frame index divided by the reported frame rate, rounded to three decimals; it is not a source presentation timestamp. Variable-frame-rate video and inaccurate frame-rate metadata can break timing assumptions. See [the output schema](telemetry_schema.md).
