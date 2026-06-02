#!/usr/bin/env bash
set -euo pipefail

cd "$(dirname "$0")/../../evals"
python3 runner.py
