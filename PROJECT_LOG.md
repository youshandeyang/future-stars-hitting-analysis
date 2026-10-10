# Project Log

This file is intentionally simple. Vincent can update it weekly.

## 2026-10 - Phase II prototype
- Added pose tracking and frame-by-frame 2D telemetry.
- Compared Side/Back and Tee/Toss views.
- Back view helped reveal stride direction and wrapping patterns that were harder to judge from the side.
- AI-generated reports were useful for organizing evidence, but some explanations sounded more certain than the data justified.

### Next tests
- Add event labels.
- Test camera-angle sensitivity.
- Decide which measurements are reliable enough to keep.
- Re-run several existing retest players through the new pipeline.

## 2026-10-10 - Public-release preparation
- Removed individual participant examples and identifying example filenames from public-facing files.
- Corrected notebook/script claims to 2D image-plane measurements and fixed the notebook script path.
- Documented actual CSV columns, the separate synthetic review example, angle conventions, and incomplete features.
- Pinned an observed legacy runtime and added basic input/output failure guards without changing the geometry formulas.
- Added synthetic geometry and mocked-pipeline tests; ran a non-person real-model smoke test. See docs/release_checks.md for scope and limits.
- Retained the original coaching/retest goals; no measurement or coaching validation was claimed.

## 2026-10-10 - Phase I practical output added
- Added the family recording guide and AI report rules as an editable two-page document and readable repository page.
- Aligned the one-page checklists and standard recording protocol to 8-10 baseline/retest swings, with review of 5-10 swings.
- Used the full category label "Barrel Path & Through-Zone Extension" from the guide.
- Kept project-reported participation separate from verified artifact contents. The guide contains a method and reporting rules, not participant scores or a measured-outcomes study.
