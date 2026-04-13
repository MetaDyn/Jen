#!/usr/bin/env python3
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent
cmd = [str(ROOT / 'metadyn_crm.py'), 'list-companies', *sys.argv[1:]]
raise SystemExit(subprocess.call(cmd))
