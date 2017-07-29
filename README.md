# audio-recorder-and-publisher

## Goal
Record a sound from input and publish on Clyp.it.


## Materiel used
- Raspberry PI 2
- Analog audio input (USB)
- iPhone Personal Hotspot over USB

## Schematic of GPIO



## Installation

### Procedure to install from scratch
Write SD card with Raspberry [instruction](https://www.raspberrypi.org/documentation/installation/installing-images).


### Install driver to activate iPhone Personal Hotspot over USB
```
sudo apt-get install usbmuxd
```


### Script to launch at boot



## Launch command app.py
```
sudo python3 app.py -d
```
