#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
AUTOLAUNCH="$HOME/.config/iterm2/AppSupport/Scripts/AutoLaunch"

mkdir -p "$AUTOLAUNCH"
cp "$SCRIPT_DIR/iterm2_alfred_agent.py" "$AUTOLAUNCH/iterm2_alfred_agent.py"
echo "✓ Installed agent → $AUTOLAUNCH/iterm2_alfred_agent.py"

echo ""
echo "Next steps:"
echo "1. Restart iTerm2 (or: Scripts → AutoLaunch → iterm2_alfred_agent)"
echo "2. Verify: curl http://127.0.0.1:9998/health"
echo "3. Build and install the Alfred workflow: ./build.sh && open iterm2-session-switcher.alfredworkflow"
