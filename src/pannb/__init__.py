"""A panflute filter that process ipynb inputs."""

from __future__ import annotations

import os
from typing import TYPE_CHECKING

from panflute.elements import CodeBlock, Div, Doc, Para, RawBlock
from panflute.io import run_filters
from panflute.tools import convert_text

from .util import setup_logging

if TYPE_CHECKING:
    from typing import Any

    from panflute.elements import CodeBlock, Doc

logger = setup_logging()

RAW_TEX_FORMATS = {"latex", "textile", "html", "ipynb"}
CODE_CELL_CLASSES = {"cell", "code"}
CODE_OUTPUT_CLASSES = {"output", "execute_result"}

#: priority for converting from raw-block format to AST
#: markdown first because if exist, it is likely considered a source format to be converted from
CONVERT_CELL_OUTPUT_PRIORITY = ("markdown", "html", "latex")

#: specify extra pandoc args used when calling convert_text
PANNBPANDOCARGS: list[str] = os.environ.get("PANNBPANDOCARGS", "").split()

__version__: str = "0.1.3"


def prepare_jupytext_metadata(
    doc: Doc | None,
) -> None:
    """Replace doc metadata with jupytext metadata."""
    if (
        doc is not None
        and (content := doc.content)
        and isinstance(div := content[0], Div)
        and len(div.content) == 1
        and isinstance((raw_block := div.content[0]), RawBlock)
        and raw_block.format == "ipynb"
    ):
        # overwrite
        meta = convert_text(raw_block.text, standalone=True, extra_args=PANNBPANDOCARGS)
        if metadata := meta._metadata:
            doc._metadata = metadata
            del content[0]
            logger.debug("Overwritten doc metadata by jupytext's: %s", doc.get_metadata())


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
        (
            convert_cell_output,
            remove_cell_input_python,
            remove_code_cell_classes,
        ),
        prepare=prepare_jupytext_metadata,
        doc=doc,
    )


if __name__ == "__main__":
    main()
