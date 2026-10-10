#!/usr/bin/env python3
"""
Future Stars Baseball Club - Hitting 2D Pose Measurement Prototype
=================================================================
Pose Tracking, 2D Telemetry Overlay & CSV Data Extraction
Pipeline: Google MediaPipe BlazePose + OpenCV

Usage:
------
1. Install requirements:
   pip install -r requirements.txt

2. Process a single video:
   python src/process_hitting_video.py --input "synthetic_demo_side_tee.mp4"

3. Process all videos in a directory (batch mode):
   python src/process_hitting_video.py --input_dir "./hitting_videos" --output_dir "./analyzed_output"

Features:
---------
- Uses MediaPipe Pose landmarks; this script measures x/y image-plane coordinates only
- Visualizes green skeleton lines and yellow joint landmarks on the original video (not anonymized)
- Per-frame HUD overlay:
    * L knee / R knee angles (Hip-Knee-Ankle 3-point angle)
    * L elbow / R elbow angles (Shoulder-Elbow-Wrist 3-point angle)
    * Shoulder line horizontal tilt angle (directed image-plane shoulder segment)
    * Hip line horizontal tilt angle (directed image-plane hip segment)
    * Torso lean vertical tilt angle (torso segment vs image vertical)
    * Top-right elapsed timestamp (t=00X.XXs)
- Requests an MP4 video using the mp4v codec (not guaranteed H.264)
- Exports exploratory 2D measurements to CSV; this is not validated biomechanics

Compatibility: this prototype requires the legacy mp.solutions.pose API.
The pinned legacy runtime was smoke-tested on synthetic input. See docs/limitations.md.
Do not publish input videos, annotated videos, or participant telemetry.
"""

import os
import sys
import math
import argparse
import numpy as np
import cv2
import pandas as pd

# Check MediaPipe availability
try:
    import mediapipe as mp
    MEDIAPIPE_AVAILABLE = True
except ImportError:
    MEDIAPIPE_AVAILABLE = False


def calculate_3point_angle(a, b, c):
    """
    Calculate the interior angle (in degrees) formed at vertex b by points a and c.
    Vector BA and Vector BC in 2D image coordinates.
    Returns angle in degrees [0, 180].
    """
    if a is None or b is None or c is None:
        return None
    
    ba = np.array([a[0] - b[0], a[1] - b[1]], dtype=np.float32)
    bc = np.array([c[0] - b[0], c[1] - b[1]], dtype=np.float32)
    
    norm_ba = np.linalg.norm(ba)
    norm_bc = np.linalg.norm(bc)
    if norm_ba < 1e-6 or norm_bc < 1e-6:
        return None
    
    cosine = np.dot(ba, bc) / (norm_ba * norm_bc)
    cosine = np.clip(cosine, -1.0, 1.0)
    angle = np.degrees(np.arccos(cosine))
    return float(angle)


def calculate_line_tilt_angle(p_lead, p_rear):
    """
    Calculate a directed segment bearing relative to image horizontal.
    The historical parameter names do not establish front/rear or lead/trail.
    Current calls pass anatomical left first and anatomical right second.
    atan2(-dy, dx) returns a bearing in [-180, 180] degrees from right to left.
    A horizontal segment can read 0 or +/-180 depending on its direction.
    Do not interpret the sign as a coaching or physical ground-plane measure.
    """
    if p_lead is None or p_rear is None:
        return None
    
    dx = p_lead[0] - p_rear[0]
    dy = p_lead[1] - p_rear[1]
    
    if abs(dx) < 1e-6 and abs(dy) < 1e-6:
        return None
    
    # In standard Cartesian coordinates (y upwards), tilt = arctan2(-dy, dx)
    angle = np.degrees(np.arctan2(-dy, dx))
    return float(angle)


def calculate_torso_lean_angle(mid_shoulder, mid_hip):
    """
    Calculate the midpoint torso segment bearing relative to image vertical.
    Camera roll is not calibrated; image vertical is not necessarily gravity.
    Vector from mid_hip to mid_shoulder.
    In image coordinates: dy = y_shoulder - y_hip (usually negative since shoulder is higher).
    Angle with vertical: arctan2(dx, -dy).
    """
    if mid_shoulder is None or mid_hip is None:
        return None
    
    dx = mid_shoulder[0] - mid_hip[0]
    dy = -(mid_shoulder[1] - mid_hip[1]) # convert so up is positive
    
    if abs(dx) < 1e-6 and abs(dy) < 1e-6:
        return None
    
    angle = np.degrees(np.arctan2(dx, dy))
    return float(angle)


# MediaPipe Pose Topology for Skeleton Visualization
SKELETON_CONNECTIONS = [
    # Head / Neck / Face
    (0, 1), (1, 2), (2, 3), (3, 7),
    (0, 4), (4, 5), (5, 6), (6, 8),
    (9, 10),
    # Torso
    (11, 12), # Shoulder line
    (11, 23), # Left side torso
    (12, 24), # Right side torso
    (23, 24), # Hip line
    # Arms
    (11, 13), (13, 15), # Left arm (Shoulder -> Elbow -> Wrist)
    (15, 17), (15, 19), (15, 21), (17, 19), # Left hand
    (12, 14), (14, 16), # Right arm
    (16, 18), (16, 20), (16, 22), (18, 20), # Right hand
    # Legs
    (23, 25), (25, 27), # Left leg (Hip -> Knee -> Ankle)
    (27, 29), (27, 31), (29, 31), # Left foot (Heel -> Toe)
    (24, 26), (26, 28), # Right leg
    (28, 30), (28, 32), (30, 32), # Right foot
]


def process_video(input_path, output_video_path, output_csv_path, min_detection_confidence=0.5, min_tracking_confidence=0.5):
    """
    Processes a single hitting video: extracts pose landmarks, computes angles,
    overlays telemetry HUD and skeleton, and saves video + CSV.
    """
    input_resolved = os.path.normcase(os.path.realpath(input_path))
    output_resolved = {
        os.path.normcase(os.path.realpath(output_video_path)),
        os.path.normcase(os.path.realpath(output_csv_path)),
    }
    if input_resolved in output_resolved or len(output_resolved) != 2:
        print("[ERROR] Input and output paths must be distinct; no files were opened.")
        return False

    if not MEDIAPIPE_AVAILABLE:
        print("[ERROR] MediaPipe is not installed in this Python environment.")
        print("Please run: pip install -r requirements.txt")
        return False

    if not hasattr(mp, "solutions") or not hasattr(mp.solutions, "pose"):
        print("[ERROR] This prototype needs the legacy mp.solutions.pose API.")
        print("Use the pinned requirements in a fresh Python 3.12 environment.")
        return False

    cap = cv2.VideoCapture(input_path)
    if not cap.isOpened():
        print(f"[ERROR] Could not open video file: {input_path}")
        cap.release()
        return False

    raw_width = cap.get(cv2.CAP_PROP_FRAME_WIDTH)
    raw_height = cap.get(cv2.CAP_PROP_FRAME_HEIGHT)
    fps = cap.get(cv2.CAP_PROP_FPS)
    frame_count = cap.get(cv2.CAP_PROP_FRAME_COUNT)
    total_frames = int(frame_count) if math.isfinite(frame_count) and frame_count > 0 else 0
    if (not math.isfinite(raw_width) or raw_width < 1 or
            not math.isfinite(raw_height) or raw_height < 1 or
            not math.isfinite(fps) or fps <= 0):
        print("[ERROR] Video dimensions or frame rate are invalid; timestamps would be unreliable.")
        cap.release()
        return False
    width, height = int(raw_width), int(raw_height)

    print(f"--> Input Video: {os.path.basename(input_path)}")
    print(f"    Resolution: {width}x{height} | FPS: {fps:.2f} | Frames: {total_frames}")

    # Set up video writer using mp4v; availability depends on the OpenCV build
    fourcc = cv2.VideoWriter_fourcc(*'mp4v')
    try:
        out = cv2.VideoWriter(output_video_path, fourcc, fps, (width, height))
    except Exception as exc:
        print(f"[ERROR] Could not initialize video writer: {exc}")
        cap.release()
        return False
    if not out.isOpened():
        print(f"[ERROR] Could not open video writer: {output_video_path}")
        cap.release()
        out.release()
        return False

    # Scale factors for drawing based on video resolution (normalized to 640x368 base)
    scale_factor = max(1.0, width / 640.0)
    line_thickness = max(2, int(2 * scale_factor))
    joint_radius = max(3, int(4 * scale_factor))
    hud_font_scale = 0.42 * scale_factor
    hud_font_thickness = max(1, int(1 * scale_factor))
    hud_line_height = int(15 * scale_factor)
    hud_top = int(10 * scale_factor)
    hud_left = int(10 * scale_factor)
    hud_width = int(215 * scale_factor)
    hud_height = int(138 * scale_factor)

    pose = None
    try:
        # Initialize MediaPipe Pose
        mp_pose = mp.solutions.pose
        pose = mp_pose.Pose(
            static_image_mode=False,
            model_complexity=2, # MediaPipe Heavy model; project-specific accuracy is unvalidated
            smooth_landmarks=True,
            min_detection_confidence=min_detection_confidence,
            min_tracking_confidence=min_tracking_confidence
        )

        telemetry_records = []
        frame_idx = 0

        print("--> Processing frames...")
        while True:
            ret, frame = cap.read()
            if not ret:
                break

            timestamp_sec = frame_idx / fps
            rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            results = pose.process(rgb_frame)

            angles = {
                "L_knee": None,
                "R_knee": None,
                "L_elbow": None,
                "R_elbow": None,
                "shoulder_line": None,
                "hip_line": None,
                "torso_lean": None
            }

            pts = {}
            if results.pose_landmarks:
                landmarks = results.pose_landmarks.landmark
                for idx, lm in enumerate(landmarks):
                    # Filter by visibility threshold
                    if lm.visibility >= 0.4:
                        px = int(lm.x * width)
                        py = int(lm.y * height)
                        pts[idx] = (px, py)

                # Draw skeleton connections (Green lines: (0, 255, 0))
                for p1_idx, p2_idx in SKELETON_CONNECTIONS:
                    if p1_idx in pts and p2_idx in pts:
                        cv2.line(frame, pts[p1_idx], pts[p2_idx], (0, 255, 0), line_thickness)

                # Draw joints (Yellow filled circles: (0, 255, 255))
                for idx in pts:
                    cv2.circle(frame, pts[idx], joint_radius, (0, 255, 255), -1)

                # Compute exploratory 2D image-plane angles
                # 1. L knee (Left Hip 23, Left Knee 25, Left Ankle 27)
                if 23 in pts and 25 in pts and 27 in pts:
                    angles["L_knee"] = calculate_3point_angle(pts[23], pts[25], pts[27])

                # 2. R knee (Right Hip 24, Right Knee 26, Right Ankle 28)
                if 24 in pts and 26 in pts and 28 in pts:
                    angles["R_knee"] = calculate_3point_angle(pts[24], pts[26], pts[28])

                # 3. L elbow (Left Shoulder 11, Left Elbow 13, Left Wrist 15)
                if 11 in pts and 13 in pts and 15 in pts:
                    angles["L_elbow"] = calculate_3point_angle(pts[11], pts[13], pts[15])

                # 4. R elbow (Right Shoulder 12, Right Elbow 14, Right Wrist 16)
                if 12 in pts and 14 in pts and 16 in pts:
                    angles["R_elbow"] = calculate_3point_angle(pts[12], pts[14], pts[16])

                # 5. Shoulder line tilt (Left Shoulder 11, Right Shoulder 12)
                if 11 in pts and 12 in pts:
                    angles["shoulder_line"] = calculate_line_tilt_angle(pts[11], pts[12])

                # 6. Hip line tilt (Left Hip 23, Right Hip 24)
                if 23 in pts and 24 in pts:
                    angles["hip_line"] = calculate_line_tilt_angle(pts[23], pts[24])

                # 7. Torso lean (Midpoint shoulders to midpoint hips)
                if 11 in pts and 12 in pts and 23 in pts and 24 in pts:
                    mid_sh = ((pts[11][0] + pts[12][0]) / 2.0, (pts[11][1] + pts[12][1]) / 2.0)
                    mid_hp = ((pts[23][0] + pts[24][0]) / 2.0, (pts[23][1] + pts[24][1]) / 2.0)
                    angles["torso_lean"] = calculate_torso_lean_angle(mid_sh, mid_hp)

            # -------------------------------------------------------------
            # Draw Telemetry HUD Overlay (Top-Left Black Rectangle)
            # -------------------------------------------------------------
            cv2.rectangle(
                frame,
                (hud_left, hud_top),
                (hud_left + hud_width, hud_top + hud_height),
                (0, 0, 0),
                -1
            )

            hud_labels = [
                ("L knee", angles["L_knee"]),
                ("R knee", angles["R_knee"]),
                ("L elbow", angles["L_elbow"]),
                ("R elbow", angles["R_elbow"]),
                ("Shoulder line", angles["shoulder_line"]),
                ("Hip line", angles["hip_line"]),
                ("Torso lean", angles["torso_lean"]),
            ]

            for i, (name, val) in enumerate(hud_labels):
                if val is not None and not math.isnan(val):
                    text_str = f"{name}: {val:5.1f} deg"
                else:
                    text_str = f"{name}:    --    "
            
                y_pos = hud_top + int((16 + i * 15) * scale_factor)
                x_pos = hud_left + int(6 * scale_factor)
            
                cv2.putText(
                    frame,
                    text_str,
                    (x_pos, y_pos),
                    cv2.FONT_HERSHEY_SIMPLEX,
                    hud_font_scale,
                    (255, 255, 255),
                    hud_font_thickness,
                    cv2.LINE_AA
                )

            # -------------------------------------------------------------
            # Draw Frame-Based Timestamp (Top-Right: t=00X.XXs)
            # -------------------------------------------------------------
            t_text = f"t={timestamp_sec:06.2f}s"
            t_x = width - int(105 * scale_factor)
            t_y = int(25 * scale_factor)
            cv2.putText(
                frame,
                t_text,
                (t_x, t_y),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.45 * scale_factor,
                (255, 255, 255),
                max(1, int(1 * scale_factor)),
                cv2.LINE_AA
            )

            # Record to telemetry table
            telemetry_records.append({
                "frame": frame_idx,
                "time_sec": round(timestamp_sec, 3),
                "L_knee_deg": round(angles["L_knee"], 2) if angles["L_knee"] is not None else np.nan,
                "R_knee_deg": round(angles["R_knee"], 2) if angles["R_knee"] is not None else np.nan,
                "L_elbow_deg": round(angles["L_elbow"], 2) if angles["L_elbow"] is not None else np.nan,
                "R_elbow_deg": round(angles["R_elbow"], 2) if angles["R_elbow"] is not None else np.nan,
                "shoulder_line_deg": round(angles["shoulder_line"], 2) if angles["shoulder_line"] is not None else np.nan,
                "hip_line_deg": round(angles["hip_line"], 2) if angles["hip_line"] is not None else np.nan,
                "torso_lean_deg": round(angles["torso_lean"], 2) if angles["torso_lean"] is not None else np.nan,
            })

            out.write(frame)
            frame_idx += 1

            if frame_idx % 100 == 0:
                if total_frames > 0:
                    print(f"    Processed {frame_idx}/{total_frames} frames ({frame_idx/total_frames*100:.1f}%)")
                else:
                    print(f"    Processed {frame_idx} frames (total unknown)")

    except Exception as exc:
        print(f"[ERROR] Processing failed: {exc}")
        return False
    finally:
        cap.release()
        out.release()
        if pose is not None:
            pose.close()

    if frame_idx == 0:
        print("[ERROR] No video frames were decoded.")
        return False

    # Save CSV
    try:
        df = pd.DataFrame(telemetry_records)
        df.to_csv(output_csv_path, index=False)
    except Exception as exc:
        print(f"[ERROR] Could not save telemetry CSV: {exc}")
        return False
    print(f"[SUCCESS] Processed {frame_idx} frames.")
    print(f"    Annotated Video: {output_video_path}")
    print(f"    2D telemetry CSV: {output_csv_path}")
    return True


def main():
    parser = argparse.ArgumentParser(description="Future Stars Baseball Hitting 2D Pose Measurement Prototype")
    inputs = parser.add_mutually_exclusive_group(required=True)
    inputs.add_argument("--input", "-i", type=str, help="Path to input video file (e.g. synthetic_demo_side_tee.mp4)")
    inputs.add_argument("--input_dir", "-d", type=str, help="Directory containing multiple hitting MP4 videos")
    parser.add_argument("--output_dir", "-o", type=str, default="./analyzed_output", help="Directory to save analyzed videos and CSVs")
    args = parser.parse_args()

    os.makedirs(args.output_dir, exist_ok=True)

    if args.input:
        video_files = [args.input]
    elif args.input_dir:
        if not os.path.isdir(args.input_dir):
            parser.error("--input_dir must be an existing directory")
        video_files = sorted(
            os.path.join(args.input_dir, f) for f in os.listdir(args.input_dir)
            if f.lower().endswith(('.mp4', '.mov', '.avi'))
        )
    if not video_files:
        parser.error("No supported input video files found")
    basenames = [os.path.splitext(os.path.basename(p))[0] for p in video_files]
    if len(set(basenames)) != len(basenames):
        parser.error("Input basenames collide; rename them to avoid overwriting outputs")

    input_paths = {os.path.normcase(os.path.realpath(p)) for p in video_files}
    output_paths = []
    for base_name in basenames:
        output_paths.extend([
            os.path.normcase(os.path.realpath(os.path.join(args.output_dir, f"{base_name}_analyzed.mp4"))),
            os.path.normcase(os.path.realpath(os.path.join(args.output_dir, f"{base_name}_telemetry.csv"))),
        ])
    if input_paths.intersection(output_paths):
        parser.error("An output path would overwrite an input; use a separate output directory")
    if len(set(output_paths)) != len(output_paths):
        parser.error("Output paths collide; use distinct destinations")

    print(f"=== Found {len(video_files)} video(s) to process ===")
    all_succeeded = True
    for v_path in video_files:
        base_name = os.path.splitext(os.path.basename(v_path))[0]
        out_v = os.path.join(args.output_dir, f"{base_name}_analyzed.mp4")
        out_csv = os.path.join(args.output_dir, f"{base_name}_telemetry.csv")
        succeeded = process_video(v_path, out_v, out_csv)
        all_succeeded = succeeded and all_succeeded
    return 0 if all_succeeded else 1


if __name__ == "__main__":
    sys.exit(main())
