# ChristmasLights
A system for Christmas lights powered by a RaspberryPi and an Arduino.

This program turns your arduino into a lights controller

## Setup

I started with `Raspbian`, which came with `python3` pre-installed, but if you don't have it, install it by following instructions found here:
https://samx18.io/blog/2018/09/05/python3_raspberrypi.html

Run these commands to install the required software and libraries:
`mpg321` and `mpyg321` are optional, but are required if you want to play audio from thhe raspberry pi
```
sudo apt-get install mpg321
sudo pip3 install board adafruit-circuitpython-neopixel mpyg321
```

Start the program with this command:
`sudo python3 lights_player.py`

Or, without sound
`sudo python3 lights_player.py --no-sound`

## Parts List
Many parts I already owned, so do your own research on the legitimacy of these offers:

- Raspberry Pi: https://www.raspberrypi.org/products/raspberry-pi-4-model-b/ (You do not need the latest and greatest, my pi is a couple years old. I'd like to try this out on a raspberry pi zero)
- Raspberry pi power cable
- Arduino: https://store.arduino.cc/usa/arduino-uno-rev3 (I used an uno, though I'd like to use a nano (see alibaba for super cheap nanos!), if it works just as well)
- LEDs: https://www.amazon.ca/gp/product/B01AG923GI (one of many options)
- Some wires, male and female: https://www.amazon.ca/Jumper-Wires-Premium-200mm-Female/dp/B008MRZSH8

Optional:
- Power adapter for LEDs: https://www.amazon.ca/gp/product/B07DQR919Y If you want to power more LEDs, you'll want a power adapter for additional amperage
- Connectors for power adapter: https://www.amazon.ca/gp/product/B076SXZK7M
