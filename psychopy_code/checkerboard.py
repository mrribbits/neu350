from psychopy import visual, core, event, plugins
from psychopy.monitors import Monitor  # import Monitor correctly
import numpy as np
plugins.activatePlugins()

#import Prisma_config_1 as room_config
#room_config.ApplyMonitorConfig()
#room_config.ApplyEyeLinkDefaults()

# === Experiment Parameters ===
wait_for_trigger = True  # Set to True if waiting for MRI trigger
checker_size = 0.75  # Size of each checker in degrees
flicker_rate = 8  # Hz (times per second the checkerboard inverts)
duration = 240  # Total duration in seconds
block_duration = 20  # Duration of each ON/OFF block (seconds)

# Create a Monitor Object
mon = Monitor('my_monitor')  # Ensure this is configured in PsychoPy settings

# Create a window
win = visual.Window(monitor='my_monitor', size=[1920, 1080], fullscr=True, screen=0)

# Get screen size in pixels
screen_width_pix, screen_height_pix = win.size  

# Get monitor physical dimensions
screen_width_cm = mon.getWidth()  # Monitor width in cm
viewing_distance_cm = mon.getDistance()  # Viewing distance in cm

# Convert screen size to degrees using trigonometry
deg_per_cm = (180 / np.pi) * (1 / viewing_distance_cm)  # Degrees per cm
screen_width_deg = screen_width_cm * deg_per_cm
screen_height_deg = screen_width_deg * (screen_height_pix / screen_width_pix)  # Maintain aspect ratio

# Compute number of checkers that fit in width & height
num_cols = int(screen_width_deg / checker_size)
num_rows = int(screen_height_deg / checker_size)

# Generate positions and alternating colors
positions = []
colors = []

for i in range(num_cols):
    for j in range(num_rows):
        x = (i - num_cols / 2) * checker_size
        y = (j - num_rows / 2) * checker_size
        positions.append([x, y])
        colors.append([1, 1, 1] if (i + j) % 2 == 0 else [-1, -1, -1])  # Alternate colors

# Create the checkerboard as an ElementArrayStim
checkerboard = visual.ElementArrayStim(
    win=win,
    units="deg",
    nElements=len(positions),
    elementTex=None,  # No texture, just solid colors
    elementMask=None,
    xys=positions,
    sizes=checker_size,
    colors=colors,
)

# Create a fixation point
fixation = visual.TextStim(win, text='+', color='black', height=0.12)

# === Wait for MRI Trigger (if enabled) ===
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

# Flickering Loop with Blocks
clock = core.Clock()
frame_time = 1 / (2 * flicker_rate)  # Time per phase (black->white or white->black)
total_blocks = duration // block_duration
on_blocks = [i for i in range(total_blocks) if i % 2 == 1]  # ON blocks

clock.reset()
while clock.getTime() < duration:
    current_time = clock.getTime()
    block_number = int(current_time // block_duration)
    is_on_block = block_number in on_blocks

    if is_on_block:
        checkerboard.colors *= -1  # Invert colors for flicker effect
        checkerboard.draw()
    
    fixation.draw()  # Draw fixation point always
    win.flip()
    
    core.wait(frame_time)
    
    # Check for quit key
    if "q" in event.getKeys():
        break

# === Cleanup ===
win.close()
core.quit()
