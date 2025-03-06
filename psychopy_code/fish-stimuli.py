from psychopy import visual, core, event, plugins
from psychopy.monitors import Monitor  # import Monitor correctly
import numpy as np
plugins.activatePlugins()

import Prisma_config_1 as room_config
room_config.ApplyMonitorConfig()
room_config.ApplyEyeLinkDefaults()

# For NEU350 Ambrosini
# Written in PsychoPy v2023.2.3
# Must install psychopy-visionscience plugin in Tools->plugins/packages manager.
# M Pinsk 20250219

# Experiment parameters
wait_for_trigger = True  # Set to False if you don't want to wait for MRI trigger
duration = 4 * 60  # Total duration in seconds
block_duration = 20  # Duration of each ON/OFF block
rotation_speed = 0.25  # Degrees per frame (adjust for speed preference)

# Create a Monitor Object
mon = Monitor('my_monitor')  # Ensure this is configured in PsychoPy settings

# Create a window
win = visual.Window(monitor='my_monitor', size=[1920, 1080], fullscr=True, screen=0)

# If waiting for MRI trigger
if wait_for_trigger:
    waiting_text = visual.TextStim(win, text="Waiting for MRI start trigger...", color='black', height=0.1)
    waiting_text.draw()
    win.flip()

    event.clearEvents()  # Clear any previous keypresses
    keys = event.waitKeys(keyList=['equal'])  # Wait for equal sign
    print("Key pressed:", keys)

    if 'q' in keys:  # Quit if 'q' is pressed
        win.close()
        core.quit()

# Create a fixation point
fixation = visual.TextStim(win, text='+', color='black', height=0.12)

# Create stimulus
checkerboard1 = visual.RadialStim(
win = win,
units='deg',
colorSpace='rgb',
size=17,
texRes = 512,
angularRes = 512,
tex="sqrXsqr",
color = 1,
contrast = 1,
pos = (0,0),
visibleWedge= (0,360),
mask = 'circle',
radialCycles = 2.5, # 5 rings
angularCycles= 10, # 20 slices
radialPhase = 0,
angularPhase = 0,
)

# Experiment timing setup
clock = core.Clock()
total_blocks = duration // block_duration
on_blocks = [i for i in range(total_blocks) if i % 2 == 1]  # ON blocks

# Main experiment loop
clock.reset()
block_index = 0
while clock.getTime() < duration:
    current_time = clock.getTime()
    block_number = int(current_time // block_duration)
    is_on_block = block_number in on_blocks
    fixation.draw()

    if is_on_block:
        # Determine rotation direction
        direction = 1 if (block_number // 2) % 2 == 0 else -1
        checkerboard1.ori += direction * rotation_speed # Rotate
        checkerboard1.draw()     
    
    fixation.draw()
    win.flip()
    
    # Check for quit event
    if 'q' in event.getKeys():
        break
    
    core.wait(1 / 60.0) # Wait for 1 frame (16.67 ms at 60Hz) for stable timing/smoother visual

# Cleanup
win.close()
core.quit()
