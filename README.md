# Knowledge Base Optimizer

Turn a messy knowledge base into a fast, lossless source of truth. Splits startup context from deep reference, so agents start faster and cost fewer tokens, with zero files lost.

It audits how your files are organized, separates the compact context an agent needs at startup from the deep reference material it only reads on demand, and restructures everything without ever deleting or summarizing away an original file. The result is faster agent startup, lower token costs, and a knowledge base that stays trustworthy as it grows.

## Install

```bash
npx skills add https://github.com/craviart/knowledge-base-optimizer
```

## What's inside

- **`SKILL.md`** — the skill: operating rules, user modes, and the standard audit-to-optimize workflow.
- **`scripts/audit_knowledge_base.py`** — a read-only audit helper that reports tree shape, Markdown word/token counts, likely loader files, largest files, duplicate names, broken relative links, and path risks.
- **`references/`** — supporting guides: target file-tree model, audit rubric, zero-loss migration, performance reporting, and the maintenance loop.

## Tags

knowledge base, context engineering, agent memory, token optimization, file organization, source of truth, markdown, developer tools

## License

[MIT](LICENSE) © Camille Raviart
