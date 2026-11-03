#!/usr/bin/env python3
"""C5 — full pipeline: ingest -> engine -> site -> curation, one receipt."""
import subprocess, sys
steps = [
    (["python3","scripts/scrape.py","--smoke"],  "SMOKE_OK"),
    (["python3","scripts/engine_test.py"],       "ENGINE_OK"),
    (["python3","scripts/build_site.py"],        "SITE_OK"),
    (["python3","scripts/curate.py","--selftest"],"CURATION_OK"),
]
for cmd, want in steps:
    r = subprocess.run(cmd, capture_output=True, text=True, timeout=240)
    if r.returncode != 0 or want not in (r.stdout + r.stderr):
        print("FULL_FAIL at %s: %s" % (cmd[1], (r.stdout+r.stderr)[-200:]))
        sys.exit(1)
print("FULL_OK all 4 layers verified=true")
