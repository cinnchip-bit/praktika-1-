#!/bin/sh
set -eu
python3 src/main.py --vfs examples/vfs_nested.json \
  --script scripts/demo.txt
