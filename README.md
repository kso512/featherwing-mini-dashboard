# featherwing-mini-dashboard

Documentation and CircuitPython code for a device mounted to the front of a computer to display graphs

# Design Overview

The general idea behind this project is to be able to check on the status of a server's long job run from afar.

## Hardware

Hardware for this project consists of:

1. PC running Linux
1. [Adafruit Feather STM32F405 Express](https://www.adafruit.com/product/4382)
1. [Adafruit Mini Color TFT with Joystick FeatherWing](https://www.adafruit.com/product/3321)
1. [I/O Crest Blank Tray Storage Box Drawer for 5.25" Bay Drive for Any PC Desktop Computer](https://amzn.com/B01LY3YDLN) (or equivalent)

## Software

Software for this project consists of:

1. Python script on the PC running Linux, using RRDtool to generate a graph in BMP format and save it on the CircuitPython
1. Python script on the Feather, displaying the graph

# License

MIT - see ./LICENSE
