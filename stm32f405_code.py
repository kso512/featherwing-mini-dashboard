#pylint: disable=import-error

"""
Python script on the Feather, converting the text file data into a graph and
displaying the graph.

References
* https://learn.adafruit.com/adafruit-stm32f405-feather-express/overview
* https://circuitpython.readthedocs.io/en/latest/shared-bindings/supervisor/__init__.html
* https://circuitpython.readthedocs.io/en/latest/shared-bindings/board/__init__.html
* https://circuitpython.readthedocs.io/en/latest/shared-bindings/digitalio/__init__.html
* https://circuitpython.readthedocs.io/en/latest/shared-bindings/time/__init__.html
* https://circuitpython.readthedocs.io/projects/featherwing/en/latest/index.html
"""

## LIBRARIES
import board
import digitalio
import supervisor
import time
from adafruit_featherwing import minitft_featherwing

## VARIABLES
### DEBUG: Toggle debugging if needed
DEBUG = True
### TXTFILE: File to read information from
TXTFILE = "/hostinfo.txt"
### Pre-defined numbers; keep (LOOPDELAY * LOOPFACTOR) > 60
LOOPCOUNT = 0
LOOPDELAY = 1
LOOPFACTOR = 61
### LASTVALUE; VALUE: Initialize variables to aid in
###  troubleshooting
LASTVALUE = VALUE = "EMPTY"

## CONFIGURATION
### Onboard red LED attached to digital pin 13
led = digitalio.DigitalInOut(board.D13)
led.direction = digitalio.Direction.OUTPUT
### Mini Color TFT with Joystick FeatherWing
minitft = minitft_featherwing.MiniTFTFeatherWing()

## MAIN LOOP
while True:
    ### Disable autoreload
    supervisor.disable_autoreload()
    ### Indicate that we're processing data
    led.value = True
    ### Count loops
    LOOPCOUNT = LOOPCOUNT + 1
    LOOPMOD = LOOPCOUNT % LOOPFACTOR
    if DEBUG:
        print("LOOPCOUNT / LOOPMOD:", LOOPCOUNT, "/", LOOPMOD)
    ### Check for button presses; hold down for LOOPDELAY seconds!
    buttons = minitft.buttons
    if buttons.right:
        print("Button RIGHT!")
    if buttons.down:
        print("Button DOWN!")
    if buttons.left:
        print("Button LEFT!")
    if buttons.up:
        print("Button UP!")
    if buttons.select:
        print("Button SELECT!")
    if buttons.a:
        print("Button A!")
    if buttons.b:
        print("Button B! Toggling DEBUG.")
        if DEBUG:
            DEBUG = False
        else:
            DEBUG = True        
    ### Attempt to open the file
    if DEBUG:
        print("Trying to open file:", TXTFILE)
    try:
        #### Read the file
        with open(TXTFILE, "r") as FP:
            VALUE = FP.read()
            ##### Close the file
            FP.close()
            if DEBUG:
                print("Read and closed file:", TXTFILE)
    ### Handle missing file error
    except OSError as e:
        print("FILE NOT FOUND!")
        OVERRIDE = "RED"
        #### Enable autoreload
        supervisor.enable_autoreload()        
    if DEBUG:
        print("VALUE:", VALUE)

    ### Indicate that we're done processing data
    led.value = False
    ### Pause until it's time to act again
    if DEBUG:
        print("***** Sleeping for", LOOPDELAY, "second(s).")
    time.sleep(LOOPDELAY)
