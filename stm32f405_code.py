#pylint: disable=import-error

"""
Python script on the Feather, converting the text file data into a graph and
displaying the graph.

References
https://learn.adafruit.com/adafruit-stm32f405-feather-express/overview
https://circuitpython.readthedocs.io/en/latest/shared-bindings/supervisor/__init__.html
https://circuitpython.readthedocs.io/en/latest/shared-bindings/board/__init__.html
https://circuitpython.readthedocs.io/en/latest/shared-bindings/digitalio/__init__.html
https://circuitpython.readthedocs.io/en/latest/shared-bindings/time/__init__.html
https://circuitpython.readthedocs.io/projects/featherwing/en/latest/index.html
https://circuitpython.readthedocs.io/en/latest/shared-bindings/displayio/__init__.html
"""

## LIBRARIES
import time
import board
import digitalio
import displayio
import supervisor
from adafruit_featherwing import minitft_featherwing

## VARIABLES
### DEBUG: Toggle debugging if needed
DEBUG = True
### TXTFILE: File to read information from
TXTFILE = "/hostinfo.txt"
### Keep (LOOPDELAY * LOOPFACTOR) > 60
### LOOPDELAY: Number of seconds to wait before restarting the main loop
LOOPDELAY = 1
### LOOPFACTOR: Number to divide by and return the remainder of
LOOPFACTOR = 61
### PALETTECOLORS: Number of colors in the palette
PALETTECOLORS = 6
### PALETTE: A palette with PALETTECOLORS colors
PALETTE = displayio.Palette(PALETTECOLORS)
PALETTE[0] = 0x000000 #black
PALETTE[1] = 0xff0000 #red
PALETTE[2] = 0xffff00 #yellow
PALETTE[3] = 0x00ff00 #green
PALETTE[4] = 0x0000ff #blue
PALETTE[5] = 0xffffff #white
### SCREENHEIGHT: Number of screen pixels vertically
SCREENHEIGHT = 80
### SCREENWIDTH: Number of screen pixels horizontally
SCREENWIDTH = 160
### CURRENTCOLOR: Integer color value
CURRENTCOLOR = 0
### COLORLIST: List of integers containing past color values
COLORLIST = [0] * SCREENWIDTH
### LASTVALUE; VALUE; CONDITION: Initialize strings to aid in troubleshooting
LASTVALUE = VALUE = CONDITION = "EMPTY"
### LOOPCOUNT; LOOPMOD: Initialize integers to aid in troubleshooting
LOOPCOUNT = LOOPMOD = 0
### CPUCOUNT; LOAD1: Initialize floats to aid in troubleshooting
CPUCOUNT = LOAD1 = 0.0

## CONFIGURATION
### Onboard red LED attached to digital pin 13
LED = digitalio.DigitalInOut(board.D13)
LED.direction = digitalio.Direction.OUTPUT
### Mini Color TFT with Joystick FeatherWing
MINITFT = minitft_featherwing.MiniTFTFeatherWing()
DISPLAY = MINITFT.display
### Create a bitmap with PALETTECOLORS colors
BITMAP = displayio.Bitmap(SCREENWIDTH, SCREENHEIGHT, PALETTECOLORS)
### Create a TileGrid using the Bitmap and Palette
TILEGRID = displayio.TileGrid(BITMAP, pixel_shader=PALETTE)
### Create a Group
GROUP = displayio.Group()
### Add the TileGrid and label to the Group
GROUP.append(TILEGRID)
### Add the GROUP to the Display
DISPLAY.show(GROUP)

### Fill space with black
for X in range(0, (SCREENWIDTH - 1)):
    for Y in range(0, (SCREENHEIGHT - 1)):
        BITMAP[X, Y] = 0

## MAIN LOOP
while True:
    ### Disable autoreload
    supervisor.disable_autoreload()
    ### Indicate that we're processing data
    LED.value = True
    ### Count loops
    LOOPCOUNT = LOOPCOUNT + 1
    LOOPMOD = LOOPCOUNT % LOOPFACTOR
    if DEBUG:
        print("LOOPCOUNT / LOOPMOD:", LOOPCOUNT, "/", LOOPMOD)
    ### Check for button presses; hold down for LOOPDELAY seconds!
    BUTTONS = MINITFT.buttons
    if BUTTONS.right:
        print("Button RIGHT!")
    if BUTTONS.down:
        print("Button DOWN!")
    if BUTTONS.left:
        print("Button LEFT!")
    if BUTTONS.up:
        print("Button UP!")
    if BUTTONS.select:
        print("Button SELECT!")
    if BUTTONS.a:
        print("Button A!")
    if BUTTONS.b:
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
            CONDITION = "EMPTY"
            if DEBUG:
                print("Read and closed file:", TXTFILE)
    ### Handle missing file error
    except OSError as error_os:
        if DEBUG:
            print("FILE NOT FOUND!")
        CONDITION = "RED"
    if DEBUG:
        print("VALUE:", VALUE)
    ### After > 60 seconds, see if LASTVALUE is EMPTY; if so, set it to the
    ###  new value
    if LOOPMOD == 1:
        if LASTVALUE == VALUE:
            print("VALUE has not changed!")
            if CONDITION == "EMPTY":
                CONDITION = "YELLOW"
            #### Enable autoreload
            supervisor.enable_autoreload()
        else:
            if DEBUG:
                print("LASTVALUE / VALUE:", LASTVALUE, "/", VALUE)
            LASTVALUE = VALUE
            #### Split the string into a list and then tuple
            VALUETUPLE = tuple(VALUE.split())
            if DEBUG:
                print("VALUETUPLE:", VALUETUPLE)
            #### Break the tuple into individual numerical values
            CPUCOUNT = float(VALUETUPLE[0])
            if DEBUG:
                print("CPUCOUNT:", CPUCOUNT)
            LOAD1 = float(VALUETUPLE[1])
            if DEBUG:
                print("LOAD1:", LOAD1)
            PROCESSINFO = VALUETUPLE[4].split('/')
            if DEBUG:
                print("PROCESSINFO:", PROCESSINFO)
            PROCESSTUPLE = tuple(PROCESSINFO)
            if DEBUG:
                print("PROCESSTUPLE:", PROCESSTUPLE)
            PROCESSCOUNT = int(PROCESSTUPLE[0])
            if DEBUG:
                print("PROCESSCOUNT:", PROCESSCOUNT)
            CURRENTTIME = VALUETUPLE[6]
            if DEBUG:
                print("CURRENTTIME:", CURRENTTIME)
            #### Scale load value, which starts as a float that needs to be
            ####  divided by CPUCOUNT, scaled between 0 and 80, multiplied by
            ####  the process count, then rounded to integers.
            LOADONE = int(((LOAD1/CPUCOUNT)*SCREENHEIGHT)*PROCESSCOUNT)
            #### Send integers lower than (SCREENHEIGHT - 1)
            if LOADONE > (SCREENHEIGHT - 1):
                LOADONE = (SCREENHEIGHT - 1)
            if DEBUG:
                print("LOADONE:", LOADONE)
        #### Convert the load values into a color, taking earlier overrides
        ####  into consideration.
        if CONDITION == "RED":
            print("CONDITION RED")
            CURRENTCOLOR = 1
        elif CONDITION == "YELLOW":
            print("CONDITION YELLOW")
            CURRENTCOLOR = 2
        elif LOADONE > 39:
            print("CONDITION GREEN")
            CURRENTCOLOR = 3
        else:
            print("CONDITION BLUE")
            CURRENTCOLOR = 4
        #### Tend the list of colors, removing the first and appending the
        ####  newest.
        if DEBUG:
            print("OLD COLORLIST:", COLORLIST)
        COLORLIST.pop(0)
        COLORLIST.append(CURRENTCOLOR)
        if DEBUG:
            print("NEW COLORLIST:", COLORLIST)
        #### Loop through each column and paint it the color from the list
        for X in range(0, (SCREENWIDTH - 1)):
            for Y in range(0, (SCREENHEIGHT - 1)):
                BITMAP[X, Y] = COLORLIST[X+1]

    ### Indicate that we're done processing data
    LED.value = False
    ### Pause until it's time to act again
    if DEBUG:
        print("***** Sleeping for", LOOPDELAY, "second(s).")
    time.sleep(LOOPDELAY)
