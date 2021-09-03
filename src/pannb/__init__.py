"""A panflute filter that process ipynb inputs."""

from __future__ import annotations

from panflute.elements import CodeBlock, Div, Doc, RawBlock
from panflute.io import run_filters
from panflute.tools import convert_text

from .util import setup_logging

logger = setup_logging()

RAW_TEX_FORMATS = {"latex", "textile", "html", "ipynb"}


def convert_jupytext_metadata(raw_block: RawBlock, doc: Doc) -> list | None:
    """Overwrite doc.metadata by jupytext-style metadata."""
    # overwrite
    meta = convert_text(raw_block.text, standalone=True)
    if (metadata := meta._metadata):
        doc._metadata = metadata
        logger.debug("Overwritten doc metadata by jupytext's: %s", doc.get_metadata())
        setattr(doc, "_walk_and_convert_jupytext_metadata_not_done", False)
        return []


def walk_and_convert_jupytext_metadata(
    element=None,
    doc: Doc | None = None,
):
    """Walk and overwrite doc.metadata by jupytext-style metadata if found."""
    _walk_and_convert_jupytext_metadata_not_done = getattr(doc, "_walk_and_convert_jupytext_metadata_not_done", True)
    if (
        _walk_and_convert_jupytext_metadata_not_done
        and doc is not None
        and isinstance(div := element, Div)
        and len(div.content) == 1
        and isinstance((raw_block := div.content[0]), RawBlock)
        and raw_block.format == "ipynb"
    ):
        return convert_jupytext_metadata(raw_block, doc)


def convert_raw_block(
    element=None,
    doc: Doc | None = None,
):
    if isinstance(element, RawBlock) and element.format != "ipynb":
        input_format = element.format
        if input_format in RAW_TEX_FORMATS:
            input_format += "+raw_tex"
        return convert_text(element.text, input_format=input_format)


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
