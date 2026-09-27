# FilePilot Architecture

FilePilot deliberately keeps its runtime small. The application is a Python CLI with two source modules and no third-party runtime dependency.

## Flow

<pre>
CLI arguments
    |
    v
build_plan(source, destination, ...)
    |
    +--> category_for(path)
    +--> _unique_destination(...)
    |
    v
list[Move]
    |
    +--> plan command ----> print only
    |
    +--> organize --------> apply_plan(...)
                              |
                              +--> shutil.move
                              +--> rollback on failure
                              +--> JSON manifest
                                         |
                                         v
                                  undo(manifest)

hash command ---------------------------> SHA-256
</pre>

## Core data model

<code>Move</code> is a frozen dataclass containing source path, destination path, category, and file size.

## Planning

<code>category_for()</code> uses the lowercase file suffix and the in-code category mapping. Unknown extensions are assigned to Other.

<code>build_plan()</code> resolves paths, validates the source, rejects unsafe recursive same-destination use, enumerates files, skips hidden paths unless requested, chooses categories, reserves collision-free destinations, and returns a sorted list of Move values.

No file move occurs during planning.

## Apply and rollback

<code>apply_plan()</code> requires a new manifest path. Moves are applied one by one and tracked. If a later move fails, completed moves are traversed in reverse and moved back when possible.

After all moves succeed, FilePilot writes a versioned JSON manifest with a UTC creation timestamp and serialized move records.

This is best-effort rollback, not a filesystem transaction or backup snapshot.

## Undo

<code>undo()</code> reads the manifest and processes moves in reverse.

- Missing moved files are skipped.
- An occupied original path raises FileExistsError.
- Parent directories are recreated when required.

## Integrity helper

<code>file_sha256()</code> reads a file in chunks and returns a SHA-256 hex digest. It does not compare against a remote registry.

## Tests and CI

The tests cover case-insensitive classification, collision-safe naming, apply/undo round trips, recursive safety, hidden-file behavior, and a known SHA-256 digest.

GitHub Actions runs pytest on Ubuntu, Windows, and macOS with Python 3.10, 3.12, and 3.13.
