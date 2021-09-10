"""A panflute filter that process ipynb inputs."""

from __future__ import annotations

from logging import getLogger
from typing import TYPE_CHECKING

from panflute.elements import CodeBlock, Div, Doc, Para, RawBlock
from panflute.io import run_filters
from panflute.tools import convert_text

if TYPE_CHECKING:
    from typing import Any

    from panflute.base import Element

logger = getLogger(__name__)

RAW_TEX_FORMATS = {"latex", "textile", "html", "ipynb"}
CODE_CELL_CLASSES = {"cell", "code"}
CODE_OUTPUT_CLASSES = {"output", "execute_result"}

#: priority for converting from raw-block format to AST
#: we choose latex first before some LaTeX Math environment might have extra delimiters around markdown, html
#: markdown next because if exist, it is likely considered a source format to be converted from
CONVERT_CELL_OUTPUT_PRIORITY = ("latex", "markdown", "html")


def convert_jupytext_metadata(raw_block: RawBlock, doc: Doc) -> list | None:
    """Overwrite doc.metadata by jupytext-style metadata."""
    # overwrite
    meta = convert_text(raw_block.text, standalone=True)
    if metadata := meta._metadata:
        doc._metadata = metadata
        logger.debug("Overwritten doc metadata by jupytext's: %s", doc.get_metadata())
        setattr(doc, "_walk_and_convert_jupytext_metadata_not_done", False)
        return []
    else:
        return None


def walk_and_convert_jupytext_metadata(
    element=None,
    doc: Doc | None = None,
) -> list | None:
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
    else:
        return None


def convert_cell_output(
    element=None,
    doc: Doc | None = None,
) -> Div | None:
    if (
        isinstance(element, Div)
        and CODE_OUTPUT_CLASSES.issubset(set(element.classes))
        and CODE_CELL_CLASSES.issubset(set(element.parent.classes))
    ):
        content = element.content
        # possible types are CodeBlock, Para, RawBlock
        # Para is images
        has_no_para = True
        for elem in content:
            if isinstance(elem, Para):
                has_no_para = False
                break
        # if there's a Para (which contains an Image), don't touch this and let pandoc decide
        if has_no_para:
            choices: dict[str, RawBlock] = {}
            for elem in content:
                if isinstance(elem, RawBlock):
                    choices[elem.format] = elem
            # if no choices, i.e. only CodeBlock, don't touch this and let pandoc decide
            if choices:
                for input_format in CONVERT_CELL_OUTPUT_PRIORITY:
                    if input_format in choices:
                        elem = choices[input_format]
                        if input_format in RAW_TEX_FORMATS:
                            input_format += "+raw_tex"
                        return convert_text(elem.text, input_format=input_format)
    return None


def remove_cell_input_python(
    element=None,
    doc: Doc | None = None,
) -> list | None:
    """Delete ipynb cell input with python code."""
    if (
        isinstance(element, CodeBlock)
        and element.classes == ["python"]
        and CODE_CELL_CLASSES.issubset(set(element.parent.classes))
    ):
        return []
    else:
        return None


def main(doc: Doc | None = None) -> Any:
    """a pandoc filter converting math in code block.

    Fenced code block with class math will be runned using texp.
    """
    return run_filters(
        [
            walk_and_convert_jupytext_metadata,
            convert_cell_output,
            remove_cell_input_python,
        ],
        doc=doc,
    )


if __name__ == "__main__":
    main()
