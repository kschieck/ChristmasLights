# ChristmasLights
A system for Christmas lights powered by a RaspberryPi and an Arduino.

This program turns your Arduino into a lights controller and your RaspberryPi into the driver

## Setup and Testing

I started with `Raspbian`, which came with `python3` pre-installed, but if you don't have it, install it by following instructions found here:
https://samx18.io/blog/2018/09/05/python3_raspberrypi.html

Run these commands to install the required software and libraries:
`mpg321` and `mpyg321` are optional, but are required if you want to play audio from the raspberry pi
```
sudo apt-get install mpg321
sudo pip3 install board adafruit-circuitpython-neopixel mpyg321
```

Start the program with this command:
`sudo python3 lights_player.py`

Or, without sound:
`sudo python3 lights_player.py --no-sound`

For debug prints, use this command line argument:
`--debug`

To play the `csv` and `mp3` of your choosing, use this argument:
`--name="<filename without extension>"`

Examples:
```
# This will show debug statements, and play the file `./data/pattern1.csv`
sudo python3 lights_player.py --no-sound --debug --name="pattern1"

# This will play the files `data/Through the Fire and Flames.mp3` and `data/Through the Fire and Flames.csv` with no debug statements
sudo python3 lights_player.py --name="Through the Fire and Flames"

# This will play `data/test.csv` with no sound, no debug statements
sudo python3 lights_player.py --no-sound
```

## Running the Web Server

Use this command to run a server where you can pick songs or patterns to play from the `data` folder
```
sudo python3 server.py
```

Then visit `<ip>:8000` from any device on the same network. You'll see the IP in the output of the server command above

## Adding Songs and Patterns

Add a `.csv` file and optionally a matching file name `.mp3` file to the data directory on the RaspberryPi (or other device) and it should be made available to play via the server.

## Creating New Songs and patterns

Visit http://doityourselfchristmas.com/ and download the software Vixen3. With this app you can create light shows to be in sync with songs and export the files to a format readable by this software.

Steps:
- Create output display (Vixen)
- Create pattern in the sequence editor (Vixen)
- Save sequence
- Export as CSV (100 ms)
- Upload `csv` (and optionally `mp3`) to RaspberryPi (`data` directory)

## Parts List
Many parts I already owned, so do your own research on the legitimacy of these offers:

- RaspberryPi: https://www.raspberrypi.org/products/raspberry-pi-4-model-b/ (You do not need the latest and greatest, my pi is a couple years old. I'd like to try this out on a RaspberryPi zero)
- RaspberryPi power cable
- Arduino: https://www.alibaba.com/product-detail/Micro-USB-Nano-V3-0-ATmega328P_62019159090.html (I didn't purchase this specific one)
- LEDs: https://www.amazon.ca/gp/product/B01AG923GI (one of many options)
- Some wires, male and female: https://www.amazon.ca/Jumper-Wires-Premium-200mm-Female/dp/B008MRZSH8

Optional:
- Power adapter for LEDs: https://www.amazon.ca/gp/product/B07DQR919Y If you want to power more LEDs, you'll want a power adapter for additional amperage
- Connectors for power adapter: https://www.amazon.ca/gp/product/B076SXZK7M

## Resources Used While Creating this Project

https://roboticsbackend.com/raspberry-pi-arduino-serial-communication/

https://howtomechatronics.com/tutorials/arduino/how-to-control-ws2812b-individually-addressable-leds-using-arduino/

https://forum.arduino.cc/index.php?topic=396450.0
