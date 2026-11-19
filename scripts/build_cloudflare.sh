#!/bin/sh
set -eu

# The importer uses commit history to find the latest CSV for each base.
if [ "$(git rev-parse --is-shallow-repository)" = true ]; then
    git fetch --unshallow origin
fi

python3 scripts/import_csv.py
mkdir -p dist
cp index.html data.json dist/
