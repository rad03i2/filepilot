from __future__ import annotations

import hashlib
import json
import shutil
from dataclasses import asdict, dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Iterable

CATEGORIES: dict[str, set[str]] = {
    "Images": {".jpg", ".jpeg", ".png", ".gif", ".webp", ".bmp", ".svg", ".heic"},
    "Videos": {".mp4", ".mkv", ".avi", ".mov", ".webm", ".m4v"},
    "Audio": {".mp3", ".wav", ".flac", ".aac", ".ogg", ".m4a"},
    "Documents": {".pdf", ".doc", ".docx", ".txt", ".rtf", ".odt", ".md"},
    "Spreadsheets": {".csv", ".xls", ".xlsx", ".ods"},
    "Presentations": {".ppt", ".pptx", ".odp"},
    "Archives": {".zip", ".rar", ".7z", ".tar", ".gz", ".bz2", ".xz"},
    "Code": {".py", ".js", ".ts", ".java", ".c", ".cpp", ".cs", ".go", ".rs", ".html", ".css", ".json", ".yaml", ".yml"},
}

@dataclass(frozen=True)
class Move:
    source: str
    destination: str
    category: str
    size: int


def category_for(path: Path) -> str:
    suffix = path.suffix.lower()
    for category, extensions in CATEGORIES.items():
        if suffix in extensions:
            return category
    return "Other"


def _unique_destination(path: Path, reserved: set[Path]) -> Path:
    if not path.exists() and path not in reserved:
        return path
    stem, suffix = path.stem, path.suffix
    counter = 1
    while True:
        candidate = path.with_name(f"{stem} ({counter}){suffix}")
        if not candidate.exists() and candidate not in reserved:
            return candidate
        counter += 1


def build_plan(source: Path, destination: Path | None = None, *, recursive: bool = False,
               include_hidden: bool = False) -> list[Move]:
    source = source.expanduser().resolve()
    destination = (destination or source).expanduser().resolve()
    if not source.is_dir():
        raise ValueError(f"Source is not a directory: {source}")
    if source == destination and recursive:
        raise ValueError("Recursive mode requires a separate destination to avoid reprocessing category folders.")

    iterator: Iterable[Path] = source.rglob("*") if recursive else source.iterdir()
    reserved: set[Path] = set()
    moves: list[Move] = []
    for item in iterator:
        if not item.is_file():
            continue
        try:
            relative = item.relative_to(source)
        except ValueError:
            continue
        if not include_hidden and any(part.startswith(".") for part in relative.parts):
            continue
        category = category_for(item)
        target = _unique_destination(destination / category / item.name, reserved)
        if item.resolve() == target.resolve():
            continue
        reserved.add(target)
        moves.append(Move(str(item), str(target), category, item.stat().st_size))
    return sorted(moves, key=lambda m: (m.category, m.source.lower()))


def apply_plan(moves: list[Move], manifest: Path) -> dict:
    manifest = manifest.expanduser().resolve()
    if manifest.exists():
        raise FileExistsError(f"Manifest already exists: {manifest}")
    completed: list[Move] = []
    try:
        for move in moves:
            src, dst = Path(move.source), Path(move.destination)
            if not src.is_file():
                raise FileNotFoundError(src)
            dst.parent.mkdir(parents=True, exist_ok=True)
            if dst.exists():
                raise FileExistsError(dst)
            shutil.move(str(src), str(dst))
            completed.append(move)
    except Exception:
        for move in reversed(completed):
            src, dst = Path(move.source), Path(move.destination)
            if dst.exists() and not src.exists():
                src.parent.mkdir(parents=True, exist_ok=True)
                shutil.move(str(dst), str(src))
        raise

    payload = {
        "version": 1,
        "created_at": datetime.now(timezone.utc).isoformat(),
        "moves": [asdict(m) for m in completed],
    }
    manifest.parent.mkdir(parents=True, exist_ok=True)
    manifest.write_text(json.dumps(payload, indent=2, ensure_ascii=False), encoding="utf-8")
    return payload


def undo(manifest: Path) -> int:
    manifest = manifest.expanduser().resolve()
    data = json.loads(manifest.read_text(encoding="utf-8"))
    moves = [Move(**item) for item in data.get("moves", [])]
    restored = 0
    for move in reversed(moves):
        original, current = Path(move.source), Path(move.destination)
        if not current.exists():
            continue
        if original.exists():
            raise FileExistsError(f"Cannot restore; original path is occupied: {original}")
        original.parent.mkdir(parents=True, exist_ok=True)
        shutil.move(str(current), str(original))
        restored += 1
    return restored


def file_sha256(path: Path, chunk_size: int = 1024 * 1024) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        while chunk := handle.read(chunk_size):
            digest.update(chunk)
    return digest.hexdigest()
