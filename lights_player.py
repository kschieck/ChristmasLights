#!/usr/bin/env python3
import serial
import re
import time
import random
import sys
import re

# TODO restart arduino on new serial connection, however that's done
# TODO baud rate calculation
# TODO add more songs

def main_loop(argv):
    # allow for no sound command line argument to make it easier to play
    no_sound = '--no-sound' in argv
    debug = '--debug' in argv

    # handle --name="<name of song>"
    name_matcher = re.compile("--name=(.*)")
    args_name_match = list(filter(name_matcher.match, argv))
    file_name = "test" # default
    if len(args_name_match) == 0:
        print("No name provided in arguments (--name=\"<file name>\")")
    else:
        matches = re.search(name_matcher, args_name_match[0])
        file_name = matches.group(1)
    print("Request to play:", file_name)

    if not no_sound:
        from mpyg321.mpyg321 import MPyg321Player

    serial_name = '/dev/ttyACM0'
    serial_baud_rate = 9600 # bytes per second possible

    bytes_sent = 0
    bytes_expected = 0

    bytes_per_transfer = 30 # must divide bytes per transfer evenly
    bytes_per_request = 150

    if not no_sound:
        player = MPyg321Player()

    line_bytes = []
    line_bytes_idx = 0 # the index in line_bytes that we have already transferred up to

    try:
        ser = serial.Serial(serial_name, serial_baud_rate, serial.EIGHTBITS, timeout=1)
        ser.flush()
    except serial.serialutil.SerialException as err:
        print("Failed to open serial connection to", serial_name, err)
        return

    with open('data/' + file_name + '.csv') as fp:

        while True:
            if ser.in_waiting > 0:
                line = ser.readline().decode('utf-8').rstrip()
                x = re.search("DATA (\d+)", line)

                if x != None:
                    if debug:
                        print(line)
                    line_bytes_idx = 0
                    bytes_expected += bytes_per_request
                    currentLine = fp.readline() # 1 line per data request
                    if (currentLine == ""):
                        line_bytes = [0 for _ in range(bytes_per_request)]
                        continue
                    line_bytes = bytes([int(int(x) / 5) for x in currentLine.split(',')])
                    continue

                x = re.search("START", line)
                if x != None:
                    if debug:
                        print(line);
                    if not no_sound:
                        player.play_song('data/' + file_name + '.mp3')

            if bytes_sent < bytes_expected:
                # write the next bytes and update the idx
                ser.write(line_bytes[line_bytes_idx:line_bytes_idx+bytes_per_transfer])
                line_bytes_idx += bytes_per_transfer
                bytes_sent += bytes_per_transfer

            # rate limit the bytes
            time.sleep(0.01)

if __name__ == '__main__':
    main_loop(sys.argv)