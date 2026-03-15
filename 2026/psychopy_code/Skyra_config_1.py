#!/usr/bin/env python
# -*- coding: utf-8 -*-


"""
Projector and eye tracker configuration for Skyra MRI ONLY.
Add this file to the experiment directory and then import it into the experiment script:
    import Skyra_config_x as room_config
        where x is the version of Skyra_config_*.py to import.

Apply the functions in your script with:
    room_config.ApplyMonitorConfig()
    room_config.ApplyEyeLinkDefaults()

Remember to use the defined monitor when creating the window in your script, e.g.:
    win = visual.Window(monitor='my_monitor', size=[1920, 1080], fullscr=True, screen=0)

"""

import numpy, psychopy, pylink
from psychopy import visual, core, monitors
from EyeLinkCoreGraphicsPsychoPy import EyeLinkCoreGraphicsPsychoPy

def ApplyMonitorConfig():

    # Define "full" gamma grid (min,max,gamma,a,b,k)
    gammGrid=numpy.zeros([4,6])
    gammGrid=[[4.918,288.8,2.2109,4.918,0.0078,12.8623],[4.918,59.8,2.5724,4.8080,0.424,4.3288],[4.918,147.1,2.1906,4.918,0.0052,9.6126],[4.918,15.74,2.4422,4.9176,0.0404,2.5999]]

    # Define a monitor without using Monitor Center GUI
    from psychopy.monitors import Monitor
    my_monitor = Monitor(name='my_monitor')
    my_monitor.setSizePix((1920, 1080))
    my_monitor.setWidth(64.0)
    my_monitor.setDistance(89.0)
    my_monitor.setGammaGrid(gammGrid)
    my_monitor.setPsychopyVersion("2023.2.3")
    my_monitor.setLineariseMethod(4) #"Easy" saves as 1 when one provides just min, max, gamma. "Full" saves as 4 when you provide all 6 values to gamma table.
    my_monitor.setNotes("2023.11.16. Lights off in magnet and control rooms. Patch size 1.0. Photometer at foot end of bed. Projector: B:50/C:50/S:15/G:Film 2.2")
    my_monitor.saveMon() #This will save everything to a .json file in C:\Users\username\AppData\Roaming\psychopy3\monitors which is read by Monitor Center.
    
    # Print monitor details
    print("My gamma table: ", my_monitor.getGammaGrid())
    print("My resolution: ", my_monitor.getSizePix())
    print("My width: ", my_monitor.getWidth(), "cm")
    print("My distance: ", my_monitor.getDistance(), "cm")
    print("My linearise method: ", my_monitor.getLinearizeMethod())
    print("My gamma calibration notes: ", my_monitor.getNotes())
    print("Psychopy version used for gamma calibration: ", my_monitor.getPsychopyVersion())


def ApplyEyeLinkDefaults():
    
    el_tracker = pylink.EyeLink("100.1.1.1")
    
    win = visual.Window(fullscr=True,
                    monitor='my_monitor',
                    winType='pyglet',
                    size=[1920, 1080],
                    screen=0,
                    colorSpace='rgb',
                    units='pix')

    # Camera setup
    el_tracker.sendCommand('sample_rate = 1000') #Sample rate: 250, 500, 1000, 2000 Hz.

    # Eye image display
    el_tracker.sendCommand('autothreshold_click = YES') # Mouse autothreshold
    el_tracker.sendCommand('elcl_tt_power 2') # Illuminator level: 1= 100%, 2= 75%, 3 = 50%

    # Tracking
    el_tracker.sendCommand('enable_search_limits = ON') # Use search limits (useful when subject wears glasses). Always enable in Remote Mode (i.e., EEG lab)
    el_tracker.sendCommand('track_search_limits = OFF') # Move search limits (when on, you must click the pupil to re-center the search limits).
    el_tracker.sendCommand('aux_mouse_simulation = NO') # Mouse simulation mode
    el_tracker.sendCommand('pupil_size_diameter = AREA') # Pupil size units: area, diameter

    # Display PC settings
    el_tracker.sendCommand('screen_distance = 870 910') # Eye to screen top/bottom distances.
    # Get the native screen resolution used by PsychoPy
    scn_width, scn_height = win.size
    # Pass the display pixel coordinates (left, top, right, bottom) to the eye tracker
    el_coords = "screen_pixel_coords = 0 0 %d %d" % (scn_width - 1, scn_height - 1)
    # set the native screen resolution
    el_tracker.sendCommand(el_coords)

    # Calibration and validation
    el_tracker.sendCommand("calibration_type = HV9") # Calibration type: H3,HV3,HV5,HV9,HV13. Use HV13 in Remote Mode (always the case in EEG)
    el_tracker.sendCommand('enable_automatic_calibration = YES') # Enable automatic calibration or manual accepting of each point
    el_tracker.sendCommand('automatic_calibration_pacing = 1000') # Pacing interval: Off/500/1000/1500 ms
    el_tracker.sendCommand('randomize_calibration_order = YES') # Randomize calibration order
    el_tracker.sendCommand('randomize_validation_order = YES')  # Randomize validation order
    el_tracker.sendCommand('cal_repeat_first_target = YES') # Repeat the first calibration point at the end
    el_tracker.sendCommand('val_repeat_first_target = YES') # Repeat the last validation point at the end
    el_tracker.sendCommand('calibration_area_proportion 0.55 0.83') # Reduce point spread.
    el_tracker.sendCommand('validation_area_proportion 0.55 0.83') # Reduce point spread.

    # Event and data processing
    el_tracker.sendCommand('recording_parse_type = GAZE') # Parse using Gaze or HREF
    el_tracker.sendCommand('select_parser_configuration 0') # Configure parser's saccade sensitivity: 0=cognitive 1=psychophysical
    el_tracker.sendCommand('heuristic_filter 2 1') # File and Analog Sample filters: 0=Off, 1=Standard, 2=Extra
    el_tracker.sendCommand('file_sample_data = LEFT,RIGHT,GAZE,GAZERES,HREF,PUPIL,AREA,HTARGET,INPUT,STATUS')  # Sample contents of file
    el_tracker.sendCommand('file_event_filter = LEFT,RIGHT,FIXATION,SACCADE,BLINK,MESSAGE,BUTTON,INPUT') # Event contents of file

    # Recording data view
    el_tracker.sendCommand('rec_plot_enabled = NO') # Recording view: Yes=Plot, No=Gaze Cursor
    el_tracker.sendCommand('rec_plot_data = GAZE') # Type of data to plot: Gaze, Angle, HREF, Raw

    win.close()

ApplyMonitorConfig()
