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
import board
import digitalio
import displayio
import supervisor
import time
from adafruit_featherwing import minitft_featherwing

## VARIABLES
### DEBUG: Toggle debugging if needed
DEBUG = True
### TXTFILE: File to read information from
TXTFILE = "/hostinfo.txt"
### LOOPCOUNT: Number of times the main loops has been run
LOOPCOUNT = 0
### Keep (LOOPDELAY * LOOPFACTOR) > 60
### LOOPDELAY: Number of seconds to wait before restarting the main loop
LOOPDELAY = 1
### LOOPFACTOR: Number to divide by and return the remainder of
LOOPFACTOR = 61
### PALETTE: A palette with 5 colors
PALETTE = displayio.Palette(8)
PALETTE[0] = 0x000000 #black
PALETTE[1] = 0xff0000 #red
PALETTE[2] = 0xffff00 #yellow
PALETTE[3] = 0x00ff00 #green
PALETTE[4] = 0x0000ff #blue
### CURRENTCOLOR: Integer color value
CURRENTCOLOR = 0
### COLORLIST: List of integers containing past color values
COLORLIST = [0] * 160
### LASTVALUE; VALUE; LOOPMOD; CONDITION: Initialize variables to aid in
###  troubleshooting
LASTVALUE = VALUE = LOOPMOD = CONDITION = "EMPTY"

## CONFIGURATION
### Onboard red LED attached to digital pin 13
led = digitalio.DigitalInOut(board.D13)
led.direction = digitalio.Direction.OUTPUT
### Mini Color TFT with Joystick FeatherWing
minitft = minitft_featherwing.MiniTFTFeatherWing()
display = minitft.display
### Create a bitmap with five colors
bitmap = displayio.Bitmap(160, 80, 5)
### Fill space with black
for x in range(0, 159):
    for y in range(0, 79):
        bitmap[x, y] = 0

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
    ### Create a TileGrid using the Bitmap and Palette
    tile_grid = displayio.TileGrid(bitmap, pixel_shader=PALETTE)
    ### Create a Group
    group = displayio.Group()
    ### Add the TileGrid to the Group
    group.append(tile_grid)
    ### Add the Group to the Display
    display.show(group)
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
            CONDITION = "EMPTY"
            if DEBUG:
                print("Read and closed file:", TXTFILE)
    ### Handle missing file error
    except OSError as e:
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
            LOAD1 = float(VALUETUPLE[1])
            PROCESSINFO = VALUETUPLE[4].split('/')
            PROCESSTUPLE = tuple(PROCESSINFO)
            PROCESSCOUNT = int(PROCESSTUPLE[0])
            if DEBUG:
                print("LOAD1:", LOAD1, "/ PROCESSCOUNT:", PROCESSCOUNT)
            #### Scale load value, which starts as a float that needs to be
            ####  divided by CPUCOUNT, scaled between 0 and 80, multiplied by
            ####  the process count, then rounded to integers.
            LOADONE = int( ( ( LOAD1 / CPUCOUNT ) * 80 ) * PROCESSCOUNT )
            #### Send integers lower than 79
            if LOADONE > 79:
                LOADONE = 79
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
        for x in range(0,159):
            for y in range(0,79):
                bitmap[x, y] = COLORLIST[x+1]
    ### Indicate that we're done processing data
    led.value = False
    ### Pause until it's time to act again
    if DEBUG:
        print("***** Sleeping for", LOOPDELAY, "second(s).")
    time.sleep(LOOPDELAY)
