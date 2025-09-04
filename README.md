<div align="center">
<img src="https://raw.githubusercontent.com/Jayanth-MKV/expreval/refs/heads/main/assets/logo.png" alt="expreval logo" width="100">

<i>Expreval, A Minimal, robust Python library for any math expressions</i>

<br/>
<!-- Coverage badge (dynamic via Codecov). Replace 'YOUR_ORG' if repo under org -->
<!-- <a href="https://codecov.io/gh/Jayanth-MKV/expreval">
	<img src="https://codecov.io/gh/Jayanth-MKV/expreval/branch/main/graph/badge.svg" alt="Coverage status" />
</a> -->

<img alt="coverage" src="https://raw.githubusercontent.com/Jayanth-MKV/expreval/refs/heads/main/assets/coverage.svg" />

<br/>
<a href="CHANGELOG.md">Changelog</a>

</div>

Minimal. Single function. No dependencies. You give a string with a numeric expression; it returns a float.

## Install

```bash
pip install expreval
```

## Quick use

```python
from expreval import evaluate
evaluate("sin(pi/2) + log(e)")  # 2.0
```

CLI:

```bash
expreval "sin(pi/4)**2"
```

## What works now

- Numbers: int / float literals
- Operators: + - \* / % \*\* and unary + -
- Grouping: ( )
- Names: pi, e, any function from the standard `math` module (sin, cos, sqrt, log, ...)
- Simple function calls with positional arguments only

That is all - for now.

## Safety (current scope)

Only a hand‑written walk over Python's `ast` for a very small subset. No attribute access, no imports, no keywords, no assignments, no lambdas, no comprehensions. If it's not listed above it should raise an error.

## API

```python
evaluate(expression: str) -> float
```

Returns a float (even if you pass an int literal). Raises standard Python exceptions (`NameError`, `TypeError`, etc.) for invalid input.

## Examples

```python
evaluate("2*(3+4)-5/2")        # 11.5
evaluate("sin(pi/6)**2")       # 0.249999... (floating point)
evaluate("sqrt(2)**2")         # 2.000000...
```

## Why

Original itch: certain very large numeric expressions (or results) caused `numexpr` to raise errors in our workflow. For simple scalar math that shouldn't fail, we just needed a tiny, predictable evaluator that:

- Has zero heavy dependencies
- Doesn't optimize or chunk arrays (so no surprise shape / size limits)
- Always returns a plain Python float for valid math
- Is easy to audit (a short AST walk) and extend later if truly needed

So `expreval` exists to reliably handle those "big result" cases where bringing in `numexpr` (and hitting its internal limits) was overkill. If you only need quick scalar math, this keeps it boring and dependable.

## Contributor Guide

```
uv venv
uv sync

# make changes and then run these 

# to create coverage logo and changelogs
.\scripts\update.sh

# (Optional)to bump version for release
uv run scripts\bump_version.py <X.Y.Z>

```


## License

MIT. See `LICENSE`.
