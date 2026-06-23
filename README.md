# Comment DOCX

Agent-friendly DOCX commenting using LLM-selected run ranges.

The tool reads a `.docx`, builds a structured list of text runs with stable ids,
asks an OpenAI-compatible LLM which runs should receive comments for a query,
validates the response, and writes a new `.docx` with comments.

## Configuration

Values may be supplied in the environment or a local `.env` file:

```bash
PROVIDER_BASE_URL=https://dashscope-intl.aliyuncs.com/compatible-mode/v1
PROVIDER_API_KEY=...
PROVIDER_MODEL=qwen-plus-latest
```

## CLI

```bash
uv run comment-docx add resources/бескупонные_облигации.docx "Find places that need clarification"
```

By default this writes `<input-stem>.commented.docx`. Choose a path with
`--output`:

```bash
uv run comment-docx add file.docx "Comment risky assumptions" --output outputs/file.commented.docx
```

Useful options:

- `--author`: DOCX comment author. Default: `LLM Agent`.
- `--initials`: DOCX comment initials. Default: `AI`.
- `--timeout`: LLM request timeout in seconds. Default: `120`.
- `--max-tokens`: Maximum LLM response tokens. Default: `2048`.
- `--dump-context`: Write the run-id context JSON for inspection.

## Scope

The first version exposes non-empty runs from main document body paragraphs and
table cells. Comments are anchored to complete Word runs because `python-docx`
comments must start and end on run boundaries.
