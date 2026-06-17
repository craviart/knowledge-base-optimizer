# Zero-Loss Migration

Use this reference for cleanup or restructuring work. Optimization is only successful when the original knowledge remains recoverable and traceable.

## Core Invariants

- Preserve every original file before changing structure.
- Never replace a full source with a summary, index, or startup note.
- Treat indexes, summaries, and routing files as derived artifacts.
- Copy before moving when the source-of-truth status is uncertain.
- Keep a path map so every old location can be traced to its new location or archive location.

## Archive-First Sequence

1. Create a timestamped migration folder, usually under `archive/` or `outputs/reports/`.
2. Write a file manifest with every original file path.
3. Write a SHA-256 checksum manifest for every readable original file.
4. Create an old-to-new path map with columns: original path, action, new path, reason, verification status.
5. Copy high-risk source material into the target structure before moving or archiving anything.
6. Verify copied file checksums before updating routes.
7. Move legacy clutter into archive only after source copies and path maps exist.

## Content Coverage Checks

- Compare file counts before and after migration.
- Confirm every original path appears in the manifest and path map.
- Confirm every copied source has matching checksum before any link rewriting.
- Confirm derived indexes point to full sources.
- Confirm active loaders route to current sources, not archived files, unless explicitly marked as compatibility.

## Rollback Expectations

- A user or future agent should be able to reconstruct the initial state from the archive and path map.
- Archive folders should preserve original filenames and folder names when practical.
- If paths must be renamed for safety or portability, record the exact reason in the path map.
- Do not remove the archive as part of the same optimization pass.

## User-Facing Language

Lead with preservation before performance:

```text
First I will preserve the current state: archive, file manifest, checksums, and an old-to-new path map.
Then I will reorganize copies or move legacy files into archive.
Only after that will I update routing and report the token savings.
```
