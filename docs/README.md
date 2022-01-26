---
title:	pannb—pandoc filter for ipynb
...

[![Documentation Status](https://readthedocs.org/projects/pannb/badge/?version=latest)](https://pannb.readthedocs.io/en/latest/?badge=latest&style=plastic)
[![Documentation Status](https://github.com/ickc/pannb/workflows/GitHub%20Pages/badge.svg)](https://ickc.github.io/pannb)

![GitHub Actions](https://github.com/ickc/pannb/workflows/Python%20package/badge.svg)
[![Coverage Status](https://codecov.io/gh/ickc/pannb/branch/master/graphs/badge.svg?branch=master)](https://codecov.io/github/ickc/pannb)
[![Coverage Status](https://coveralls.io/repos/ickc/pannb/badge.svg?branch=master&service=github)](https://coveralls.io/r/ickc/pannb)
[![Codacy Code Quality Status](https://img.shields.io/codacy/grade/078ebc537c5747f68c1d4ad3d3594bbf.svg)](https://www.codacy.com/app/ickc/pannb)
[![Scrutinizer Status](https://img.shields.io/scrutinizer/quality/g/ickc/pannb/master.svg)](https://scrutinizer-ci.com/g/ickc/pannb/)
[![CodeClimate Quality Status](https://codeclimate.com/github/ickc/pannb/badges/gpa.svg)](https://codeclimate.com/github/ickc/pannb)

[![Supported versions](https://img.shields.io/pypi/pyversions/pannb.svg)](https://pypi.org/project/pannb)
[![Supported implementations](https://img.shields.io/pypi/implementation/pannb.svg)](https://pypi.org/project/pannb)
[![PyPI Wheel](https://img.shields.io/pypi/wheel/pannb.svg)](https://pypi.org/project/pannb)
[![PyPI Package latest release](https://img.shields.io/pypi/v/pannb.svg)](https://pypi.org/project/pannb)
[![GitHub Releases](https://img.shields.io/github/tag/ickc/pannb.svg?label=github+release)](https://github.com/ickc/pannb/releases)
[![Development Status](https://img.shields.io/pypi/status/pannb.svg)](https://pypi.python.org/pypi/pannb/)
[![Downloads](https://img.shields.io/pypi/dm/pannb.svg)](https://pypi.python.org/pypi/pannb/)
[![Commits since latest release](https://img.shields.io/github/commits-since/ickc/pannb/v0.1.1.svg)](https://github.com/ickc/pannb/compare/v0.1.1...master)
![License](https://img.shields.io/pypi/l/pannb.svg)

[![Conda Recipe](https://img.shields.io/badge/recipe-pannb-green.svg)](https://anaconda.org/conda-forge/pannb)
[![Conda Downloads](https://img.shields.io/conda/dn/conda-forge/pannb.svg)](https://anaconda.org/conda-forge/pannb)
[![Conda Version](https://img.shields.io/conda/vn/conda-forge/pannb.svg)](https://anaconda.org/conda-forge/pannb)
[![Conda Platforms](https://img.shields.io/conda/pn/conda-forge/pannb.svg)](https://anaconda.org/conda-forge/pannb)

# Introduction

Pandoc supports ipynb format. What this does is add support of

1. jupytext style yaml metadata block
2. filter out the Python code block
3. convert raw block to native pandoc AST, e.g.
    - if a cell outputs HTML, then it is an HTML raw block by default, meaning only HTML-like output formats contains these output cells. This filter convert them using pandoc itself to native pandoc AST so that any output formats will contains the same output.

These 3 filters are implemented as 3 individual functions, so that you can cherry-pick your own combinations (See [API doc](../api/pannb/)). The command line program `pannb` have all 3 included.

# Example

See `docs/example.ipynb` for the input notebook and its [output without the filter](../example/) and [output with the filter](../example-output/). Note that the output will be correct only if you set `--ipynb-output=html` after [this patch is merged](https://github.com/jgm/pandoc/pull/7538).
