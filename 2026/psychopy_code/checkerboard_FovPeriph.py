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
# Foveal/Peripheral alternating checkerboard with interleaved blank blocks
# Block sequence (repeating): blank -> FOVEAL -> blank -> PERIPHERAL
# Foveal    : circular checkerboard within 3° of fixation
# Gap       : 3°–10° — no stimulus presented
# Peripheral: checkerboard annulus from 10° to screen edge
# 6 FOVEAL + 6 PERIPHERAL + 12 blank = 24 blocks x 20s = 480s total
# M Pinsk 20260219

# === Experiment Parameters ===
wait_for_trigger = True   # Set to True if waiting for MRI trigger
checker_size    = 0.75     # Size of each checker in degrees
flicker_rate    = 8        # Hz
duration        = 480      # Total run duration in seconds
block_duration  = 20       # Duration of each block in seconds
foveal_radius         = 1.0   # Degrees — outer edge of foveal stimulus
peripheral_inner_radius = 10.0  # Degrees — inner edge of peripheral stimulus (gap: 3°–10°)

# Block sequence (repeating unit of 4):
BLOCK_SEQUENCE = [0, 1, 0, 2]   # 0=blank, 1=foveal, 2=peripheral

# Create Monitor and Window
mon = Monitor('my_monitor')
win = visual.Window(monitor='my_monitor', size=[1920, 1080], fullscr=True, screen=0)

screen_width_pix, screen_height_pix = win.size
screen_width_cm    = mon.getWidth()
viewing_distance_cm = mon.getDistance()

deg_per_cm       = (180 / np.pi) * (1 / viewing_distance_cm)
screen_width_deg = screen_width_cm * deg_per_cm
screen_height_deg = screen_width_deg * (screen_height_pix / screen_width_pix)

# Full grid of checker positions (centred on fixation)
num_cols = int(screen_width_deg  / checker_size)
num_rows = int(screen_height_deg / checker_size)

# Build all positions and colours for the full grid
all_positions = []
all_colors    = []

for i in range(num_cols):
    for j in range(num_rows):
        x = (i - num_cols / 2) * checker_size
        y = (j - num_rows / 2) * checker_size
        all_positions.append([x, y])
        all_colors.append([1, 1, 1] if (i + j) % 2 == 0 else [-1, -1, -1])

all_positions = np.array(all_positions)
all_colors    = np.array(all_colors)

# Split into foveal (eccentricity < foveal_radius) and peripheral
eccentricities = np.sqrt(all_positions[:, 0]**2 + all_positions[:, 1]**2)
foveal_mask    = eccentricities <  foveal_radius
periph_mask    = eccentricities >= peripheral_inner_radius

positions_foveal = all_positions[foveal_mask]
colors_foveal    = all_colors[foveal_mask]

positions_periph = all_positions[periph_mask]
colors_periph    = all_colors[periph_mask]

# Create ElementArrayStim objects
checkerboard_foveal = visual.ElementArrayStim(
    win=win,
    units="deg",
    nElements=len(positions_foveal),
    elementTex=None,
    elementMask=None,
    xys=positions_foveal,
    sizes=checker_size,
    colors=colors_foveal,
)

checkerboard_periph = visual.ElementArrayStim(
    win=win,
    units="deg",
    nElements=len(positions_periph),
    elementTex=None,
    elementMask=None,
    xys=positions_periph,
    sizes=checker_size,
    colors=colors_periph,
)

# Fixation cross (drawn every frame)
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
frame_time = 1 / (2 * flicker_rate)

clock.reset()
while clock.getTime() < duration:
    current_time = clock.getTime()
    block_number = int(current_time // block_duration)
    block_type   = BLOCK_SEQUENCE[block_number % len(BLOCK_SEQUENCE)]

    if block_type == 1:       # FOVEAL
        checkerboard_foveal.colors *= -1
        checkerboard_foveal.draw()
    elif block_type == 2:     # PERIPHERAL
        checkerboard_periph.colors *= -1
        checkerboard_periph.draw()
    # block_type == 0: BLANK — just fixation

    fixation.draw()
    win.flip()

    core.wait(frame_time)

    if "q" in event.getKeys():
        break

# === Cleanup ===
win.close()
core.quit()
