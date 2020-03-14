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
"""

## LIBRARIES
import board
import digitalio
import supervisor
import time

## VARIABLES
### DEBUG: Toggle debugging if needed
DEBUG = True
### TXTFILE: File to read information from
TXTFILE = "/hostinfo.txt"
### Pre-defined numbers; keep (LOOPDELAY * LOOPFACTOR) > 60
LOOPCOUNT = 0
LOOPDELAY = 10
LOOPFACTOR = 7

## CONFIGURE
### Onboard red LED attached to digital pin 13
led = digitalio.DigitalInOut(board.D13)
led.direction = digitalio.Direction.OUTPUT

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
    ### Indicate that we're processing data
    led.value = False
    ### Pause until it's time to act again
    if DEBUG:
        print("***** Processing complete, sleeping for", LOOPDELAY, "seconds... *****")
    time.sleep(LOOPDELAY)
