#!/usr/bin/env python3

"""
Python script on the PC running Linux, gathering local information
and saving it as a text file on the CircuitPython. Requires Python 
3.8.2 or higher.  This script does not provide automation, as that 
can be applied with this cron entry:
`* * * * * <repository path>/pc_mkgraph.py >/dev/null 2>&1`
"""

## LIBRARIES


## VARIABLES
### Toggle debugging if needed
DEBUG = True
### File to read information from
TXTFILE = "hostinfo.txt"
### Set output line to aid in troubleshooting
OUTPUT = "EMPTY"

## CODE
### Write output
print("OUTPUT:", OUTPUT)
FILEOUT = open(TXTFILE, "w")
FILEOUT.write(OUTPUT)
FILEOUT.close()

### Let the user know we're done
if DEBUG:
    print("*** Script Complete ***")
