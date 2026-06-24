#!/usr/bin/env python3
"""
iterm2_alfred_agent.py — standalone iTerm2 HTTP agent for alfred-iterm2.

Place in: ~/.config/iterm2/AppSupport/Scripts/AutoLaunch/iterm2_alfred_agent.py

Endpoints
─────────
  GET  /health
  GET  /sessions/all                  all open iTerm2 sessions
  POST /sessions/{session_id}/activate  focus a session by its iTerm2 ID
"""

import asyncio
import json
import logging
import sys
import urllib.parse

import iterm2

PORT = 9998
VERSION = "1.0.0"

logging.basicConfig(
    level=logging.INFO,
    format="[iterm2-alfred] %(levelname)s %(message)s",
    stream=sys.stdout,
)
log = logging.getLogger(__name__)

_STATUS_TEXT = {200: "OK", 404: "Not Found", 500: "Internal Server Error"}


def _response(status: int, data: dict) -> bytes:
    body = json.dumps(data).encode("utf-8")
    header = (
        f"HTTP/1.1 {status} {_STATUS_TEXT.get(status, 'Unknown')}\r\n"
        f"Content-Type: application/json\r\n"
        f"Content-Length: {len(body)}\r\n"
        f"Connection: close\r\n\r\n"
    ).encode("utf-8")
    return header + body


async def _parse_request(reader: asyncio.StreamReader):
    try:
        line = await asyncio.wait_for(reader.readline(), timeout=10.0)
    except asyncio.TimeoutError:
        return None, None

    parts = line.decode("utf-8", errors="replace").strip().split(" ", 2)
    if len(parts) < 2:
        return None, None

    method = parts[0].upper()
    path = urllib.parse.unquote(parts[1].split("?")[0])

    # drain headers
    while True:
        try:
            hline = await asyncio.wait_for(reader.readline(), timeout=10.0)
        except asyncio.TimeoutError:
            break
        if hline.strip() == b"":
            break

    return method, path


async def main(connection):
    app = await iterm2.async_get_app(connection)
    log.info("Connected to iTerm2 — listening on http://127.0.0.1:%d", PORT)

    async def _find_session(session_id: str):
        for window in app.windows:
            for tab in window.tabs:
                for session in tab.all_sessions:
                    if session.session_id == session_id:
                        return session
        return None

    async def _route(method: str, path: str):
        if method == "GET" and path == "/health":
            return {"ok": True, "version": VERSION}, 200

        if method == "GET" and path == "/sessions/all":
            result = []
            for window in app.windows:
                for tab in window.tabs:
                    for session in tab.all_sessions:
                        result.append({
                            "session_id": session.session_id,
                            "name": session.name or "",
                        })
            return {"sessions": result}, 200

        parts = path.strip("/").split("/")
        # POST /sessions/{session_id}/activate
        if method == "POST" and len(parts) == 3 \
                and parts[0] == "sessions" and parts[2] == "activate":
            session = await _find_session(parts[1])
            if session is None:
                return {"ok": False, "error": f"No session '{parts[1]}'"}, 404
            await session.async_activate(select_tab=True, order_window_front=True)
            log.info("Activated %s", parts[1])
            return {"ok": True}, 200

        return {"ok": False, "error": f"No route for {method} {path}"}, 404

    async def _handle_client(reader: asyncio.StreamReader, writer: asyncio.StreamWriter):
        try:
            method, path = await _parse_request(reader)
            if method is None:
                return
            resp_data, status = await _route(method, path)
            writer.write(_response(status, resp_data))
            await writer.drain()
        except Exception as exc:
            log.exception("Error: %s", exc)
        finally:
            try:
                writer.close()
                await writer.wait_closed()
            except Exception:
                pass

    server = await asyncio.start_server(_handle_client, "127.0.0.1", PORT)
    async with server:
        await asyncio.Future()


iterm2.run_forever(main)
