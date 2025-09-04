## [unreleased]

### 🚜 Refactor

- Rename project from exprcalc to expreval; update CI, README, and tests accordingly

## [0.2.0] - 2025-09-04

### 🚀 Features

- Add local hooks for coverage badge generation and update README to use local coverage.svg

### 📚 Documentation

- Add CHANGELOG and coverage badge; ci: add release workflow; test: improve coverage; refactor: wrap evaluate root

### 🧪 Testing

- Expand CLI tests, adjust coverage threshold to 98%; chore: simplify pre-commit config

## [0.1.0] - 2025-09-04

### 🧪 Testing

- Add basic evaluate() test suite with pytest
- _(coverage)_ Add extensive test suite, coverage config, py.typed, CI coverage steps

### ⚙️ Miscellaneous Tasks

- Add project scaffold (config, core evaluator, CLI, docs)
- _(ci)_ Configure pre-commit with Ruff
- Add GitHub Actions workflow for linting and tests
- _(types)_ Add mypy with strict config and CI integration
