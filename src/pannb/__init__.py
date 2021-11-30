"""A panflute filter that process ipynb inputs."""

from __future__ import annotations

import os
from logging import getLogger
from typing import TYPE_CHECKING

from panflute.elements import CodeBlock, Div, Doc, Para, RawBlock
from panflute.io import run_filters
from panflute.tools import convert_text

if TYPE_CHECKING:
    from typing import Any, Callable, Optional, Union

    from panflute.base import Element

logger = getLogger(__name__)

RAW_TEX_FORMATS = {"latex", "textile", "html", "ipynb"}
CODE_CELL_CLASSES = {"cell", "code"}
CODE_OUTPUT_CLASSES = {"output", "execute_result"}

#: priority for converting from raw-block format to AST
#: markdown first because if exist, it is likely considered a source format to be converted from
CONVERT_CELL_OUTPUT_PRIORITY = ("markdown", "html", "latex")

#: specify extra pandoc args used when calling convert_text
PANNBPANDOCARGS: list[str] = os.environ.get("PANNBPANDOCARGS", "").split()

__version__: str = "0.1.1"


def convert_jupytext_metadata(raw_block: RawBlock, doc: Doc) -> list | None:
    """Overwrite doc.metadata by jupytext-style metadata."""
    # overwrite
    meta = convert_text(raw_block.text, standalone=True, extra_args=PANNBPANDOCARGS)
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
                        return convert_text(elem.text, input_format=input_format, extra_args=PANNBPANDOCARGS)
    return None


def remove_code_cell_classes(
    element=None,
    doc: Doc | None = None,
) -> Div | None:
    """Remove code-cell classes from code-cell.

    Pandoc by default inject a CSS that indent class with code.
    Doing this will remove that from from output code cells,
    hence also remove that extra indentation.
    """
    if isinstance(element, Div) and CODE_CELL_CLASSES.issubset(set(element.classes)):
        return Div(
            *element.content,
            identifier=element.identifier,
            classes=[cls for cls in element.classes if cls not in CODE_CELL_CLASSES],
            attributes=element.attributes,
        )


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


#: A tuple of filters (functions)
#: equiv. to the pannb cli, but provided as a Python interface
FILTERS: tuple[Callable[[Optional[Element], Optional[Doc]], Union[Element, list, None]], ...] = (
    walk_and_convert_jupytext_metadata,
    convert_cell_output,
    remove_cell_input_python,
    remove_code_cell_classes,
)


def main(doc: Doc | None = None) -> Any:
    """a pandoc filter converting math in code block.

    Fenced code block with class math will be runned using texp.
    """
    return run_filters(FILTERS, doc=doc)


if __name__ == "__main__":
    main()
