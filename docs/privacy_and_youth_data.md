# Privacy and Youth Data

This project involves minors. The telemetry sample is synthetic. A specific family-authorized coaching case is also available.

Except for the Leo case explicitly authorized below, keep these out of public files, Issues, pull requests, notebook output, and history:
- Participant names, stable identifiers, dates of birth, schools, locations, and contacts
- Individual scores, medical information, family feedback, and private reports
- Raw or annotated videos, faces, voices, jersey numbers, distinctive backgrounds, and source-frame images
- Filenames, timestamps, GPS/EXIF, embedded document credentials, private links, notebook metadata, and lookup tables that can reconnect a record to a person
- Real frame-level movement telemetry unless a separate, specific publication review establishes permission and adequately addresses reidentification risk

Replacing a name with a token is pseudonymization, not proof of anonymity. Annotation overlays preserve the source image. Automatic ignore rules and metadata removal cannot replace a manual release review.

Use the project locally with media you are authorized to process. Uploading to Colab or an AI service is a separate sharing action; do not upload participant media or data merely to run a public demo.

The public repository documents the method; it is not a public database of children.

## Specific publication exception: Leo coaching case

The owner expressly authorized publishing the supplied Leo demo. Selected clips, still frames, first name, session dates, report-based scores, and an archived overlay are included in `examples/leo-coaching-demo/`. This exception applies only to those supplied assets; the original recordings and private review PDF are excluded. Media and likeness rights are not granted by the MIT code license. The case is not a public-script validation dataset or an automatic-scoring demonstration.
