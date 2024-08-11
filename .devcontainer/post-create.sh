#!/bin/sh
set -e
python -m venv /venv
. /venv/bin/activate
cd /workspaces/pykrotik
pip install -e ".[dev]"
