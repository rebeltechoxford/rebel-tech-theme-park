"""One bounded relative mouse-camera movement; keeps the existing control lease checks."""
import sys, time
from pathlib import Path
ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'scripts'))
import pc2_desktop_control as control
button, dx, dy = sys.argv[1], int(sys.argv[2]), int(sys.argv[3])
if button not in {'middle', 'right'} or max(abs(dx), abs(dy)) > 450:
    raise SystemExit('Invalid bounded camera request')
ctx = control.context()
control.point(ctx, 960, 540)
down, up = {'middle': (0x20, 0x40), 'right': (0x8, 0x10)}[button]
control.u.mouse_event(down, 0, 0, 0, 0)
try:
    time.sleep(.15)
    last_x = last_y = 0
    for i in range(1, 31):
        control.context()
        x, y = round(dx*i/30), round(dy*i/30)
        control.u.mouse_event(0x1, (x-last_x)&0xffffffff, (y-last_y)&0xffffffff, 0, 0)
        last_x, last_y = x, y
        time.sleep(.025)
finally:
    control.u.mouse_event(up, 0, 0, 0, 0)
print('RELATIVE_CAMERA_STEP_COMPLETE', button, dx, dy)
