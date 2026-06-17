# Audit Rubric

Use this rubric before proposing or making changes. The goal is to protect context while reducing friction and token load. Zero knowledge loss is mandatory: original source material must remain recoverable, traceable, and verifiable.

## User Mode Fit

- Starter mode: The next step is simple, plain-language, and does not require knowing agent or repository jargon.
- Cleanup mode: The recommendation starts with inventory, classification, and archive-first preservation.
- Advanced optimization mode: The recommendation includes measured startup load, task-route load, and estimated token reduction.
- Maintenance mode: The recommendation keeps source files, indexes, links, and routing healthy after initial setup.
- The mode can be changed as the user becomes more confident or asks for deeper optimization.

## Beginner Usability

- The proposed starter tree has only the folders the user needs now.
- The user can tell where to put personal context, source material, workflows, outputs, and archive files.
- Recommendations avoid unexplained terms such as canonical, lazy loading, or provenance unless briefly defined.
- The smallest useful next action is clear.

## Organization

- The top-level tree has a clear small set of folders.
- Canonical source files have one active location.
- Outputs and drafts are not mixed with source material.
- Archive material is clearly separated from active sources.
- Compatibility layers are labeled as compatibility layers, not canonical files.

## Messy-Source Triage

- Each file is classified before moving: canonical source, derived output, workflow, review/checklist, identity/rule, or archive candidate.
- Duplicate filenames are reviewed as possible source-of-truth conflicts.
- Large or important files are copied before moving when their status is uncertain.
- Original path, new path, action, and reason are recorded in a migration map.
- Unreferenced files are treated as discovery items, not trash.

## Routing

- Agents have one compact startup path.
- Startup instructions point to task-specific sources instead of loading broad context by default.
- Loader files do not duplicate the same rules in multiple places.
- Reread triggers are explicit for exact facts, definitions, current status, compliance, or other high-risk claims.
- Active loaders do not point to archived or legacy paths except as compatibility fallbacks.

## Maintenance

- New files have a clear home, provenance note, and route from an index, README, key-links file, or loader.
- Indexes are refreshed when canonical sources change.
- Markdown files have useful headings and are not empty placeholder files unless explicitly intentional.
- Broken links, stale references, and duplicate source names are reviewed regularly.
- Startup files are watched for load creep as new rules and context are added.
- Maintenance edits are additive and reversible unless the user explicitly requests source rewriting.

## Token Load

- Default startup file set is listed and word-counted.
- Common task routes are listed and word-counted.
- Large files are marked as canonical source, not default context.
- Frequently queried large files have lightweight indexes.
- Estimated tokens use a consistent approximation, such as `words / 0.75`.

## Advanced Optimization

- The default startup path is reduced to the smallest safe context.
- Task routes load indexes before full sources when exact details are not needed.
- Full canonical sources remain available for exact facts, definitions, rules, compliance, metrics, or current status.
- Any extra targeted read introduced by lazy loading is disclosed as a tradeoff.
- The system is not called optimized until source preservation and routing checks both pass.

## Safety

- A timestamped archive exists before mutation.
- A file manifest records the initial file list.
- A checksum manifest records initial content hashes.
- An old-to-new path map records copied, moved, untouched, and archived files.
- Existing source files are not deleted.
- Full source files are not replaced by summaries or indexes.
- Moves are reversible and documented.
- User approval is obtained before changing source-of-truth files when the user's rules require it.

## Knowledge Loss Risk

- **Critical**: Delete, overwrite, or summarize-and-replace original sources. Block the change.
- **High**: Move source files without checksums, manifests, archive copy, or path map. Require preservation first.
- **Medium**: Update routing before verifying copied sources and links. Verify before promoting new routes.
- **Low**: Add derived indexes or startup files while keeping original sources intact and traceable.

## Verification

- Expected target folders and files exist.
- Canonical files are present in the target source shelf.
- Active loaders prefer the new routes.
- Old path references are absent from active loaders or explicitly documented as compatibility.
- Relative Markdown links are checked for likely broken paths.
- Before/after word counts and estimated token reductions are reported.
- Source preservation evidence is reported before performance gains.
