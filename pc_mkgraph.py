#!/usr/bin/env python3

"""
Python script on the PC running Linux, gathering local information
and saving it as a text file on the CircuitPython. Requires Python 
3.8.2 or higher.  This script does not provide automation, as that 
can be applied with this cron entry:
`* * * * * <repository path>/pc_mkgraph.py >/dev/null 2>&1`
"""

## LIBRARIES
### https://docs.python.org/3/library/time.html
import time

## VARIABLES
### Toggle debugging if needed
DEBUG = False
### File to read information from
TXTFILE = "hostinfo.txt"
### Set output line to aid in troubleshooting
OUTPUT = "EMPTY"

## CODE
### Pull time and format to ISO 8601
###  https://www.tutorialspoint.com/python3/time_strftime.htm
###  https://en.wikipedia.org/wiki/ISO_8601
LOCALTIME = time.strftime("%Y-%m-%dT%H:%M:%S%z", time.localtime(time.time()))
if DEBUG:
    print("LOCALTIME:", LOCALTIME)

### Write output
OUTPUT = LOCALTIME
if DEBUG:
    print("OUTPUT:", OUTPUT)
FILEOUT = open(TXTFILE, "w")
FILEOUT.write(OUTPUT)
FILEOUT.close()

### Let the user know we're done
if DEBUG:
    print("*** Script Complete ***")
