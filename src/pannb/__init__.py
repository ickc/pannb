"""A panflute filter that process ipynb inputs."""

from __future__ import annotations

from panflute.elements import CodeBlock, Div, Doc, RawBlock
from panflute.io import run_filters
from panflute.tools import convert_text

from .util import setup_logging

logger = setup_logging()


def convert_jupytext_metadata(raw_block: RawBlock, doc: Doc) -> None:
    """Overwrite doc.metadata by jupytext-style metadata."""
    # overwrite
    meta = convert_text(raw_block.text, standalone=True)
    doc._metadata = meta._metadata
    logger.debug("Overwritten doc metadata by jupytext's: %s", doc.get_metadata())


def walk_and_convert_jupytext_metadata(
    element=None,
    doc: Doc | None = None,
):
    """Walk and overwrite doc.metadata by jupytext-style metadata if found."""
    if (
        doc is not None
        and isinstance(div := element, Div)
        and len(div.content) == 1
        and isinstance((raw_block := div.content[0]), RawBlock)
        and raw_block.format == "ipynb"
    ):
        convert_jupytext_metadata(raw_block, doc)
        return []


def convert_raw_block(
    element=None,
    doc: Doc | None = None,
):
    if isinstance(element, RawBlock) and element.format != "ipynb":
        return convert_text(element.text, input_format=element.format)


def remove_python_codeblock(
    element=None,
    doc: Doc | None = None,
):
    """Delete CodeBlock with only class python."""
    if isinstance(element, CodeBlock) and element.classes == ["python"]:
        return []


def main(doc: Doc | None = None):
    """a pandoc filter converting math in code block.

    Fenced code block with class math will be runned using texp.
    """
    return run_filters(
        [
            walk_and_convert_jupytext_metadata,
            convert_raw_block,
            remove_python_codeblock,
        ],
        doc=doc,
    )


if __name__ == "__main__":
    main()
