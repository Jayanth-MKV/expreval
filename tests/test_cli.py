from __future__ import annotations

from typing import Any

from expreval import main


def test_cli_success(capsys: Any) -> None:
    code = main(["2+2*3"])  # 2 + 6
    captured = capsys.readouterr()
    assert code == 0
    assert captured.out.strip() == "8.0"


def test_cli_error(capsys: Any) -> None:
    code = main(["unknown_func(1)"])
    captured = capsys.readouterr()
    assert code == 2
    assert "error:" in captured.err


def test_cli_help(capsys: Any) -> None:
    code = main(["--help"])
    captured = capsys.readouterr()
    assert code == 0
    assert "Usage:" in captured.out


def test_cli_empty_args(capsys: Any) -> None:
    code = main([])
    captured = capsys.readouterr()
    assert code == 0
    assert "Usage:" in captured.out


def test_cli_success_complex(capsys: Any) -> None:
    code = main(["sin(pi/2)+1"])  # 1 + 1
    captured = capsys.readouterr()
    assert code == 0
    assert captured.out.strip() == "2.0"


def test_cli_stdout_capture() -> None:
    import io
    from contextlib import redirect_stdout

    buf = io.StringIO()
    with redirect_stdout(buf):
        rc = main(["1+2"])  # prints 3.0
    assert rc == 0
    assert buf.getvalue().strip() == "3.0"
