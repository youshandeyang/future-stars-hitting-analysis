# Future Stars Youth Hitting Analysis

A student-led, low-cost project exploring how ordinary home video can help young baseball players understand and improve their swings.

**Project lead:** Vincent Hall, founder of Future Stars Baseball Club

## Start here for families

Start with the one-page, no-code family guide. A phone, a safe practice space, and an adult are enough for the basic record-and-retest loop; the Python prototype is optional.

- [English checklist](docs/family_swing_checklist.md) | [Print the one-page English PDF](docs/Future_Stars_Family_Swing_Checklist_EN.pdf)

The guide covers safe camera placement, tee or adult toss, choosing one cue, repeatable retesting, and optional AI assistance with a person reviewing the evidence.

## Why this project exists

Future Stars began with a practical coaching problem: young players are often told what to change, but it is hard for them to see whether the movement actually changed. We started with simple video review and retesting. Phase II now explores whether ordinary Side/Back, Tee/Toss video can also produce simple, repeatable movement measurements.

The goal is not to build a "perfect swing" model. The goal is to create a method that is affordable, understandable, repeatable, and honest about its limits.

## What we have done so far

### Phase I - video coaching + retest
- Project-reported participation: 12 youth players.
- Project-reported follow-up: 7 completed at least one retest.
- We used a six-category scoring rubric.
- Players received one or two practice priorities, then recorded again later.

### Phase I practical output: Family Guide & AI Report Rules


Phase I produced a reusable family recording workflow and rules for evidence-based AI report drafts. Read [the full family guide and AI report rules](docs/phase_i_family_guide.md), or download [the editable two-page Word guide](docs/Future_Stars_Family_Guide_AI_Report_Rules_EN.docx). Use it alongside the [current safety and privacy checklist](docs/family_swing_checklist.md).

The protocol uses 8-10 swings at baseline and retest, one safe fixed side view as the minimum, optional additional views, one or two practice targets, and consistent retesting. Its report rules require traceable evidence, the same scoring rubric, clear uncertainty, and human review.

This is a practical methods output. The guide contains no participant scores or measured improvement estimates; it does not independently verify the project-reported 12 participants and 7 retests. Individual participant records are not included in this public starter.

### Phase II - movement data from ordinary video
Current prototype:
1. MediaPipe Pose detects body landmarks.
2. Project code calculates selected **2D** movement measurements.
3. Annotated video + synchronized CSV telemetry are exported.
4. Side/Back and Tee/Toss views are compared.
5. AI may help organize evidence and draft a report.
6. Vincent reviews the evidence and selects one or two training priorities.
7. The player practices and retests.

## Simple project loop

**Record the Swing -> Watch & Compare -> Pick One Thing -> Practice a Change -> Record Again -> See What Changed**

## Important honesty about the current system

- MediaPipe is an off-the-shelf pose detector. We did not train it.
- Current joint/tilt values are 2D image-based measurements, not lab-grade 3D biomechanics.
- Reference ranges are context, not universal youth standards.
- AI-generated explanations are hypotheses unless they are directly supported by video/data.
- This public release contains no participant media or individual participant results. Its data example is synthetic.
- "Not enough information" is an acceptable result.

## Prototype status and local use

This is the original V3 prototype with limited public-release corrections. It is not a validated model. The four-view comparison, six-category rubric, AI draft review, and retest loop are a human-guided method; the script does not automate those steps.

**Legacy runtime:** the script uses `mp.solutions.pose`, which current MediaPipe packages no longer expose. This starter pins MediaPipe 0.10.21 and the direct dependencies used in a Python 3.12.14 Linux smoke test. It remains a legacy prototype. See [limitations](docs/limitations.md) and [release checks](docs/release_checks.md).

Use Python 3.12 in a fresh virtual environment. From the repository root:

```sh
python3.12 -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.txt
python src/process_hitting_video.py --input path/to/your_video.mp4 --output_dir ./analyzed_output
```

On Windows, activate with `.venv\Scripts\activate` instead. MediaPipe may download its Heavy pose model on first use; model weights are not included in this repository. The notebook does not automatically fetch the repository into Colab.

The script writes annotated video and frame-level CSV files. These outputs retain participant information and must stay private. The annotated video is not anonymized by adding a skeleton overlay. No public example video is included.

For a data-only example, inspect [the synthetic CSV](data/sample_telemetry.csv). Its event labels and identifiers illustrate a proposed review schema; they are not emitted by the current script. See [telemetry schema](docs/telemetry_schema.md).

## Repository map

```text
docs/
  recording_protocol.md
  measurement_method.md
  scoring_rubric.md
  ai_assisted_analysis.md
  limitations.md
  research_questions.md
  privacy_and_youth_data.md
src/
  process_hitting_video.py
notebooks/
  demo_pipeline.ipynb
data/
  sample_telemetry.csv
examples/
  README.md
PROJECT_LOG.md
CONTRIBUTING.md
DATA_POLICY.md
LICENSE
```

## What we are working on next

- Event labels: Stance, Load, Foot Plant, Launch, Contact, Extension, Finish
- Camera-placement error testing
- Measurement repeatability
- Occlusion / missing-landmark handling
- Multi-view comparison rules
- Retest-based evaluation of practice changes

## Open questions

We do not have final answers yet. That is part of the project.

See [docs/research_questions.md](docs/research_questions.md).

## Contributing

We welcome practical criticism and reproducible suggestions. Please open an Issue if you have ideas about camera setup, measurement error, event definitions, youth-friendly reporting, or how to test whether a training change actually helped.

## Software checks

Run `python -m unittest discover -s tests -v` after installing the pinned requirements. The tests use synthetic geometry and mocked pose landmarks; they do not validate youth swing measurements or coaching outcomes.

## License and dependencies

The project source and documentation carry the included MIT license. Dependencies and separately downloaded model weights retain their own upstream licenses and terms; see [dependency notes](docs/dependencies.md). This repository grants no rights to participant data or third-party media.
