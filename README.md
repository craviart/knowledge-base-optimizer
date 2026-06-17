# Knowledge Base Optimizer

[![skills.sh](https://skills.sh/b/craviart/knowledge-base-optimizer)](https://skills.sh/craviart/knowledge-base-optimizer)

Turn a messy knowledge base into a fast, lossless source of truth. Splits startup context from deep reference, so agents start faster and cost fewer tokens, with zero files lost.

It audits how your files are organized, separates the compact context an agent needs at startup from the deep reference material it only reads on demand, and restructures everything without ever deleting or summarizing away an original file. The result is faster agent startup, lower token costs, and a knowledge base that stays trustworthy as it grows.

## Install

```bash
npx skills add https://github.com/craviart/knowledge-base-optimizer
```

## Try it

Once installed, prompt your agent with things like:

- "My knowledge base is a mess. Audit it and tell me what to fix first."
- "Reorganize this context folder to cut token usage, without losing anything."
- "Set up a clean knowledge base for this project from scratch."
- "Add these notes to my source of truth and refresh the indexes."
- "My agent is slow to start. Trim the context it loads by default."

## What's inside

- **`SKILL.md`**: the skill itself, with operating rules, four user modes (starter, cleanup, advanced optimization, maintenance), and the standard audit-to-optimize workflow.
- **`scripts/audit_knowledge_base.py`**: a read-only audit helper that reports tree shape, Markdown word and token counts, likely loader files, largest files, duplicate names, broken relative links, and path risks.
- **`references/`**: supporting guides covering the target file-tree model, audit rubric, zero-loss migration, performance reporting, and the maintenance loop.

## How it works

Zero knowledge loss is the core invariant. Original files are preserved, with a timestamped archive, a file manifest, SHA-256 checksums, and an old-to-new path map created before anything moves. Generated summaries and indexes are treated as derived artifacts, never replacements for source material. Only then does it separate a compact startup context from deep reference that is read on demand, and report the token savings.

## License

[MIT](LICENSE) © Camille Raviart
