import math

import pytest

from exprcalc import evaluate


@pytest.mark.parametrize(
    "expr,expected",
    [
        ("1", 1.0),
        ("2+3*4", 14.0),
        ("(2+3)*4", 20.0),
        ("sin(pi/2)", 1.0),
        ("sin(pi/6)**2", math.sin(math.pi / 6) ** 2),
        ("sqrt(2)**2", 2.0),
        ("log(e)", 1.0),
        ("2*(3+4)-5/2", 11.5),
    ],
)
def test_basic(expr, expected):
    assert evaluate(expr) == pytest.approx(expected)


def test_name_error():
    with pytest.raises(NameError):
        evaluate("unknown_func(2)")


def test_unsupported_syntax():
    with pytest.raises(TypeError):
        evaluate("(lambda x: x)(2)")  # lambdas not allowed
