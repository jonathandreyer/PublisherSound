# PublisherSound

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
sudo apt-get install portaudio19-dev libav-tools
pip3 install -r requirements.txt
```


### Script to launch at boot
1. Copy file *app_example.service* to *app.service*
2. Edit with correct paths to repository (app & config file)
3. Copy file *app.service* in */lib/systemd/system/*
```
sudo cp ./app.service /lib/systemd/system/
sudo chmod 644 /lib/systemd/system/app.service
chmod +x ./app.py
```

4. Activate it:
```
sudo systemctl daemon-reload
sudo systemctl enable app.service
sudo systemctl start app.service
```

5. *(Optional) Show status of app:*
```
sudo systemctl status app.service
```


### Create config file with credential
1. Copy file *config_example.ini* to *config.ini*
2. Change *USERNAME_CLYP* & *PASSWORD_CLYP* with correct credential


## Launch command app.py
```
sudo python3 app.py -d
```



## Sources
- *USB audio adapter* : https://learn.adafruit.com/usb-audio-cards-with-a-raspberry-pi/updating-alsa-config
- *Python app as service* : http://www.diegoacuna.me/how-to-run-a-script-as-a-service-in-raspberry-pi-raspbian-jessie/
