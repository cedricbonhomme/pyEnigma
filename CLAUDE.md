# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Overview

pyEnigma is a Python simulator of the Enigma cypher machine, usable both as a library (`from pyenigma import enigma, rotor`) and as a CLI (`enigma`). It targets Python ^3.10 and is managed with Poetry.

## Commands

Dependency/build management uses Poetry:

```bash
poetry install                       # install deps + dev tools into a venv
poetry shell                         # enter the venv
```

Tests use nose2 (tests live in `tests/`, plain unittest under the hood):

```bash
poetry run nose2 -v --pretty-assert                  # run all tests
poetry run nose2 -v tests.test_pyenigma.TestpyEnigma.test_encrypt   # single test
```

Linting/formatting is enforced via pre-commit (black, flake8 + bugbear, pyupgrade, reorder-python-imports):

```bash
poetry run pre-commit run --all-files
poetry run flake8 . --count --select=E9,F63,F7,F82 --show-source --statistics   # CI's hard-fail lint
```

Running the CLI:

```bash
echo "Hello World" | poetry run enigma ABC A I II III "AV BS CG DL FU HZ IN KM OW RX"
```

CI runs on sourcehut (`.builds/`): it installs via Poetry, runs the flake8 syntax check, then `nose2`. The canonical repo is on sourcehut (`git.sr.ht/~cedric/pyenigma`); GitHub is a mirror. Issues are tracked at `todo.sr.ht/~cedric/pyenigma`.

## Architecture

Three source modules plus the CLI:

- **`pyenigma/rotor.py`** — `Rotor` and `Reflector` classes, plus module-level instances of every historical rotor/reflector (e.g. `ROTOR_I`, `ROTOR_Reflector_B`). A `Rotor` holds `wiring` (the forward substitution) and derives `rwiring` (the inverse) automatically — note the custom `__setattr__` that rebuilds `rwiring` whenever `wiring` is assigned. `state` is the rotor's current rotational position, `ring` is the Ringstellung, and `notchs` are the turnover positions. Encryption is split into `encipher_right` (signal entering toward the reflector) and `encipher_left` (signal returning), each applying `shift = state - ring` arithmetic mod 26.

- **`pyenigma/enigma.py`** — the `Enigma` class wires everything together: reflector + 3 rotors, an initial `key` (3-letter rotor start positions), `plugs` (plugboard pairs as a space-separated string like `"AV BS CG"`), and `ring`. The plugboard is implemented as a `str.translate` table applied both before and after the rotor pipeline. `encipher()` is the single public operation and is its own inverse (same settings encrypt and decrypt). The rotor stepping/turnover logic lives at the top of the per-character loop in `encipher()`; non-alphabetic characters pass through untouched and original letter case is restored at the end.

- **`bin/enigma.py`** — the CLI entry point (`enigma = "bin.enigma:main"` in `pyproject.toml`). It reads plaintext from stdin and takes settings as positional args in the order: `KEY REF R1 R2 R3 PLUGS [--verbose]`. The `KEY` may optionally carry a Ringstellung suffix (`ABC-DEF`). With `--verbose`, the resulting rotor state line is written to **stderr** so the ciphertext on stdout can still be piped into another `enigma` invocation.

### Key invariant

The substitution is symmetric: enciphering ciphertext with the identical reflector/rotor/key/plug/ring settings yields the original plaintext. The test in `tests/test_pyenigma.py` pins `"Hello World"` → `"Qgqop Vyzxp"` for a fixed configuration; preserve this when modifying rotor/enigma math.
