# Telemetry Schema

## Current script output

Each decoded frame contributes one CSV row. Columns, in order:

- `frame`: zero-based frame index
- `time_sec`: frame / reported FPS, rounded to 3 decimals
- `L_knee_deg`, `R_knee_deg`: left/right hip-knee-ankle interior angles
- `L_elbow_deg`, `R_elbow_deg`: left/right shoulder-elbow-wrist interior angles
- `shoulder_line_deg`, `hip_line_deg`: directed right-to-left image bearings
- `torso_lean_deg`: torso segment bearing relative to image vertical

Angles are in degrees and rounded to 2 decimals. Missing angles are empty CSV values, never a meaningful zero. See measurement_method.md for formulas, camera conventions, and limits. The current output does not include per-landmark visibility, event labels, swing IDs, or view/mode metadata. Filenames are inherited from inputs and can identify participants.

## Synthetic review example

`data/sample_telemetry.csv` contains two synthetic demonstration rows, not real anonymized player records and not measurements produced by an included video. `P001` and `S001` are example tokens, not a lookup to a participant. Its values and labels cannot be used as evidence of improvement or measurement accuracy.

The example illustrates additional manually reviewed fields: `player_id`, `session_id`, `view`, `mode`, `swing_id`, `event`, and `notes`. Its `left_knee_deg`, `right_knee_deg`, `left_elbow_deg`, and `right_elbow_deg` correspond conceptually to current `L_knee_deg`, `R_knee_deg`, `L_elbow_deg`, and `R_elbow_deg` fields but are not identical column names. An event-enrichment/export conversion is not implemented.

Do not publish real individual telemetry by simply replacing names with IDs. Motion patterns, timestamps, filenames, source frames, linked videos, and contextual notes can allow reidentification. Public examples in this release are synthetic only.
