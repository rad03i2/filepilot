# Security Policy

FilePilot operates on local files, so data-loss prevention is the primary security concern.

## Reporting
Please report security issues privately to the maintainer through an appropriate private GitHub contact channel rather than publishing exploit details in a public issue. Do not include private files, credentials, or personal data in reports.

## Safety guarantees and boundaries
- Existing destination files are not overwritten.
- Hidden files are excluded unless explicitly requested.
- A failed apply attempts to roll back moves already completed in that run.
- Undo refuses to overwrite a newly occupied original path.
- FilePilot does not include network communication.

These controls reduce risk but are not a substitute for backups of irreplaceable data.

Maintainer: **Radwan Abdulhadi Ahmed (@rad03i2)**
