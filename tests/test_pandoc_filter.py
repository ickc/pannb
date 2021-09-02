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
        doc = panflute.convert_text(self.text, input_format="ipynb", standalone=True)
        main(doc)
        text = panflute.convert_text(doc, input_format="panflute", output_format="rst", standalone=True)
        assert text == self.text_ref.strip()
