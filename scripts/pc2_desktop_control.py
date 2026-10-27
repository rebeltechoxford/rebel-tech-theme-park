"""Supervised Planet Coaster 2 desktop input. Windows only.

Runs on Raven after PC2 is foreground; restricts input to game window.
Usage:
  python scripts/pc2_desktop_control.py click 432 770
  python scripts/pc2_desktop_control.py key ESC
  python scripts/pc2_desktop_control.py capture
  python scripts/pc2_desktop_control.py scroll -3
  python scripts/pc2_desktop_control.py drag 100 100 500 100 1.0

Stores screenshot locally in ignored build/probe/; does not share screenshots.
Coordinate inputs are client-area pixels, not unverified screen coordinates.
"""
import argparse
import ctypes
import json
import os
import sys
import time
from ctypes import wintypes
from pathlib import Path

if sys.platform != "win32":
    raise SystemExit("Windows only")

u = ctypes.WinDLL("user32", use_last_error=True)
k = ctypes.WinDLL("kernel32", use_last_error=True)
u.GetForegroundWindow.restype = wintypes.HWND
u.GetWindowThreadProcessId.argtypes = (wintypes.HWND, ctypes.POINTER(wintypes.DWORD))
u.GetWindowThreadProcessId.restype = wintypes.DWORD
u.GetWindowTextLengthW.argtypes = (wintypes.HWND,)
u.GetWindowTextLengthW.restype = ctypes.c_int
u.GetWindowTextW.argtypes = (wintypes.HWND, wintypes.LPWSTR, ctypes.c_int)
u.GetWindowTextW.restype = ctypes.c_int
u.GetClientRect.argtypes = (wintypes.HWND, ctypes.POINTER(wintypes.RECT))
u.GetClientRect.restype = wintypes.BOOL
u.ClientToScreen.argtypes = (wintypes.HWND, ctypes.POINTER(wintypes.POINT))
u.ClientToScreen.restype = wintypes.BOOL
u.SetCursorPos.argtypes = (ctypes.c_int, ctypes.c_int)
u.SetCursorPos.restype = wintypes.BOOL
u.mouse_event.argtypes = (wintypes.DWORD, wintypes.DWORD, wintypes.DWORD, wintypes.DWORD, ctypes.c_size_t)
u.keybd_event.argtypes = (ctypes.c_ubyte, ctypes.c_ubyte, wintypes.DWORD, ctypes.c_size_t)

def context():
    hwnd = u.GetForegroundWindow()
    length = u.GetWindowTextLengthW(hwnd)
    name = ctypes.create_unicode_buffer(length + 1)
    u.GetWindowTextW(hwnd, name, length + 1)
    if "Planet Coaster 2" not in name.value:
        # A newly started terminal can steal focus. Explicitly focus only
        # the verified, exact-title game window, then re-check before input.
        u.FindWindowW.argtypes = (wintypes.LPCWSTR, wintypes.LPCWSTR)
        u.FindWindowW.restype = wintypes.HWND
        u.SetForegroundWindow.argtypes = (wintypes.HWND,)
        u.SetForegroundWindow.restype = wintypes.BOOL
        u.ShowWindow.argtypes = (wintypes.HWND, ctypes.c_int)
        target = u.FindWindowW(None, "Planet Coaster 2")
        if not target:
            raise RuntimeError("Input blocked: no Planet Coaster 2 window to focus")
        u.ShowWindow(target, 9)
        if not u.SetForegroundWindow(target):
            # ALT key gesture is a standard Windows foreground activation
            # workaround for input initiated by an authorized user session.
            u.keybd_event(0x12, 0, 0, 0)
            u.SetForegroundWindow(target)
            u.keybd_event(0x12, 0, 0x0002, 0)
        time.sleep(0.3)
        hwnd = u.GetForegroundWindow()
        length = u.GetWindowTextLengthW(hwnd)
        name = ctypes.create_unicode_buffer(length + 1)
        u.GetWindowTextW(hwnd, name, length + 1)
    if "Planet Coaster 2" not in name.value:
        raise RuntimeError("Input blocked: foreground window is not Planet Coaster 2 (got title %r)" % name.value)
    pid = wintypes.DWORD()
    u.GetWindowThreadProcessId(hwnd, ctypes.byref(pid))
    proc = k.OpenProcess(0x1000, False, pid.value)
    if not proc:
        raise RuntimeError("Input blocked: process cannot be verified")
    try:
        k.QueryFullProcessImageNameW.argtypes = (wintypes.HANDLE, wintypes.DWORD, wintypes.LPWSTR, ctypes.POINTER(wintypes.DWORD))
        k.QueryFullProcessImageNameW.restype = wintypes.BOOL
        buffer = ctypes.create_unicode_buffer(32768)
        size = wintypes.DWORD(len(buffer))
        if not k.QueryFullProcessImageNameW(proc, 0, buffer, ctypes.byref(size)):
            raise RuntimeError("Input blocked: could not resolve process executable")
        if os.path.basename(buffer.value).lower() != "planetcoaster2.exe":
            raise RuntimeError("Input blocked: wrong executable %r" % buffer.value)
    finally:
        k.CloseHandle(proc)
    rect = wintypes.RECT()
    origin = wintypes.POINT(0, 0)
    if not u.GetClientRect(hwnd, ctypes.byref(rect)) or not u.ClientToScreen(hwnd, ctypes.byref(origin)):
        raise RuntimeError("Unable to resolve game client bounds")
    width, height = rect.right - rect.left, rect.bottom - rect.top
    return {"hwnd": int(hwnd), "pid": pid.value, "title": name.value,
            "left": origin.x, "top": origin.y, "width": width, "height": height}

def point(ctx, x, y):
    if not (0 <= x < ctx["width"] and 0 <= y < ctx["height"]):
        raise ValueError(f"Out of client-area bounds: {(x, y)} vs {(ctx['width'],ctx['height'])}")
    if not u.SetCursorPos(ctx["left"] + x, ctx["top"] + y):
        raise RuntimeError("Failed to move cursor")

def click(ctx, x, y):
    point(ctx, x, y)
    time.sleep(0.15)
    u.mouse_event(0x0002, 0, 0, 0, 0)
    time.sleep(0.10)
    u.mouse_event(0x0004, 0, 0, 0, 0)

def key(ctx, kname):
    keys = {"ESC":0x1b, "ENTER":0x0d, "SPACE":0x20, "TAB":0x09, "F1":0x70,
            "F2":0x71, "F3":0x72, "F4":0x73, "BACKSPACE":0x08, "LEFT":0x25,
            "RIGHT":0x27, "UP":0x26, "DOWN":0x28}
    vk = keys.get(kname.upper())
    if vk is None and len(kname)==1 and kname.isalnum():
        vk = ord(kname.upper())
    if vk is None:
        raise ValueError("Unsupported key: " + kname)
    u.keybd_event(vk, 0, 0, 0)
    time.sleep(0.10)
    u.keybd_event(vk, 0, 0x0002, 0)

def type_replace(ctx, value):
    # Replace the text in a text entry that has already been focused in-game.
    # No clipboard use, no modifier left held down.
    u.VkKeyScanW.argtypes = (wintypes.WCHAR,)
    u.VkKeyScanW.restype = ctypes.c_short
    u.keybd_event(0x11, 0, 0, 0)  # CTRL down
    time.sleep(.04)
    u.keybd_event(0x41, 0, 0, 0)  # A down
    time.sleep(.05)
    u.keybd_event(0x41, 0, 0x0002, 0)
    u.keybd_event(0x11, 0, 0x0002, 0)  # CTRL up
    time.sleep(.10)
    for ch in value:
        code = u.VkKeyScanW(ch)
        if code == -1:
            raise ValueError(f"Cannot type character: {ch!r}")
        vk = code & 0xff
        mods = (code >> 8) & 0xff
        if mods & 1:
            u.keybd_event(0x10, 0, 0, 0) # SHIFT down
        u.keybd_event(vk, 0, 0, 0)
        time.sleep(.048)
        u.keybd_event(vk, 0, 0x0002, 0)
        if mods & 1:
            u.keybd_event(0x10, 0, 0x0002, 0)
        time.sleep(.037)

def capture(ctx):
    from mss import mss
    from mss.tools import to_png
    out = Path(__file__).resolve().parents[1] / "build" / "probe"
    out.mkdir(parents=True, exist_ok=True)
    path = out / "pc2-current.png"
    with mss() as sct:
        shot = sct.grab({"left":ctx["left"],"top":ctx["top"],"width":ctx["width"],"height":ctx["height"]})
        to_png(shot.rgb, shot.size, output=str(path))
    return {"path":str(path), "bytes":path.stat().st_size}

def main():
    pa=argparse.ArgumentParser()
    pa.add_argument("action", choices=["status","click","capture","key","scroll","drag","type-replace","move"])
    pa.add_argument("params", nargs="*")
    a=pa.parse_args()
    ctx=context()
    if a.action == "click":
        x,y=map(int,a.params)
        click(ctx,x,y)
    elif a.action == "move":
        x,y=map(int,a.params)
        point(ctx,x,y)
    elif a.action=="key":
        key(ctx,a.params[0])
    elif a.action=="type-replace":
        type_replace(ctx, " ".join(a.params))
    elif a.action=="scroll":
        n=int(a.params[0])
        u.mouse_event(0x0800,0,0,(n*120)&0xffffffff,0)
    elif a.action=="drag":
        x1,y1,x2,y2=map(int,a.params[:4])
        duration=float(a.params[4]) if len(a.params)>4 else 1.0
        point(ctx,x1,y1)
        time.sleep(.12)
        u.mouse_event(0x0002,0,0,0,0)
        steps=max(5,int(duration*25))
        for i in range(steps):
            x=round(x1+(x2-x1)*(i+1)/steps)
            y=round(y1+(y2-y1)*(i+1)/steps)
            point(ctx,x,y)
            time.sleep(duration/steps)
        u.mouse_event(0x0004,0,0,0,0)
    result={"action":a.action,"game_pid":ctx["pid"],"resolution":[ctx["width"],ctx["height"]],"ok":True}
    if a.action=="capture":
        result.update(capture(ctx))
    print(json.dumps(result))
if __name__=="__main__":
    main()
