from psychopy import visual, core, event, plugins
from psychopy.monitors import Monitor
import numpy as np
plugins.activatePlugins()

import Prisma_config_1 as room_config
room_config.ApplyMonitorConfig()
room_config.ApplyEyeLinkDefaults()

# For NEU350 Ambrosini
# Written in PsychoPy v2023.2.3
# Must install psychopy-visionscience plugin in Tools->plugins/packages manager.
# Left/Right alternating checkerboard with interleaved blank blocks
# Block sequence (repeating): blank -> LEFT -> blank -> RIGHT
# 6 LEFT + 6 RIGHT + 12 blank = 24 blocks x 20s = 480s total
# M Pinsk 20260219

# === Experiment Parameters ===
wait_for_trigger = True  # Set to True if waiting for MRI trigger
checker_size = 0.75       # Size of each checker in degrees
flicker_rate = 8          # Hz (times per second the checkerboard inverts)
duration = 480            # Total duration in seconds (24 blocks x 20s)
block_duration = 20       # Duration of each block in seconds

# Block sequence (repeating unit of 4):
#   0 = blank, 1 = LEFT, 2 = blank, 3 = RIGHT
BLOCK_SEQUENCE = [0, 1, 0, 2]  # indices into this list cycle with modulo 4
BLANK = 0
LEFT  = 1
RIGHT = 2

# Create a Monitor Object
mon = Monitor('my_monitor')

# Create a window
win = visual.Window(monitor='my_monitor', size=[1920, 1080], fullscr=True, screen=0)

# Get screen size in pixels
screen_width_pix, screen_height_pix = win.size

# Get monitor physical dimensions
screen_width_cm = mon.getWidth()
viewing_distance_cm = mon.getDistance()

# Convert screen size to degrees
deg_per_cm = (180 / np.pi) * (1 / viewing_distance_cm)
screen_width_deg = screen_width_cm * deg_per_cm
screen_height_deg = screen_width_deg * (screen_height_pix / screen_width_pix)

# Compute number of checkers across the full field.
# Force num_cols even so that half_cols splits symmetrically and the +0.5
# offset always places the midline boundary between two columns, never on one.
num_cols = int(screen_width_deg / checker_size)
if num_cols % 2 != 0:
    num_cols -= 1
num_rows = int(screen_height_deg / checker_size)
half_cols = num_cols // 2

# --- Build LEFT checkerboard (columns 0 .. half_cols-1) ---
positions_left = []
colors_left = []
for i in range(half_cols):
    for j in range(num_rows):
        # +0.5 offset ensures no checker is centred at x=0 or y=0;
        # the left/right boundary falls between columns at the midline.
        x = (i - num_cols / 2 + 0.5) * checker_size
        y = (j - num_rows / 2 + 0.5) * checker_size
        positions_left.append([x, y])
        colors_left.append([1, 1, 1] if (i + j) % 2 == 0 else [-1, -1, -1])

# --- Build RIGHT checkerboard (columns half_cols .. num_cols-1) ---
positions_right = []
colors_right = []
for i in range(half_cols, num_cols):
    for j in range(num_rows):
        x = (i - num_cols / 2 + 0.5) * checker_size
        y = (j - num_rows / 2 + 0.5) * checker_size
        positions_right.append([x, y])
        colors_right.append([1, 1, 1] if (i + j) % 2 == 0 else [-1, -1, -1])

# Create ElementArrayStim objects
checkerboard_left = visual.ElementArrayStim(
    win=win,
    units="deg",
    nElements=len(positions_left),
    elementTex=None,
    elementMask=None,
    xys=positions_left,
    sizes=checker_size,
    colors=colors_left,
)

checkerboard_right = visual.ElementArrayStim(
    win=win,
    units="deg",
    nElements=len(positions_right),
    elementTex=None,
    elementMask=None,
    xys=positions_right,
    sizes=checker_size,
    colors=colors_right,
)

# Fixation cross (drawn every frame regardless of block type)
fixation = visual.TextStim(win, text='+', color='black', height=0.12)

# === Wait for MRI Trigger (if enabled) ===
if wait_for_trigger:
    waiting_text = visual.TextStim(win, text="Waiting for MRI start trigger...", color='black', height=0.1)
    waiting_text.draw()
    win.flip()

    event.clearEvents()
    keys = event.waitKeys(keyList=['equal'])
    print("Key pressed:", keys)

    if 'q' in keys:
        win.close()
        core.quit()

# === Main Loop ===
clock = core.Clock()
frame_time = 1 / (2 * flicker_rate)  # Time per flicker phase

clock.reset()
while clock.getTime() < duration:
    current_time = clock.getTime()
    block_number = int(current_time // block_duration)
    block_type = BLOCK_SEQUENCE[block_number % len(BLOCK_SEQUENCE)]

    if block_type == LEFT:
        checkerboard_left.colors *= -1
        checkerboard_left.draw()
    elif block_type == RIGHT:
        checkerboard_right.colors *= -1
        checkerboard_right.draw()
    # BLANK: draw nothing except fixation below

    fixation.draw()
    win.flip()

    core.wait(frame_time)

    if "q" in event.getKeys():
        break

# === Cleanup ===
win.close()
core.quit()
