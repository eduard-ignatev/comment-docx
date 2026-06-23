from pathlib import Path

import click
from docx import Document
from dotenv import load_dotenv

from comment_docx.commenter import (
    CommentDocxError,
    ProviderConfig,
    add_comments_to_docx,
    build_run_context,
    default_output_path,
)
from comment_docx.commenter import (
    dump_context as write_context_dump,
)


@click.group()
def cli() -> None:
    """Add LLM-generated comments to DOCX files."""


@cli.command()
@click.argument(
    "input_path",
    type=click.Path(exists=True, file_okay=True, dir_okay=False, path_type=Path),
)
@click.argument("query", type=str)
@click.option(
    "--output",
    "output_path",
    type=click.Path(file_okay=True, dir_okay=False, path_type=Path),
    default=None,
    help="Path for the commented DOCX.",
)
@click.option("--author", default="AI Commenter", show_default=True, help="DOCX comment author.")
@click.option("--provider-base-url", default=None, help="OpenAI-compatible provider base URL.")
@click.option("--api-key", default=None, help="OpenAI-compatible provider API key.")
@click.option("--model", default=None, help="OpenAI-compatible model name.")
@click.option("--timeout", type=float, default=120.0, show_default=True, help="LLM request timeout in seconds.")
@click.option("--max-tokens", type=int, default=2048, show_default=True, help="Maximum LLM response tokens.")
@click.option(
    "--dump-context",
    type=click.Path(file_okay=True, dir_okay=False, path_type=Path),
    default=None,
    help="Write the run context sent to the model as JSON.",
)
def add(
    input_path: Path,
    query: str,
    output_path: Path | None,
    author: str,
    provider_base_url: str | None,
    api_key: str | None,
    model: str | None,
    timeout: float,
    max_tokens: int,
    dump_context: Path | None,
) -> None:
    """Add comments to INPUT_PATH for QUERY and write a new DOCX."""
    load_dotenv()
    output_path = output_path or default_output_path(input_path)

    try:
        provider = ProviderConfig.from_values(
            base_url=provider_base_url,
            api_key=api_key,
            model=model,
            timeout=timeout,
            max_tokens=max_tokens,
        )

        if dump_context is not None:
            context = build_run_context(Document(input_path))
            write_context_dump(context, dump_context, query)

        result = add_comments_to_docx(
            input_path=input_path,
            output_path=output_path,
            query=query,
            provider=provider,
            author=author,
        )
    except CommentDocxError as error:
        click.echo(f"Error: {error}", err=True)
        raise SystemExit(1) from error

    click.echo(f"Output: {result.output_path}")
    click.echo(f"Comments: {result.match_count}")
    click.echo(f"Runs: {result.run_count}")
