#!/usr/bin/env python3
#pylint: disable=c-extension-no-member

"""
Python script on the PC running Linux, using RRDtool to generate a
graph in BMP format and save it on the CircuitPython.  This script
does not provide automation, as that can be applied with this cron
entry:   * * * * * <repository path>/pc_mkgraph.py >/dev/null 2>&1
Requires RRDTool:    https://pythonhosted.org/rrdtool/install.html
"""

## LIBRARIES
import rrdtool

## VARIABLES
### Toggle debugging if needed
DEBUG = False
### File to place information into
BMPFILE = "hostinfo.bmp"

## CODE
rrdtool.create(
    "test.rrd",
    "--start", "now",
    "--step", "300",
    "RRA:AVERAGE:0.5:1:1200",
    "DS:temp:GAUGE:600:-273:5000")

# feed updates to the database
rrdtool.update("test.rrd", "N:32")

### Let the user know we're done
if DEBUG:
    print("*** Script Complete ***")
