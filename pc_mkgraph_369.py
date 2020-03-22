#!/usr/bin/env python3

"""
Python script on the PC running Linux, gathering local information
and saving it as a text file on the CircuitPython. Requires Python
3.6.9 or higher.  This script does not provide automation, as that
can be applied with this cron entry:
`* * * * * <repository path>/pc_mkgraph.py >/dev/null 2>&1`

References
* https://docs.python.org/3/library/time.html
* https://docs.python.org/3/library/sys.html
* https://docs.python.org/3/library/subprocess.html
* https://docs.python.org/3/tutorial/errors.html
* http://man7.org/linux/man-pages/man5/proc.5.html
* https://www.tutorialspoint.com/python3/time_strftime.htm
* https://en.wikipedia.org/wiki/ISO_8601
"""

## LIBRARIES
import time
import sys
import subprocess

## VARIABLES
### DEBUG: Toggle debugging if needed
DEBUG = True
### TXTFILE: File to write information to
TXTFILE = "/media/kso/CIRCUITPY/hostinfo.txt"
### CPUCOUNTCMD: Program to find CPU count
CPUCOUNTCMD = "/bin/grep -c -E '^CPU|^processor' </proc/cpuinfo"
### LOADAVGCMD: Program to find load average
LOADAVGCMD = "/bin/cat /proc/loadavg"
### TIMEFORMAT: String used to format time
TIMEFORMAT = "%Y-%m-%dT%H:%M:%S%z"
### STDOUTCPU; OUTPUT; STDOUTLOAD: Initialize variables to aid in
###  troubleshooting
STDOUTCPU = OUTPUT = STDOUTLOAD = "EMPTY"

## CODE
### Pull CPU count; output should look like single number; Ex: `16`
try:
    STDOUTCPU = subprocess.check_output([CPUCOUNTCMD], shell=True)
    STDOUTCPU = STDOUTCPU.strip()
except OSError as err:
    print("OS error: {0}".format(err))
except:
    print("Unexpected error:", sys.exc_info()[0])
    raise
if DEBUG:
    print("STDOUTCPU:", STDOUTCPU)

### Pull load averages; output should look like 3 floats, a fraction, and a
###  number; Ex: `8.32 7.89 7.92 12/2452 2670160`
try:
    STDOUTLOAD = subprocess.check_output([LOADAVGCMD], shell=True)
    STDOUTLOAD = STDOUTLOAD.strip()
except OSError as err:
    print("OS error: {0}".format(err))
except:
    print("Unexpected error:", sys.exc_info()[0])
    raise
if DEBUG:
    print("STDOUTLOAD:", STDOUTLOAD)

### Pull time and format to ISO 8601; output should look like a date and time
###  stamp with timezone; Ex: `2020-03-12T21:50:21-0600`
LOCALTIME = time.strftime(TIMEFORMAT, time.localtime(time.time())).encode("utf-8")
if DEBUG:
    print("LOCALTIME:", LOCALTIME)

### Write output to the CircuitPython drive
OUTPUT = STDOUTCPU + b" " + STDOUTLOAD + b" " + LOCALTIME
if DEBUG:
    print("OUTPUT:", OUTPUT)
try:
    FILEOUT = open(TXTFILE, "w")
    FILEOUT.write(OUTPUT)
    FILEOUT.close()
    if DEBUG:
        print("File written:", TXTFILE)
except OSError as err:
    print("OS error: {0}".format(err))
except:
    print("Unexpected error:", sys.exc_info()[0])
    raise

### Let the user know we're done
if DEBUG:
    print("*** Script Complete ***")
