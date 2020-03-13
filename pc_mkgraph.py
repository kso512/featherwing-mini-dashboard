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
### https://docs.python.org/3/library/sys.html
import sys
### https://docs.python.org/3/library/subprocess.html
import subprocess

## VARIABLES
### DEBUG: Toggle debugging if needed
DEBUG = True
### CPUCOUNTCMD: Program to find CPU count
CPUCOUNTCMD = "/bin/grep -c -E '^CPU|^processor' </proc/cpuinfo"
### LOADAVGCMD: Program to find load average
LOADAVGCMD = "/bin/cat /proc/loadavg"
### TIMEFORMAT: String used to format time
TIMEFORMAT = "%Y-%m-%dT%H:%M:%S%z"
### TXTFILE: File to read information from
TXTFILE = "/media/kso/CIRCUITPY/hostinfo.txt"
### STDOUTCPU; OUTPUT; STDOUTLOAD: Set variables used later to aid in troubleshooting
STDOUTCPU = OUTPUT = STDOUTLOAD = "EMPTY"

## CODE
###  https://docs.python.org/3/tutorial/errors.html

### Pull CPU count
###  http://man7.org/linux/man-pages/man5/proc.5.html
try:
    STDOUTCPU = subprocess.run([CPUCOUNTCMD], shell=True, capture_output=True, text=True).stdout
    STDOUTCPU = STDOUTCPU.strip()
except OSError as err:
    print("OS error: {0}".format(err))
except:
    print("Unexpected error:", sys.exc_info()[0])
    raise
if DEBUG:
    print("STDOUTCPU:", STDOUTCPU)

### Pull load averages
###  https://access.redhat.com/documentation/en-US/Red_Hat_Enterprise_Linux/4/html/Reference_Guide/s2-proc-loadavg.html
###  "The first three columns measure CPU and IO utilization of the last one, five, and 10 minute periods. 
###   The fourth column shows the number of currently running processes and the total number of processes. 
###   The last column displays the last process ID used."
try:
    STDOUTLOAD = subprocess.run([LOADAVGCMD], shell=True, capture_output=True, text=True).stdout
    STDOUTLOAD = STDOUTLOAD.strip()
except OSError as err:
    print("OS error: {0}".format(err))
except:
    print("Unexpected error:", sys.exc_info()[0])
    raise
if DEBUG:
    print("STDOUTLOAD:", STDOUTLOAD)

### Pull time and format to ISO 8601
###  https://www.tutorialspoint.com/python3/time_strftime.htm
###  https://en.wikipedia.org/wiki/ISO_8601
LOCALTIME = time.strftime(TIMEFORMAT, time.localtime(time.time()))
if DEBUG:
    print("LOCALTIME:", LOCALTIME)

### Write output to the CircuitPython drive
OUTPUT = STDOUTCPU + " " + STDOUTLOAD + " " + LOCALTIME
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
