checkerboard.py: full field flickering 8Hz checkboard in a 20sec on/off block design for 4 minutes.
6 ON / 6 OFF = 12 blocks x 20s = 240 s total.

checkerboard_FovPeriph.py: Foveal/Peripheral alternating checkerboard with interleaved blank blocks.
The block sequence is: blank-Fov-blank-Periph
Foveal is ~3 deg central, while peripheral is 10+ deg.
6 FOV + 6 PERIPHERAL + 12 blank = 24 blocks x 20s = 480 s total.

checkerboard_LR.py: Left/Right alternating checkerboard with interleaved blank blocks.
The block sequence is: blank-LEFT-blank-RIGHT
6 LEFT + 6 RIGHT + 12 blank = 24 blocks x 20s = 480 s total.

EyeLinkCoreGraphicsPsychoPy.py: required in working directory for eye tracking to work.

Prisma_config_1.py: config file for Prisma to set the monitor dimensions, gamma, and eye tracking defaults.
