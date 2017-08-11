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


### Config USB sound adapter to default
```
cat > /etc/asound.conf << EOF
pcm.!default  {
 type hw card 1
}
ctl.!default {
 type hw card 1
}
EOF
```


### Install requirement for python app
```
sudo apt-get install portaudio19-dev
pip3 install -r requirements.txt
```


### Script to launch at boot



## Launch command app.py
```
sudo python3 app.py -d
```



## Sources
- *USB audio adapter* : https://learn.adafruit.com/usb-audio-cards-with-a-raspberry-pi/updating-alsa-config
