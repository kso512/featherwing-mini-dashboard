# featherwing-mini-dashboard

Documentation and CircuitPython code for a device mounted to the front of a computer which displays graphs.

## Design

The general idea behind this project is to be able to check on the status of a server's long job run from afar.  This way if the screensaver is on or the screen is otherwise not visible, a graph of the server's load can be seen.  Similar to [WOPR in "War Games"](https://www.youtube.com/watch?v=_aUHQKneAdw) or a [stack light](https://en.wikipedia.org/wiki/Stack_light) on manufacturing equipment.

### Hardware Overview

Hardware for this project consists of:

1. PC running Linux
1. [Adafruit Feather STM32F405 Express](https://www.adafruit.com/product/4382) including stacking headers
1. [Adafruit Mini Color TFT with Joystick FeatherWing](https://www.adafruit.com/product/3321)
1. [I/O Crest Blank Tray Storage Box Drawer for 5.25" Bay Drive for Any PC Desktop Computer](https://amzn.com/B01LY3YDLN) (or equivalent)
1. USB-C Cable

### Software Overview

Software for this project consists of:

1. Python script on the PC running Linux, gathering local information and saving it as a text file on the CircuitPython.
    1. Requires Python 3.8.2 or higher.
    1. This script does not provide automation, as that can be applied with this cron entry:
        > `* * * * * <repository path>/pc_mkgraph.py >/dev/null 2>&1`

1. Python script on the Feather, converting the text file data into a graph and displaying the graph.

## Installation & Configuration

### Hardware Assembly

After receiving all of the parts, assemble them so that the FeatherWing has male headers pointing down and the Feather has female headers pointing up.  Mate the two together, then plug it into your computer and follow the steps [here](https://learn.adafruit.com/welcome-to-circuitpython/installing-circuitpython) to install the latest version of CircuitPython.

Drill the screw holes in the drawer to match the mounting holes on the FeatherWing, then cut a hole in the drawer that matches the buttons and screen but leaves enough material for the screws to grip to.  The drawer may also need a notch in the back to allow a USB cable to pass through to the motherboard.

## License

[MIT](https://raw.githubusercontent.com/kso512/featherwing-mini-dashboard/master/LICENSE)
