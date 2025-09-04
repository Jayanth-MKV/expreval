from __future__ import annotations

from typing import Any

from exprcalc import main


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
