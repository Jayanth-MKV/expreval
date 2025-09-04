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
def test_basic(expr: str, expected: float) -> None:
    assert evaluate(expr) == pytest.approx(expected)


def test_name_error() -> None:
    with pytest.raises(NameError):
        evaluate("unknown_func(2)")


def test_unsupported_syntax() -> None:
    with pytest.raises(TypeError):
        evaluate("(lambda x: x)(2)")  # lambdas not allowed


def test_unsupported_operator() -> None:
    # Floor division '//' not allowed
    with pytest.raises(TypeError):
        evaluate("5//2")


def test_unary_plus() -> None:
    assert evaluate("+5") == pytest.approx(5.0)


def test_unary_minus() -> None:
    assert evaluate("-5") == pytest.approx(-5.0)


def test_keyword_arguments_disallowed() -> None:
    with pytest.raises(TypeError):
        evaluate("log(x=2)")  # keyword usage not supported


def test_non_name_call_disallowed() -> None:
    # (sin)(0) builds an ast.Call with ast.Name so still ok; use attribute to force rejection
    with pytest.raises(TypeError):
        evaluate("math.sin(0)")  # attribute access not allowed


def test_name_not_found() -> None:
    with pytest.raises(NameError):
        evaluate("unknown + 2")


def test_unsupported_literal() -> None:
    with pytest.raises(TypeError):
        evaluate("'hi'")


def test_unknown_function_call() -> None:
    with pytest.raises(NameError):
        evaluate("foo(1)")


def test_unsupported_syntax_generic() -> None:
    with pytest.raises(TypeError):
        evaluate("[1,2,3]")  # list nodes not supported


def test_expression_wrapper_branch() -> None:
    # Ensures the ast.Expression branch is traversed (already by any evaluate call after change)
    assert evaluate("1+1") == pytest.approx(2.0)


def test_cli_error_message_format(monkeypatch: object) -> None:
    # Induce NameError to ensure 'error:' prefix path is covered
    from exprcalc import main as cli_main

    class DummyArgs(list):
        pass

    # Using direct call
    code = cli_main(["doesnotexist(1)"])
    assert code == 2
