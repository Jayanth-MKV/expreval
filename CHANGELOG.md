# Changelog

All notable changes to this project will be documented in this file.

The format loosely follows Keep a Changelog and Semantic Versioning.

## [0.1.0] - 2025-09-04
### Added
- Initial release: minimal safe math expression evaluator (`evaluate`).
- CLI entry point `exprcalc`.
- Extensive test suite (25 tests) with 96% coverage.
- Strict typing (mypy) and distributed `py.typed` marker.
- CI: lint, format, type-check, tests, coverage.

### Internal / Tooling
- Ruff for lint/format.
- Coverage reporting enforced (fail under 90%).
- Pre-commit hooks (ruff + mypy).

[0.1.0]: https://github.com/Jayanth-MKV/exprcalc/releases/tag/v0.1.0
