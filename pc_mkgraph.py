#!/usr/bin/env python3
"""
Python script on the PC running Linux, using RRDtool to generate a
graph in BMP format and save it on the CircuitPython.  This script
does not provide automation, as that can be applied with this cron
entry:   * * * * * <repository path>/pc_mkgraph.py >/dev/null 2>&1
"""

## VARIABLES
DEBUG = False

## CODE
### Let the user know we're done
if DEBUG:
    print("*** Script Complete ***")
