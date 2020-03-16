# featherwing-mini-dashboard

Documentation and CircuitPython code for a device mounted to the front of a computer which displays graphs.

## Design

The general idea behind this project is to be able to check on the status of a server's long job run from afar.  This way if the screensaver is on or the screen is otherwise not visible, a graph of the server's load can be seen.  Similar to [WOPR in "War Games"](https://www.youtube.com/watch?v=_aUHQKneAdw) or a [stack light](https://en.wikipedia.org/wiki/Stack_light) on manufacturing equipment.

### Hardware Overview

Hardware for this project consists of:

1. PC running Linux
1. [Adafruit Feather STM32F405 Express including stacking headers](https://www.adafruit.com/product/4382)
1. [Adafruit Mini Color TFT with Joystick FeatherWing](https://www.adafruit.com/product/3321)
1. [I/O Crest Blank Tray Storage Box Drawer for 5.25" Bay Drive for Any PC Desktop Computer](https://amzn.com/B01LY3YDLN) (or equivalent)
1. USB-C Cable

### Software Overview

Software for this project consists of:

1. Python script on the PC running Linux, gathering local information and saving it as a text file on the CircuitPython.
    1. Requires Python 3.8.2 or higher.
    1. This script does not provide automation as that can be applied with cron; see below.

1. Python script on the Feather, converting the text file data into a graph and displaying the graph.  The graph will consist of colored vertical bars, each dependent upon the state at the time:
    1. RED: Failure condition, such as a missing file
    1. YELLOW: Warning condition, such as a stale file
    1. GREEN: Normal operation, processing data
    1. BLUE: Standing by, no load
1. New bars will appear on the right and old bars drop off the left, causing a crawling effect.  For now, the whole display marks the current status.

## Installation & Configuration

### Hardware Assembly

After receiving all of the parts, assemble them so that the FeatherWing has male headers pointing down and the Feather has female headers pointing up.  Mate the two together, then plug it into to the PC running Linux with the USB-C cable and follow the steps [here](https://learn.adafruit.com/welcome-to-circuitpython/installing-circuitpython) to install the latest version of CircuitPython.  After connecting the Feather, note the path given to the mounted drive.

Carefully drill holes in the front of the drawer to match the mounting holes on the FeatherWing, then cut a hole in the drawer that matches the buttons and screen but leaves enough material for the screws to grip to.  The drawer may also need a notch in the back to allow the USB-C cable to pass through to the motherboard.  After troubleshooting any issues and making sure everything's working well, mount the device in the drawer and mount the drawer into the PC running Linux.

### Software Installation and Configuration

Clone the repository from GitHub.  Adjust the variables, especially TXTFILE so it matches the path given to the mounted drive.  Enable automation with cron using an entry such as this:
> `* * * * * <repository path>/pc_mkgraph.py >/dev/null 2>&1`

Copy `stm32f405_code.py` to the mounted drive as `code.py` and reset using REPL or the reset button.

## References

* [time — Time access and conversions](https://docs.python.org/3/library/time.html)
* [sys — System-specific parameters and functions](https://docs.python.org/3/library/sys.html)
* [subprocess — Subprocess management](https://docs.python.org/3/library/subprocess.html)
* [Errors and Exceptions](https://docs.python.org/3/tutorial/errors.html)
* [proc - process information pseudo-filesystem](http://man7.org/linux/man-pages/man5/proc.5.html)
* [ISO 8601 Date and time format](https://www.iso.org/iso-8601-date-and-time-format.html)
* [Adafruit STM32F405 Feather Express](https://learn.adafruit.com/adafruit-stm32f405-feather-express/overview)
* [supervisor - Supervisor settings](https://circuitpython.readthedocs.io/en/latest/shared-bindings/supervisor/__init__.html)
* [board - Board specific pin names](https://circuitpython.readthedocs.io/en/latest/shared-bindings/board/__init__.html)
* [digitalio — Basic digital pin support](https://circuitpython.readthedocs.io/en/latest/shared-bindings/digitalio/__init__.html)
* [time — time and timing related functions](https://circuitpython.readthedocs.io/en/latest/shared-bindings/time/__init__.html)
* [Introduction (to FeatherWing Library)](https://circuitpython.readthedocs.io/projects/featherwing/en/latest/index.html)

## License

[MIT](https://raw.githubusercontent.com/kso512/featherwing-mini-dashboard/master/LICENSE)
