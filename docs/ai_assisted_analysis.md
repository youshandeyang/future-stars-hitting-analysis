# AI-Assisted Analysis

AI is experimental in this project.

## Public code and separate app

The public V3 Python script implements selected 2D body measurements, annotated video, and per-frame CSV export. It does not implement contact-frame detection, automatic six-category scoring, synchronized multi-camera analysis, or an AI report service.

The separately developed local coaching app has its own versions and testing history. Its interface and reported capabilities are not features of this repository unless matching code and tests are added here. Refer to the [separate app status page](https://www.futurestarsbaseballclub.org/app.html) for updates; no app binary or validation of its features is included in this repository.

The workflow below describes intended human-reviewed use of external AI assistance, not functions implemented by the Python script. Software checks on synthetic/mock data do not validate an AI report or a real swing measurement.

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

Vincent reviews the final coaching recommendation.

AI should be allowed to return: **not enough information**.

This file describes a human-reviewed workflow. The repository does not implement an AI reporting service or include an approved drill library. Do not send participant videos, reports, or telemetry to a third-party AI service without specific permission for that data and destination. The family-authorized Leo coaching case is a separate real-footage example, not an implemented AI report service or public-script validation. Other public examples use synthetic data.

The [Phase I family guide and AI report rules](phase_i_family_guide.md) provide the detailed report structure and optional prompt. A heading such as “What Improved Most” does not imply an improvement occurred; report no supported gain when that is what the evidence shows.
