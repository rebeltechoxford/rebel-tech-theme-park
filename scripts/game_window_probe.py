"""
Planet Coaster 1 — read-only Windows window and screenshot probe.

Requires: Windows, Python 3.9+ and 'mss' ONLY for --capture.
Does not click, type, focus, resize, start, stop, or otherwise alter game/UI.
Does not include machine-identifying paths or screenshots in Git.

Usage from repo root:
    python scripts/game_window_probe.py
    python scripts/game_window_probe.py --capture

With --capture, saves one screenshot of Planet Coaster's CLIENT AREA only
if that game's own window is currently foreground. Screen overlays on top of
the game can appear in screen grabs, so check the image before sharing.
"""
import argparse
import ctypes
import json
import os
import sys
from ctypes import wintypes
from pathlib import Path

if sys.platform != "win32":
    raise SystemExit("Windows-only desktop probe.")

user32 = ctypes.WinDLL("user32", use_last_error=True)
kernel32 = ctypes.WinDLL("kernel32", use_last_error=True)

class POINT(ctypes.Structure):
    _fields_ = [("x", wintypes.LONG), ("y", wintypes.LONG)]

class RECT(ctypes.Structure):
    _fields_ = [
        ("left", wintypes.LONG), ("top", wintypes.LONG),
        ("right", wintypes.LONG), ("bottom", wintypes.LONG),
    ]

ENUMPROC = ctypes.WINFUNCTYPE(wintypes.BOOL, wintypes.HWND, wintypes.LPARAM)
user32.EnumWindows.argtypes = [ENUMPROC, wintypes.LPARAM]
user32.EnumWindows.restype = wintypes.BOOL
user32.GetWindowThreadProcessId.argtypes = [wintypes.HWND, ctypes.POINTER(wintypes.DWORD)]
user32.GetWindowThreadProcessId.restype = wintypes.DWORD
user32.IsWindowVisible.argtypes = [wintypes.HWND]
user32.IsWindowVisible.restype = wintypes.BOOL
user32.GetForegroundWindow.restype = wintypes.HWND
user32.GetClientRect.argtypes = [wintypes.HWND, ctypes.POINTER(RECT)]
user32.GetClientRect.restype = wintypes.BOOL
user32.ClientToScreen.argtypes = [wintypes.HWND, ctypes.POINTER(POINT)]
user32.ClientToScreen.restype = wintypes.BOOL
kernel32.OpenProcess.argtypes = [wintypes.DWORD, wintypes.BOOL, wintypes.DWORD]
kernel32.OpenProcess.restype = wintypes.HANDLE
kernel32.CloseHandle.argtypes = [wintypes.HANDLE]
kernel32.QueryFullProcessImageNameW.argtypes = [
    wintypes.HANDLE, wintypes.DWORD, wintypes.LPWSTR, ctypes.POINTER(wintypes.DWORD)
]
kernel32.QueryFullProcessImageNameW.restype = wintypes.BOOL
PROCESS_QUERY_LIMITED_INFORMATION = 0x1000

def executable_basename(pid):
    handle = kernel32.OpenProcess(PROCESS_QUERY_LIMITED_INFORMATION, False, pid)
    if not handle:
        return None
    try:
        buf = ctypes.create_unicode_buffer(32768)
        size = wintypes.DWORD(len(buf))
        if kernel32.QueryFullProcessImageNameW(handle, 0, buf, ctypes.byref(size)):
            return os.path.basename(buf.value).lower()
    finally:
        kernel32.CloseHandle(handle)
    return None

def windows_for_game():
    found = []
    @ENUMPROC
    def visit(hwnd, _):
        if not user32.IsWindowVisible(hwnd):
            return True
        pid = wintypes.DWORD()
        user32.GetWindowThreadProcessId(hwnd, ctypes.byref(pid))
        if executable_basename(pid.value) != "planetcoaster.exe":
            return True
        bounds = RECT()
        origin = POINT(0, 0)
        if not user32.GetClientRect(hwnd, ctypes.byref(bounds)):
            return True
        if not user32.ClientToScreen(hwnd, ctypes.byref(origin)):
            return True
        width = bounds.right - bounds.left
        height = bounds.bottom - bounds.top
        if width < 200 or height < 200:
            return True
        found.append({
            "hwnd": int(hwnd),
            "pid": pid.value,
            "bounds": {"left": origin.x, "top": origin.y,
                       "width": width, "height": height},
            "foreground": int(hwnd) == int(user32.GetForegroundWindow()),
        })
        return True
    if not user32.EnumWindows(visit, 0):
        raise OSError("EnumWindows failed")
    return found

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--capture", action="store_true",
                    help="Save a screenshot ONLY when Planet Coaster is foreground")
    args = ap.parse_args()
    game_windows = windows_for_game()
    result = {
        "status": "GAME_NOT_RUNNING" if not game_windows else "GAME_WINDOW_FOUND",
        "windows": game_windows,
        "capture": "not_requested" if not args.capture else "skipped",
    }
    if args.capture:
        active = next((w for w in game_windows if w["foreground"]), None)
        if not active:
            result["capture"] = "skipped: Planet Coaster is not the foreground window"
        else:
            from mss import MSS
            from mss.tools import to_png
            area = active["bounds"]
            out = Path(__file__).resolve().parents[1] / "build" / "probe"
            out.mkdir(parents=True, exist_ok=True)
            path = out / "planetcoaster-foreground.png"
            with MSS() as sct:
                shot = sct.grab(area)
                to_png(shot.rgb, shot.size, output=str(path))
            result["capture"] = "saved locally to build/probe/planetcoaster-foreground.png"
            result["size"] = path.stat().st_size
    print(json.dumps(result, indent=2))
    return 0

if __name__ == "__main__":
    sys.exit(main())
