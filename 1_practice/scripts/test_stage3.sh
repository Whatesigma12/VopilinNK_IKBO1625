#!/bin/sh
python3 src/main.py --vfs ./vfs_data/minimal --script ./scripts/start_stage2.txt
python3 src/main.py --vfs ./vfs_data/multi --script ./scripts/start_stage2.txt
python3 src/main.py --vfs ./vfs_data/deep --script ./scripts/start_stage2.txt
python3 src/main.py --vfs ./vfs_data/not_found