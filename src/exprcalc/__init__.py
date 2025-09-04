"""exprcalc: Minimal, robust Python library for any math expressions

Current focus: a minimal, dependency‑free function `evaluate()` that can compute
pure math expressions using Python's `math` module and a small safe AST walk.

Example:
    >>> evaluate("sin(pi/2) + log(e)")
    2.0

NOT a full sandbox yet: it's intentionally very small. Only direct names from
`math` (no attributes, no comprehensions, no lambdas, etc.) are accepted.
"""

from __future__ import annotations

import ast
import math
import operator
import sys
from typing import Any

__all__ = ["evaluate", "main"]

_ALLOWED_FUNCS: dict[str, Any] = {
    name: getattr(math, name) for name in dir(math) if not name.startswith("_")
}
_ALLOWED_NAMES: dict[str, Any] = {"pi": math.pi, "e": math.e, **_ALLOWED_FUNCS}

_BIN_OPS = {
    ast.Add: operator.add,
    ast.Sub: operator.sub,
    ast.Mult: operator.mul,
    ast.Div: operator.truediv,
    ast.Pow: operator.pow,
    ast.Mod: operator.mod,
}
_UNARY_OPS = {ast.USub: operator.neg, ast.UAdd: operator.pos}


def evaluate(expression: str) -> float:
    """Evaluate a math expression and return a float.

    Supported:
        * Literals: ints, floats
        * Binary ops: + - * / % **
        * Unary   : + -
        * Calls to functions in `math`
        * Names: pi, e, math function names

    Parameters
    ----------
    expression: str
        The expression to evaluate, e.g. "sin(pi/4)**2".
    """

    tree = ast.parse(expression, mode="eval")

    def _eval(node: ast.AST) -> float:
        if isinstance(node, ast.Expression):
            return _eval(node.body)
        if isinstance(node, ast.Constant):
            if isinstance(node.value, int | float):
                return float(node.value)
            raise TypeError(f"unsupported literal: {node.value!r}")
        if isinstance(node, ast.BinOp):
            op_type = type(node.op)
            if op_type not in _BIN_OPS:
                raise TypeError(f"unsupported operator: {op_type.__name__}")
            return _BIN_OPS[op_type](_eval(node.left), _eval(node.right))
        if isinstance(node, ast.UnaryOp):
            op_type = type(node.op)
            if op_type not in _UNARY_OPS:
                raise TypeError(f"unsupported unary operator: {op_type.__name__}")
            return _UNARY_OPS[op_type](_eval(node.operand))
        if isinstance(node, ast.Name):
            try:
                return float(_ALLOWED_NAMES[node.id])
            except KeyError as exc:
                raise NameError(node.id) from exc
        if isinstance(node, ast.Call):
            if not isinstance(node.func, ast.Name):
                raise TypeError("only direct function names allowed")
            func_name = node.func.id
            func = _ALLOWED_FUNCS.get(func_name)
            if func is None:
                raise NameError(func_name)
            args = [_eval(a) for a in node.args]
            if node.keywords:
                raise TypeError("keyword arguments not supported")
            return float(func(*args))
        raise TypeError(
            f"unsupported syntax: {ast.dump(node, include_attributes=False)}"
        )

    return _eval(tree.body)


def main(argv: list[str] | None = None) -> int:
    """Minimal CLI.

    Usage:
        exprcalc "sin(pi/2) + 1"  # prints result
    """

    if argv is None:
        argv = sys.argv[1:]
    if not argv or argv[0] in {"-h", "--help"}:
        print("Usage: exprcalc <expression>")
        return 0
    expr = " ".join(argv)
    try:
        val = evaluate(expr)
    except Exception as exc:  # keep simple for now
        print(f"error: {exc}", file=sys.stderr)
        return 2
    print(val)
    return 0


if __name__ == "__main__":  # pragma: no cover
    raise SystemExit(main())
