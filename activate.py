#!/usr/bin/env python3
"""Alfred Run Script — activates the selected iTerm2 session."""

import sys
import urllib.request

PORT = 9998
session_id = sys.argv[1].strip() if len(sys.argv) > 1 else ""

if not session_id:
    sys.exit(0)

try:
    req = urllib.request.Request(
        f"http://127.0.0.1:{PORT}/sessions/{session_id}/activate",
        method="POST",
    )
    urllib.request.urlopen(req, timeout=5)
except Exception as e:
    with open("/tmp/alfred-iterm2-activate.log", "w") as f:
        f.write(f"session_id: {session_id}\nerror: {e}\n")
    sys.exit(1)
