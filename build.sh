#!/usr/bin/env bash
set -euo pipefail

cd "$(dirname "$0")"

python3 - <<'PYEOF'
import plistlib, zipfile
from pathlib import Path

BUNDLE_ID = "com.tfindeisen.iterm2-session-switcher"
SF_UID    = "C1A2B3D4-0001-0001-0001-000000000001"
RS_UID    = "C1A2B3D4-0002-0002-0002-000000000002"

plist = {
    "bundleid": BUNDLE_ID,
    "name": "iTerm2 Session Switcher",
    "description": "Switch to any open iTerm2 session by name",
    "category": "Tools",
    "createdby": "Tony Findeisen",
    "readme": "", "webaddress": "",
    "version": "1.0.0",
    "disabled": False,
    "objects": [
        {
            "type": "alfred.workflow.input.scriptfilter",
            "uid": SF_UID, "version": 3,
            "config": {
                "keyword": "it",
                "withspace": True,
                "argumenttype": 1,
                "argumenttrimmode": 0,
                "argumenttreatemptyqueryasnil": False,
                "title": "iTerm2 Sessions",
                "subtext": "",
                "runningsubtext": "Loading sessions…",
                "script": 'python3 sessions.py "{query}"',
                "scriptfile": "",
                "type": 0,
                "scriptargtype": 0,
                "alfredfiltersresults": False,
                "alfredfiltersresultsmatchmode": 0,
                "queuemode": 1,
                "queuedelaymode": 0,
                "queuedelaycustom": 3,
                "queuedelayimmediatelyinitially": True,
                "escaping": 102,
            },
        },
        {
            "type": "alfred.workflow.action.script",
            "uid": RS_UID, "version": 2,
            "config": {
                "script": 'curl -sf -X POST "http://127.0.0.1:9998/sessions/{query}/activate"\n',
                "scriptfile": "",
                "type": 0,
                "scriptargtype": 0,
                "concurrently": False,
                "escaping": 102,
            },
        },
    ],
    "connections": {
        SF_UID: [
            {"destinationuid": RS_UID, "modifiers": 0, "modifiersubtext": "", "vitoclose": True}
        ]
    },
    "uidata": {
        SF_UID: {"xpos": 150.0, "ypos": 50.0},
        RS_UID: {"xpos": 450.0, "ypos": 50.0},
    },
}

out = Path("iterm2-session-switcher.alfredworkflow")
with zipfile.ZipFile(out, "w", zipfile.ZIP_DEFLATED) as zf:
    zf.writestr("info.plist", plistlib.dumps(plist, fmt=plistlib.FMT_XML).decode())
    zf.write("sessions.py")

print(f"Built {out}  ({out.stat().st_size} bytes)")
PYEOF
