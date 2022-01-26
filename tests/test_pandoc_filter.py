import unittest

import panflute

from pannb import main


class TestPandocFilter(unittest.TestCase):
    def setUp(self):
        with open("docs/example.ipynb", "r") as f:
            self.text = f.read()
        with open("docs/example-output.rst", "r") as f:
            self.text_ref = f.read()

    def test_pandoc_filter(self):
        doc = panflute.convert_text(self.text, input_format="ipynb-abbreviations+all_symbols_escapable-angle_brackets_escapable-ascii_identifiers+auto_identifiers+autolink_bare_uris+backtick_code_blocks+blank_before_blockquote+blank_before_header+bracketed_spans+citations-compact_definition_lists+definition_lists+east_asian_line_breaks-emoji+escaped_line_breaks+example_lists+fancy_lists+fenced_code_attributes+fenced_code_blocks+fenced_divs+footnotes-four_space_rule-gfm_auto_identifiers+grid_tables-gutenberg-hard_line_breaks+header_attributes-ignore_line_breaks+implicit_figures+implicit_header_references+inline_code_attributes+inline_notes+intraword_underscores-latex_macros+line_blocks+link_attributes-lists_without_preceding_blankline-literate_haskell-markdown_attribute+markdown_in_html_blocks-mmd_header_identifiers-mmd_link_attributes-mmd_title_block+multiline_tables+native_divs+native_spans-old_dashes+pandoc_title_block+pipe_tables-raw_attribute+raw_html+raw_tex-rebase_relative_paths-short_subsuperscripts+shortcut_reference_links+simple_tables+smart+space_in_atx_header-spaced_reference_links+startnum+strikeout+subscript+superscript+task_lists+table_captions+tex_math_dollars-tex_math_double_backslash-tex_math_single_backslash+yaml_metadata_block", standalone=True, extra_args=["--ipynb-output=all"])
        main(doc)
        text = panflute.convert_text(doc, input_format="panflute", output_format="rst", standalone=True)
        assert text == self.text_ref.strip()
