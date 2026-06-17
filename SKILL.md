---
name: knowledge-base-optimizer
description: Audit, organize, maintain, and optimize local knowledge bases, context folders, agent memory folders, project brains, research libraries, or source-of-truth file trees with zero knowledge loss. Use when asked to create a knowledge base from scratch, clean a messy source of truth, maintain Markdown knowledge files, add or route new source files, refresh indexes, reduce drift, restructure knowledge, streamline context engineering, reduce token consumption, improve agent startup speed, create non-destructive migrations, audit file organization, design lazy-loading context routes, or explain performance benefits of a knowledge-base cleanup.
---

# Knowledge Base Optimizer

Use this skill to make a knowledge base easier for agents and humans to navigate while reducing default context load. Stay platform-neutral: do not assume a specific agent runtime, tool, company, project, or filesystem path.

## Operating Rules

- Start by discovering the current root, structure, active loader files, source files, and outputs. Infer the root from the user request when possible; otherwise ask for the root path.
- Audit before editing. Treat organization, startup load, duplicate routing, stale paths, large files, and source-of-truth ambiguity as first-class findings.
- Treat zero knowledge loss as the core invariant. Preserve original files, provenance, checksums, and migration records before improving structure or performance.
- Default to non-destructive changes. Before any mutation, create a timestamped archive, a file manifest, a SHA-256 checksum manifest, and an old-to-new path map inside an archive or reports area.
- Never delete files by default. Never replace a full source with a summary. Copy source-of-truth material before moving it when canonical status is unclear.
- Treat generated summaries, indexes, and startup files as derived artifacts, not replacements for source material.
- Separate fast startup context from deep reference context. Aim for one compact startup file, task-specific routing, lightweight indexes for large sources, and full source reads only for exact facts.
- When discussing changes with users, quantify performance: current default word/token load, proposed default word/token load, estimated reduction, practical speed benefit, and lazy-loading tradeoffs.
- Treat knowledge-base care as ongoing maintenance, not a one-shot migration. Help users add new files, refresh indexes, repair links, reduce drift, and keep routing current without losing original context.

## Choose the User Mode

- **Starter mode**: Use when the user has no existing structure or asks how to begin. Keep language plain, create the smallest useful tree, and offer one next step at a time.
- **Cleanup mode**: Use when the user has a messy source of truth. Inventory first, classify files, copy before moving uncertain sources, archive legacy clutter, and preserve path provenance.
- **Advanced optimization mode**: Use when the user already has a structure and wants speed, token, routing, or precision improvements. Measure before and after, add indexes, refine lazy-loading, and name the tradeoffs.
- **Maintenance mode**: Use when the user wants to add sources, update Markdown files, refresh indexes, check drift, repair links, or keep the knowledge base healthy after initial setup.

## Standard Workflow

1. **Map the current state**
   - List top-level folders, Markdown files, loaders, and likely canonical sources.
   - Run the audit helper when available: `python3 scripts/audit_knowledge_base.py /path/to/knowledge-base`.
   - For detailed structure guidance, read `references/file-tree-model.md`.
   - For migration or cleanup work, read `references/zero-loss-migration.md`.

2. **Measure context cost**
   - Count words in startup files, task routes, large sources, and indexes.
   - Estimate tokens as `words / 0.75` unless a better tokenizer is available.
   - Identify the current default load path and the smallest viable replacement.
   - For reporting guidance, read `references/performance-reporting.md`.

3. **Design the target structure**
   - Use `README.md` for human orientation.
   - Use `identity/` for compact agent startup, context, preferences, and rules.
   - Use `playbooks/` for repeatable workflows.
   - Use `sources/` for canonical sources plus lightweight indexes.
   - Use `outputs/` for generated work, drafts, exports, and reports.
   - Use `reviews/` for checklists and QA guardrails.
   - Use `archive/` for legacy structure, backups, and migration records.

4. **Plan or implement safely**
   - If only asked to audit, produce findings and recommendations without changing files.
   - If asked to implement, archive first, preserve manifests and checksums, then copy or move according to source-of-truth risk.
   - For messy systems, classify each file as canonical source, derived output, workflow, review/checklist, identity/rule, or archive candidate before moving it.
   - In every migration plan, state what will be copied, moved to archive, remain untouched, and how each old path maps to a new path.
   - Update active loaders to prefer the compact startup file and lazy task routing.
   - For safety checks and acceptance criteria, read `references/audit-rubric.md`.

5. **Maintain over time**
   - When adding a file, place it in the right area, preserve its original path or provenance, update the relevant index or key-link file, and verify routing.
   - When editing Markdown knowledge, keep the full source intact unless the user explicitly asks for content changes. Prefer additive updates, dated notes, and links back to source material.
   - Periodically check broken links, unreferenced sources, duplicate names, stale indexes, and startup-load creep.
   - For maintenance guidance, read `references/maintenance-loop.md`.

6. **Verify and explain**
   - Confirm expected files exist, old clutter moved or preserved safely, and active loaders no longer point at stale paths.
   - Re-run word counts and route checks.
   - Report before/after load size, estimated token savings, source-preservation evidence, and residual risks.
   - Do not describe the system as optimized unless source preservation and routing verification are both complete.

## Bundled Resources

- `scripts/audit_knowledge_base.py`: read-only audit helper for tree shape, Markdown word counts, likely loader files, largest files, path risks, broken relative Markdown links, and token estimates.
- `references/file-tree-model.md`: reusable target tree, naming conventions, and migration patterns.
- `references/audit-rubric.md`: checklist for organization, safety, routing, token load, and verification.
- `references/performance-reporting.md`: concise formulas and language for communicating speed and token benefits.
- `references/zero-loss-migration.md`: archive-first migration, provenance mapping, checksum verification, content coverage checks, and rollback expectations.
- `references/maintenance-loop.md`: ongoing care for adding files, refreshing indexes, repairing links, and keeping Markdown knowledge current.
