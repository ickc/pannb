# Revision history for `pannb`

- v0.1.3: fix `README.rst`: use hard-coded links to guarantee it compiles everywhere (including PyPI)
- v0.1.2: minor improvements
    - support pandoc 2.17 and drop older pandoc: improvements in ipynb handling made in upstream. See [pandoc 2.17 release notes](https://github.com/jgm/pandoc/releases/tag/2.17).
    - speed up by rewriting `walk_and_convert_jupytext_metadata` using a prepare function `prepare_jupytext_metadata` instead.

    v0.1.2 is not publishable to PyPI as the `README.rst` has directives.

- v0.1.1: support pandoc 2.15–16 where its ipynb reader/writer are improved (See <https://github.com/jgm/pandoc/releases/tag/2.15>) and is required here.
- v0.1.0: first release and proof of concept.