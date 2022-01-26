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
	PANNBLOGLEVEL=DEBUG pandoc $< -s -o $@ --ipynb-output=all -F pannb

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
	# sphinx-build -b linkcheck docs dist/docs

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
