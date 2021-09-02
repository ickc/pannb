---
title:	pannb—pandoc filter for ipynb
...

``` {.table}
---
header: false
markdown: true
include: badges.csv
...
```

# Introduction

Pandoc supports ipynb format. What this does is add support of

1. jupytext style yaml metadata block
2. filter out the Python code block
3. convert raw block to native pandoc AST, e.g.
    - if a cell outputs HTML, then it is an HTML raw block by default, meaning only HTML-like output formats contains these output cells. This filter convert them using pandoc itself to native pandoc AST so that any output formats will contains the same output.

These 3 filters are implemented as 3 individual functions, so that you can cherry-pick your own combinations (See [API doc](../api/pannb/)). The command line program `pannb` have all 3 included.

# Example

See `docs/example.ipynb` for the input notebook and its [output without the filter](../example/) and [output with the filter](../example-output/). Note that the output will be correct only if you set `--ipynb-output=html` after [this patch is merged](https://github.com/jgm/pandoc/pull/7538).
