#!/usr/bin/env python3
"""Alfred Script Filter — lists iTerm2 sessions, filtered by query."""

import json
import sys
import urllib.request

PORT = 9998
query = " ".join(sys.argv[1:]).strip().lower()


def matches(name: str) -> bool:
    if not query:
        return True
    return all(word in name.lower() for word in query.split())


try:
    with urllib.request.urlopen(
        f"http://127.0.0.1:{PORT}/sessions/all", timeout=3
    ) as r:
        data = json.load(r)
except Exception:
    print(json.dumps({"items": [{
        "title": "iTerm2 agent not running",
        "subtitle": "Launch iterm2_alfred_agent in iTerm2 → Scripts",
        "valid": False,
    }]}))
    sys.exit(0)

items = []
for s in data.get("sessions", []):
    name = (s.get("name") or "").strip() or s["session_id"][:8]
    if matches(name):
        items.append({
            "uid":   s["session_id"],
            "title": name,
            "arg":   s["session_id"],
            "valid": True,
        })

print(json.dumps({"items": items}))
