# File Tree Model

Use this model as a default, not a rigid schema. Adapt names to the user's domain, but preserve the separation between startup context, source material, workflows, outputs, checks, and archive.

```text
knowledge-base/
  README.md
  identity/
    agent-start.md
    context.md
    preferences.md
    rules.md
  playbooks/
    workflows/
    example-workflow.md
  sources/
    indexes/
    sources/
    key-links.md
    recurring-docs.md
  outputs/
    outputs/
    drafts/
    reports/
  reviews/
    data-checklist.md
    writing-checklist.md
    design-checklist.md
  archive/
    legacy-root-sources/
```

## Folder Responsibilities

- `README.md`: human-facing orientation, current structure, and where to start.
- `identity/agent-start.md`: compact agent startup. Keep this short and stable, ideally under 500 words.
- `identity/context.md`: deeper role, project, team, and operating context.
- `identity/preferences.md`: communication, formatting, decision, and collaboration preferences.
- `identity/rules.md`: hard approval boundaries and non-negotiable constraints.
- `playbooks/`: repeatable workflows, procedures, prompts, and operating cadences.
- `sources/sources/`: canonical source shelf for source-of-truth documents.
- `sources/indexes/`: lightweight lookup files for large canonical sources.
- `sources/key-links.md`: important external or internal links.
- `sources/recurring-docs.md`: recurring documents that agents should know how to find.
- `outputs/`: generated artifacts, drafts, reports, exports, and migration records.
- `reviews/`: checklists and quality gates.
- `archive/`: backups, legacy layouts, moved files, manifests, and migration notes.

## Migration Patterns

- If source-of-truth risk is high, copy first, verify checksums, then update routing.
- If visual cleanup matters, move legacy root clutter into `archive/legacy-root-sources/` after canonical copies exist.
- If old agent instructions still reference legacy paths, keep compatibility pointers until active loaders are updated.
- If a source is large but frequently queried for narrow facts, create an index rather than loading the full source by default.
- If a file combines routing, rules, and source material, split it into startup routing plus canonical source files.

## Naming Guidance

- Use lowercase hyphenated names for new Markdown files unless the existing project clearly uses another convention.
- Preserve original filenames in the archive.
- Prefer descriptive source names such as `product-glossary.md`, `q3-okrs.md`, or `design-system.md`.
- Avoid names that encode tool-specific behavior unless the knowledge base is intentionally tool-specific.
