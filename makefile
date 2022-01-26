SHELL = /usr/bin/env bash

_python ?= python
# use pytest-parallel if python < 3.9 else pytest-xdist
# as pytest-parallel is faster but doesn't support python 3.9 yet
# PYTESTARGS ?= $(shell python -c 'import sys; print("--workers auto" if sys.version_info < (3, 9) else "-n auto")')
# for bump2version, valid options are: major, minor, patch
PART ?= patch
N_MPI ?= 2

_pandoc = pandoc
pandocArgs = --toc -M date="`date "+%B %e, %Y"`" --wrap=none
RSTs = CHANGELOG.rst README.rst docs/example-output.rst

# Main Targets #################################################################

.PHONY: test test-mpi docs api clean

docs: $(RSTs)
	$(MAKE) html
api: docs/api/
html: dist/docs/

#  --parallel-mode
test:
	TEXPDEBUG=1 $(_python) \
		-m coverage run \
		-m pytest -vv $(PYTESTARGS) tests
coverage: test
	coverage report
	coverage html

test-mpi:
	mpirun -n $(N_MPI) $(_python) -m pytest -vv --with-mpia \
		--capture=no \
		tests

clean:
	rm -f $(RSTs)

# docs #########################################################################

README.rst: docs/README.md
	printf \
		"%s\n\n" \
		".. This is auto-generated from \`$<\`. Do not edit this file directly." \
		> $@
	cd $(<D); \
	$(_pandoc) $(pandocArgs) $(<F) -V title='pannb Documentation' -s -t rst \
		>> ../$@

docs/%-output.rst: docs/%.ipynb
	PANNBLOGLEVEL=DEBUG pandoc $< -s -o $@ --ipynb-output=all -F pannb -f ipynb-abbreviations+all_symbols_escapable-angle_brackets_escapable-ascii_identifiers+auto_identifiers+autolink_bare_uris+backtick_code_blocks+blank_before_blockquote+blank_before_header+bracketed_spans+citations-compact_definition_lists+definition_lists+east_asian_line_breaks-emoji+escaped_line_breaks+example_lists+fancy_lists+fenced_code_attributes+fenced_code_blocks+fenced_divs+footnotes-four_space_rule-gfm_auto_identifiers+grid_tables-gutenberg-hard_line_breaks+header_attributes-ignore_line_breaks+implicit_figures+implicit_header_references+inline_code_attributes+inline_notes+intraword_underscores-latex_macros+line_blocks+link_attributes-lists_without_preceding_blankline-literate_haskell-markdown_attribute+markdown_in_html_blocks-mmd_header_identifiers-mmd_link_attributes-mmd_title_block+multiline_tables+native_divs+native_spans-old_dashes+pandoc_title_block+pipe_tables-raw_attribute+raw_html+raw_tex-rebase_relative_paths-short_subsuperscripts+shortcut_reference_links+simple_tables+smart+space_in_atx_header-spaced_reference_links+startnum+strikeout+subscript+superscript+task_lists+table_captions+tex_math_dollars-tex_math_double_backslash-tex_math_single_backslash+yaml_metadata_block

%.rst: %.md
	printf \
		"%s\n\n" \
		".. This is auto-generated from \`$<\`. Do not edit this file directly." \
		> $@
	$(_pandoc) $(pandocArgs) $< -s -t rst >> $@

docs/api/:
	sphinx-apidoc \
		--maxdepth 6 \
		--force \
		--separate \
		--module-first \
		--implicit-namespaces \
		--doc-project API \
		--output-dir $@ src/pannb

dist/docs/:
	sphinx-build -E -b dirhtml docs dist/docs
	sphinx-build -b linkcheck docs dist/docs

# maintenance ##################################################################

.PHONY: pypi pypiManual gh-pages pep8 flake8 pylint
# Deploy to PyPI
## by CI, properly git tagged
pypi:
	git push origin v0.1.1
## Manually
pypiManual:
	rm -rf dist
	poetry build
	twine upload dist/*

gh-pages:
	ghp-import --no-jekyll --push dist/docs

# check python styles
pep8:
	pycodestyle . --ignore=E501
flake8:
	flake8 . --ignore=E501
pylint:
	pylint pannb

print-%:
	$(info $* = $($*))

# poetry #######################################################################

setup.py:
	poetry build
	cd dist; tar -xf pannb-0.1.1.tar.gz pannb-0.1.1/setup.py
	mv dist/pannb-0.1.1/setup.py .
	rm -rf dist/pannb-0.1.1

# since poetry doesn't support editable, we can build and extract the setup.py,
# temporary remove pyproject.toml and ask pip to install from setup.py instead.
editable: setup.py
	mv pyproject.toml .pyproject.toml
	$(_python) -m pip install --no-dependencies -e .
	mv .pyproject.toml pyproject.toml

# releasing ####################################################################

bump:
	bump2version $(PART)
	git push --follow-tags

src/pannb/pipeline_serial.py: src/pannb/pipeline.py
	sed -e 's/app_//g' -e 's/.result()//g' $< > $@
