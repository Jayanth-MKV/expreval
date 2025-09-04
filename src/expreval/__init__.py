"""expreval: Minimal, robust Python library for any math expressions

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
from collections.abc import Callable
from typing import Any

__all__ = ["evaluate", "main", "__version__"]

__version__ = "0.1.0"

_ALLOWED_FUNCS: dict[str, Any] = {
    name: getattr(math, name) for name in dir(math) if not name.startswith("_")
}
_ALLOWED_NAMES: dict[str, Any] = {"pi": math.pi, "e": math.e, **_ALLOWED_FUNCS}

_BIN_OPS: dict[type, Callable[[float, float], float]] = {
    ast.Add: operator.add,
    ast.Sub: operator.sub,
    ast.Mult: operator.mul,
    ast.Div: operator.truediv,
    ast.Pow: operator.pow,
    ast.Mod: operator.mod,
}
_UNARY_OPS: dict[type, Callable[[float], float]] = {
    ast.USub: operator.neg,
    ast.UAdd: operator.pos,
}


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
            op_obj = node.op
            op_type: type[ast.operator] = type(op_obj)
            func = _BIN_OPS.get(op_type)
            if func is None:
                raise TypeError(f"unsupported operator: {op_type.__name__}")
            return func(_eval(node.left), _eval(node.right))
        if isinstance(node, ast.UnaryOp):
            uop_obj = node.op  # ast.unaryop instance
            uop_type = type(uop_obj)
            ufunc = _UNARY_OPS.get(uop_type)
            if ufunc is None:
                raise TypeError(f"unsupported unary operator: {uop_type.__name__}")
            return ufunc(_eval(node.operand))
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

    # Call on the root Expression to exercise the ast.Expression branch for coverage
    return _eval(tree)


def main(argv: list[str] | None = None) -> int:
    """Minimal CLI.

    Usage:
        expreval "sin(pi/2) + 1"  # prints result
    """

    if argv is None:
        argv = sys.argv[1:]
    if not argv or argv[0] in {"-h", "--help"}:
        print("Usage: expreval <expression>")
        return 0
    expr = " ".join(argv)
    try:
        val = evaluate(expr)
    except Exception as exc:  # keep simple for now
        print(f"error: {exc}", file=sys.stderr)
        return 2
    # Return via print to stdout; separated for easier testing
    print(val)
    return 0


if __name__ == "__main__":  # pragma: no cover
    raise SystemExit(main())
