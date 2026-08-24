#!/usr/bin/env python3
import os
from pathlib import Path

from _compat import run_script

os.environ["FARPLANE_NOTIFY_HOME"] = str(Path(__file__).absolute().parent.parent)
run_script("runtime/notify.py")
