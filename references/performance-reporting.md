# Performance Reporting

Explain optimization in terms of the context an agent must load before it can help.

## Measurements

- **Default load**: files an agent is told to read before most relevant tasks.
- **Task route load**: startup file plus the specific playbook or source needed for a task.
- **Canonical source size**: full source-of-truth files that should be opened only when needed.
- **Index size**: lightweight lookup files that can answer routing or narrow lookup questions.

## Token Estimate

Use a simple estimate unless a runtime tokenizer is available:

```text
estimated_tokens = word_count / 0.75
```

For reduction:

```text
saved_words = before_words - after_words
saved_tokens = before_tokens - after_tokens
percent_reduction = saved_words / before_words * 100
```

## User-Facing Summary Template

```text
Current default load: N files, X words, about Y tokens.
Proposed default load: M files, A words, about B tokens.
Estimated reduction: C words, about D tokens, E%.

Practical benefit: agents should start faster, repeat fewer instructions, and only open large sources when exact facts are needed.
Tradeoff: narrow tasks may require one extra targeted read when they need exact source material.
```

## Token Consumption Example

```text
Current default load: 5 files, 3,000 words, about 4,000 tokens.
Proposed default load: 1 startup file, 450 words, about 600 tokens.
Estimated reduction: 2,550 words, about 3,400 tokens, 85%.

Practical benefit: agents can begin with the routing and rules they need, then open the exact source only when the task requires it.
Tradeoff: a task that needs exact policy, metric, or glossary wording may require one extra targeted file read.
```

## Useful Route Examples

- Glossary lookup: startup file plus glossary index, then full glossary only for exact wording.
- Status or project update: startup file plus project tracker or current status source.
- Design work: startup file plus design index, then full design system only for exact tokens or QA.
- Compliance work: startup file plus compliance source, with no guessing from memory.

## Language Guidelines

- Be concrete and numerical.
- Avoid promising exact speed improvements unless measured.
- Say "estimated token reduction" when using word-count approximations.
- Call out that lazy loading preserves source depth while reducing unnecessary startup context.
