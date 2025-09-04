<div align="center">
<img src="assets/logo.png" alt="exprcalc logo" width="100">


<i>Exprcalc, A Minimal, robust Python library for any math expressions</i>

<br/>
<!-- Coverage badge placeholder; replace with Codecov after enabling -->
<img alt="coverage" src="https://img.shields.io/badge/coverage-96%25-brightgreen" />
<br/>
<a href="CHANGELOG.md">Changelog</a>

</div>

Minimal. Single function. No dependencies. You give a string with a numeric expression; it returns a float.

## Install

```bash
pip install exprcalc
```

## Quick use

```python
from exprcalc import evaluate
evaluate("sin(pi/2) + log(e)")  # 2.0
```

CLI:

```bash
exprcalc "sin(pi/4)**2"
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

So `exprcalc` exists to reliably handle those "big result" cases where bringing in `numexpr` (and hitting its internal limits) was overkill. If you only need quick scalar math, this keeps it boring and dependable.

## License

MIT. See `LICENSE`.
