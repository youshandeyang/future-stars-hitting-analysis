# AI-Assisted Analysis

AI is experimental in this project. The same phrase, “AI-assisted,” covers **two different kinds of help** here: (1) AI/Agent tools supporting software code and documentation, and (2) AI tools helping draft descriptions or coaching reports for human review. Neither means Vincent independently programmed an AI model, nor that software-generated coaching conclusions have been validated.

For concise ownership and evidence definitions, see [Project roles and evidence](project_roles_and_evidence.md).

## Public code and separate app

The public V3 Python script implements selected 2D body measurements, annotated video, and per-frame CSV export. It does not implement contact-frame detection, automatic six-category scoring, synchronized multi-camera analysis, or an AI report service.

The separately developed local coaching app has its own versions and testing history. Its interface and reported capabilities are not features of this repository unless matching code and tests are added here. Refer to the [separate app status page](https://www.futurestarsbaseballclub.org/app.html) for updates; no app binary or validation of its features is included in this repository.

The workflow below describes intended human-reviewed use of external AI assistance, not functions implemented by the Python script. Software checks on synthetic/mock data do not validate an AI report or a real swing measurement.

## Who decides what

| Responsibility | Primary role |
| --- | --- |
| Identify the family coaching problem and affordable workflow goals | Vincent, drawing on his playing and coaching experience |
| Capture footage and support logistics | Vincent and family |
| Generate or revise Python implementation and technical prose | AI tools/agents with human guidance and oversight |
| Detect body landmarks in the public script | The third-party MediaPipe model |
| Review what an observed swing suggests and choose practical training priorities | Vincent or the responsible coach; AI may draft, not decide |
| Check whether baseline and retest conditions permit comparison | Human reviewer, with the recorded evidence |

Not every prototype output was personally reviewed or created by Vincent. Claims about his specific decisions need supporting notes or confirmation, rather than inference from source-code commits.

## Intended use
- Organize evidence from multiple views
- Summarize baseline vs retest changes
- Point out repeated patterns for review
- Draft parent-friendly explanations
- Suggest candidate drills from an approved project library

## Required evidence levels

### Observed
Directly visible or measured.

### Interpretation
A possible explanation. Must be labeled as interpretation, not fact.

### Recommendation
A testable training idea.

For a case that Vincent coaches, his own feedback and review should be identified as such. For other cases, a responsible coach or parent must decide whether any draft recommendation is suitable; AI text is not a substitute for this review.

AI should be allowed to return: **not enough information**. Do not invent frame timestamps, exact joint angles, score changes, contact outcomes, or coach quotations. If an output is from a separate local application or an earlier archived run, label that source rather than attributing it to this public code.

This file describes a human-reviewed workflow. The repository does not implement an AI reporting service or include an approved drill library. Do not send participant videos, reports, or telemetry to a third-party AI service without specific permission for that data and destination. The family-authorized Leo coaching case is a separate real-footage example, not an implemented AI report service or public-script validation. Other public examples use synthetic data.

The [Phase I family guide and AI report rules](phase_i_family_guide.md) provide the detailed report structure and optional prompt. A heading such as “What Improved Most” does not imply an improvement occurred; report no supported gain when that is what the evidence shows.
