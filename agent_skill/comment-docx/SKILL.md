---
name: comment-docx
description: Add review comments to DOCX files using an OpenAI-compatible LLM.
metadata: { "openclaw": { "requires": { "bins": ["comment-docx"], "env": ["PROVIDER_BASE_URL", "PROVIDER_API_KEY", "PROVIDER_MODEL"] } } }
---

# Comment DOCX

Use this skill when there is a need to add comments, review notes, or targeted
feedback into a local DOCX file.

The tool builds a run-id map from body paragraphs and tables, asks an
OpenAI-compatible LLM to select start/end run ids and comment text, validates the
response, and writes a new DOCX with comments.

## Inputs

- DOCX file path
- Natural-language query describing what to comment

## Output

- A new `.docx` file containing Word comments

## Configuration

Expected environment variables:

- `PROVIDER_BASE_URL`
- `PROVIDER_API_KEY`
- `PROVIDER_MODEL`

Values can also be supplied via CLI options.

## Example

```bash
comment-docx add file.docx "Comment claims that need source citations"
```

## Options

- `--output`: Output DOCX path.
- `--author`: DOCX comment author. Default: `LLM Agent`.
- `--initials`: DOCX comment initials. Default: `AI`.
- `--timeout`: LLM request timeout in seconds. Default: `120`.
- `--max-tokens`: Maximum LLM response tokens. Default: `2048`.
- `--dump-context`: Write the run-id context JSON for inspection.
