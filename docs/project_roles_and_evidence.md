# Project Roles, AI Assistance, and Evidence

This page explains **who did what**, **which artifacts support which statements**, and **what remains unproven**. It is intended to help families, reviewers and contributors evaluate the project without mistaking AI-assisted code generation for independent student programming or coaching reports for validated biomechanics.

## Problem and design goal

Vincent described a young hitter who corrected his stance while being coached, then returned to the same mistake on the next swing. The question that grew from that experience was practical: could a player **see** a repeated movement, work on one small adjustment, and check the change later?

The project therefore explores an affordable workflow that a family could try using a phone or simple camera and a safe practice space. Accessibility is a **design goal**, not evidence that the approach works reliably for every household or player.

## Roles and attribution

| Part of the work | Responsible people or tools | What the claim does **not** mean |
| --- | --- | --- |
| Coaching problem and practical goals | Vincent, drawing on years of baseball and youth coaching | Not a claim of independent software engineering |
| Recording, equipment, scheduling and organization | Vincent with family support, including his father | Not entirely a solo project |
| Practice cues and video-based coaching observations | Vincent where supported by his coach notes; reviewed reports may involve AI drafting | Not a physics-lab measurement or fully automated decision |
| Python implementation, code revisions and technical-document drafts | AI/Agent tools used with human prompts, direction and review | Vincent does **not** claim he learned to write or debug this Python code independently |
| Body landmark estimation | Pre-existing MediaPipe Pose model, used through the Python script | No proprietary model was trained |
| Selected 2D video measurements and CSV export | Experimental public Python V3 code | No automatic 3D reconstruction, synchronized multi-view tracking, swing-event recognition, six-category coaching score, or validated outcomes |
| Separately developed local coaching application | A different AI-assisted implementation and testing workflow | Its features must not be attributed to this public repository |

**Vincent's stated engineering interest is the problem/system design:** how to make a tool useful, inexpensive, understandable, and revisable from real practice feedback. AI assistance is disclosed; it does not erase his real coaching contribution or transfer AI code authorship to him.

## Evidence inventory

| Artifact | Supports | Does not establish |
| --- | --- | --- |
| [Phase I family guide](phase_i_family_guide.md) | An actual recording, review, drill and retest method | Validated improvement rates or universal clinical/biomechanics standards |
| [Public Python source](../src/process_hitting_video.py) and [measurement method](measurement_method.md) | An implemented exploratory 2D image-plane telemetry pipeline | Accuracy on real swings, reliable 3D biomechanics or automatic coaching scores |
| [Release checks](release_checks.md) | Synthetic geometry tests, mocked pipeline tests and a non-person model smoke check | Successful validated detection and measurement on a real youth swing |
| [Leo demonstration](../examples/leo-coaching-demo/README.md) | Authorized recorded coaching case, source notes and a retrospective six-category score comparison | Reproduced run of the public Python script, objective performance gain, or causation from drills |
| [Project log](../PROJECT_LOG.md) | A chronology of recorded documentation/technical milestones and forthcoming questions | Proof that Vincent wrote each code commit |
| [Data policy](../DATA_POLICY.md) | Privacy and release controls, including the limited Leo case permission | General permission to publish any child participant's media |

## Leo case: interpret the numbers correctly

- The August 12, 2026 baseline's six-category ratings were assigned **retrospectively** using the same rubric as the September 26 review.
- The reported totals were **34/60 at baseline** and **38/60 at retest**. These are human-reviewed coaching ratings with AI-assisted drafting in the broader process, not calibrated physical measurement or automatic output from the public Python script.
- Baseline contact-quality score (CQS) was a **video-observation score of 80/100**. A comparable September CQS was **not assigned**, so do not claim improved CQS.
- The selected Side Tee footage is a representative excerpt; the underlying reports consider additional views and attempts. The clips are not perfectly synchronized trials.
- An archived skeleton/angle video appears in the demo. Its exact generating software version and measurement accuracy have not been independently reproduced from the currently published code.

## Truthful statements and statements to avoid

**Supported descriptions**
- “Vincent initiated and guides a low-cost, video-based baseball coaching project with family and AI/Agent assistance.”
- “AI tools and agents helped implement the code and draft parts of the technical material and reports.”
- “The open Python prototype explores selected 2D pose-based measurements.”
- “The Leo coaching case documents observations and a retest using a six-category human-reviewed rubric.”

**Unsupported descriptions**
- “Vincent independently coded the AI application” or “trained his own AI model.”
- “The GitHub software automatically assigns six reliable biomechanical swing scores.”
- “The 34-to-38 increase proves that the AI improved swing power, bat speed or contact quality.”
- “All 40–50 participants at a Future Stars camp completed video analysis and retests.”
- “The software is ready for unsupervised public deployment or verified accurate on children.”

## Student review still needed

The following are **open questions**. They are not evidence of completed work, and should only be filled after Vincent reviews his own records.

1. **Design decision:** Which real camera setup, workflow or accessibility decision did Vincent personally make, and why?
2. **Human judgment:** Which AI-generated observation did Vincent accept, revise or reject after checking the video, and what evidence changed his mind?
3. **Next experiment:** Which single question would Vincent test next, and what evidence would count as a reliable result?

Answers should be in Vincent's own words. If an example did not occur, leave it unclaimed rather than inventing a debugging experience.

## Publication and privacy

The Leo demo has specific family authorization. That is not blanket consent for other young players, and media rights do not transfer under the source code's MIT license. Do not add other participants' faces, videos, reports, telemetry, contact details or identifying metadata to public code without the appropriate separate consent and review.

See [AI-assisted analysis boundaries](ai_assisted_analysis.md), [known limitations](limitations.md), and [data policy](../DATA_POLICY.md).
