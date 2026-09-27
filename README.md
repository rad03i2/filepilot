<div align="center">

<img src="assets/filepilot-brand-cover.svg" alt="FilePilot — safe local file organization with preview and undo" width="100%" />

# FilePilot

### Preview the route. Organize with intent. Undo when needed.

A small, cross-platform Python CLI for **local-first, reversible file organization**.

[العربية](README_AR.md) · [Architecture](docs/ARCHITECTURE.md) · [Brand](docs/BRAND.md) · [Security](SECURITY.md) · [Changelog](CHANGELOG.md)

[![CI](https://github.com/rad03i2/filepilot/actions/workflows/ci.yml/badge.svg)](https://github.com/rad03i2/filepilot/actions/workflows/ci.yml)
![Python](https://img.shields.io/badge/Python-3.10%2B-18212C?logo=python&logoColor=F6C453)
![Runtime](https://img.shields.io/badge/Runtime-Standard%20Library-3264FF)
![Privacy](https://img.shields.io/badge/Privacy-Local--First-36C9A7)
![License](https://img.shields.io/badge/License-MIT-FF6B4A)

<sub>Built by <strong>Radwan Abd alhady Ahmed</strong> · <strong>رضوان عبدالهادي</strong></sub>

</div>

---

## The idea

Most file organizers focus on moving things quickly. FilePilot focuses on knowing **what will happen before the filesystem changes**.

<pre>
PLAN  →  REVIEW  →  ORGANIZE  →  MANIFEST  →  UNDO
</pre>

<code>filepilot plan</code> is read-only. <code>filepilot organize</code> applies the reviewed move plan. Successful moves are recorded in a JSON manifest, and <code>filepilot undo</code> can use that manifest to restore moved files.

No cloud service, account, daemon, database, or background process is required.

---

## What is implemented today

| Capability | Current behavior |
|---|---|
| Preview | <code>filepilot plan</code> prints proposed moves without changing files |
| Classification | Extension-based categories for common file types |
| Collision safety | Existing destination files are not overwritten; a unique filename is generated |
| Apply | Files are moved with Python standard-library filesystem tools |
| Rollback | If apply fails midway, completed moves are replayed in reverse when possible |
| Undo | A JSON manifest records successful moves and can restore them |
| Hidden files | Skipped by default; opt in with <code>--include-hidden</code> |
| Recursive mode | Requires a separate destination to avoid reprocessing category folders |
| Integrity utility | SHA-256 hashing through <code>filepilot hash</code> |
| Runtime dependencies | None outside the Python standard library |
| CI | Ubuntu, Windows, macOS × Python 3.10, 3.12, 3.13 |

> FilePilot reduces common automation risks, but it is not a backup system. Keep independent backups of irreplaceable data.

---

## 30-second start

~~~bash
git clone https://github.com/rad03i2/filepilot.git
cd filepilot

python -m venv .venv
python -m pip install -e .
~~~

Preview a folder:

~~~bash
filepilot plan ~/Downloads
~~~

Organize it and write an undo manifest:

~~~bash
filepilot organize ~/Downloads --manifest ~/filepilot-run.json
~~~

Undo the successful moves:

~~~bash
filepilot undo ~/filepilot-run.json
~~~

---

## Commands

### Plan

~~~bash
filepilot plan ~/Downloads
filepilot plan ~/Downloads --destination ~/Sorted
~~~

### Organize

~~~bash
filepilot organize ~/Downloads --manifest ~/filepilot-run.json
~~~

Skip interactive confirmation only when intentional:

~~~bash
filepilot organize ~/Downloads --manifest ~/filepilot-run.json --yes
~~~

### Recursive organization

Recursive mode requires a separate destination:

~~~bash
filepilot plan ~/Downloads --destination ~/Sorted --recursive
filepilot organize ~/Downloads --destination ~/Sorted --recursive --manifest ~/filepilot-run.json
~~~

### Hidden files and hashing

~~~bash
filepilot plan ~/Downloads --include-hidden
filepilot hash path/to/file.iso
~~~

---

## What gets sorted

FilePilot currently classifies by file extension.

| Category | Examples |
|---|---|
| Images | JPG, PNG, GIF, WebP, SVG, HEIC |
| Videos | MP4, MKV, AVI, MOV, WebM |
| Audio | MP3, WAV, FLAC, AAC, OGG |
| Documents | PDF, DOCX, TXT, RTF, ODT, Markdown |
| Spreadsheets | CSV, XLSX, ODS |
| Presentations | PPT, PPTX, ODP |
| Archives | ZIP, RAR, 7Z, TAR, GZ |
| Code | Python, JavaScript, TypeScript, C/C++, C#, Go, Rust, HTML, CSS, JSON, YAML |
| Other | Extensions outside the configured groups |

Classification is case-insensitive. File contents and MIME signatures are **not** inspected.

---

## Safety model

### Before a move

- Plan mode is non-destructive.
- Hidden files are excluded unless explicitly requested.
- Recursive mode cannot reuse the source as its destination.
- Destination names are reserved during planning so planned moves do not collide.

### During apply

- Existing destination paths are never overwritten.
- Each successful move is tracked in memory.
- If a later move fails, completed moves are attempted in reverse order.
- The manifest itself must not already exist.

### During undo

- Moves are replayed in reverse order.
- Missing moved files are skipped.
- If the original path is occupied, undo raises an error instead of overwriting it.

Read [SECURITY.md](SECURITY.md) for the data-safety boundaries.

---

## Architecture

~~~mermaid
flowchart LR
    A[Source folder] --> B[build_plan]
    B --> C[Classify by extension]
    C --> D[Resolve safe destinations]
    D --> E{Command}
    E -->|plan| F[Print only]
    E -->|organize| G[apply_plan]
    G --> H[Filesystem moves]
    H --> I[JSON manifest]
    I --> J[undo]
    J --> K[Restore original paths]
    L[filepilot hash] --> M[SHA-256]
~~~

<pre>
src/filepilot/
├── core.py        planning, classification, move/rollback, undo, SHA-256
├── cli.py         argument parsing and command output
└── __init__.py    package metadata

tests/
└── test_core.py   core behavior tests
</pre>

See [docs/ARCHITECTURE.md](docs/ARCHITECTURE.md) for the failure and recovery flow.

---

## Quality baseline

~~~bash
python -m pip install -e . pytest
pytest -q
~~~

The current workflow runs a **9-environment CI matrix**:

| OS | Python |
|---|---|
| Ubuntu | 3.10 · 3.12 · 3.13 |
| Windows | 3.10 · 3.12 · 3.13 |
| macOS | 3.10 · 3.12 · 3.13 |

---

## Current boundaries

- Classification is extension-based rather than content-aware.
- Undo restores files but leaves empty category directories in place.
- The manifest records moves; it is not a backup of file contents.
- Recursive mode requires a destination outside the source.
- There is no graphical interface.
- There is no network or cloud synchronization layer.
- There is no scheduled/background organization.

---

## Contributing

Contributions are welcome when they preserve FilePilot's central rule: **filesystem automation must stay understandable and reversible where practical**.

Read [CONTRIBUTING.md](CONTRIBUTING.md) before changing move, rollback, collision, or undo behavior.

---

## License & author

MIT License — see [LICENSE](LICENSE).

**Radwan Abd alhady Ahmed**  
**رضوان عبدالهادي**  
GitHub: [@rad03i2](https://github.com/rad03i2)

<div align="center">
<img src="assets/filepilot-logo-square.svg" alt="FilePilot logo" width="116" />
<br/>
<sub>FILEPILOT · ROUTEBOARD IDENTITY · PREVIEW → ORGANIZE → UNDO</sub>
</div>
