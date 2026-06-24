# alfred-iterm2

Alfred 4 workflow to switch between open iTerm2 sessions by name.

## Requirements

- [iTerm2](https://iterm2.com) with its Python runtime installed  
  *(iTerm2 → Scripts → Manage → Install Python Runtime)*
- Alfred 4 with Powerpack

## Install

**1. Install the iTerm2 agent**

```bash
./install.sh
```

Restart iTerm2 — the agent starts automatically and listens on `localhost:9998`.

**2. Install the Alfred workflow**

Download `iterm2-session-switcher.alfredworkflow` from the [latest release](../../releases/latest) and open it — Alfred imports it automatically.

## Usage

Type `it ` in Alfred → all open iTerm2 panes appear by title → type to filter → press `Enter` to focus.

## HTTP API

| Method | Path | Description |
|--------|------|-------------|
| `GET`  | `/health` | Health check |
| `GET`  | `/sessions/all` | List all open sessions |
| `POST` | `/sessions/{id}/activate` | Focus a session by ID |

---

## Local Development

Build the workflow locally:

```bash
./build.sh
open iterm2-session-switcher.alfredworkflow
```

The `.alfredworkflow` file is a zip containing `info.plist`. `build.sh` generates it via an inline Python script using `plistlib` and `zipfile` — no dependencies required.

To release a new version, push a tag:

```bash
git tag v1.0.0
git push origin main --tags
```

GitHub Actions will build the workflow and attach it to the release automatically.

## License

MIT © Tony Findeisen
