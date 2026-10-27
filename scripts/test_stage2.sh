#!/bin/sh
python3 src/main.py --vfs ./vfs_data/minimal
python3 src/main.py --vfs ./vfs_data/minimal --script ./scripts/start_stage2.txt