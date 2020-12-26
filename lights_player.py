#!/usr/bin/env python3
import serial
import re
import time
import random
import sys
import re
import signal
import atexit

serial_name = '/dev/ttyUSB0'
serial_baud_rate = 115200 # bits per second possible

ser = None # serial connection

killed = False

def init_serial_connection():
    try:
        global ser
        ser = serial.Serial(serial_name, serial_baud_rate, serial.EIGHTBITS, timeout=1)
        ser.flush()
    except serial.serialutil.SerialException as err:
        print("Failed to open serial connection to", serial_name, err)
        return False
    return True

def handle_exit(a=1, b=2):
    global killed
    killed = True

def main_loop(argv, ser):
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

    bytes_sent = 0
    bytes_expected = 0

    bytes_per_transfer = 50 # must divide bytes per transfer evenly
    bytes_per_request = 150

    if not no_sound:
        player = MPyg321Player()

    line_bytes = []
    line_bytes_idx = 0 # the index in line_bytes that we have already transferred up to


    if not no_sound:
        player.play_song('data/' + file_name + '.mp3')
        player.pause()

    with open('data/' + file_name + '.csv') as fp:

        global killed
        while not killed:
            if ser.in_waiting > 0:
                line = ser.readline().decode('utf-8').rstrip()
                x = re.search("(\d+)", line)

                if x != None:
                    if debug:
                        print(line)
                    line_bytes_idx = 0
                    bytes_expected += bytes_per_request
                    currentLine = fp.readline() # 1 line per data request
                    if (currentLine == ""):
                        line_bytes = [0 for _ in range(bytes_per_request)]
                        continue
                    line_bytes = bytes([int(x) for x in currentLine.split(',')])
                    continue

                x = re.search("START", line)
                if x != None:
                    if debug:
                        print(line);
                    if not no_sound:
                        player.resume()

            if bytes_sent < bytes_expected:
                # write the next bytes and update the idx
                ser.write(line_bytes[line_bytes_idx:line_bytes_idx+bytes_per_transfer])
                line_bytes_idx += bytes_per_transfer
                bytes_sent += bytes_per_transfer

            # rate limit the bytes
            time.sleep(0.001)

        if ser is not None:
            if debug:
                print("Closing serial connection")
            ser.close()

if __name__ == '__main__':
    if init_serial_connection():
        atexit.register(handle_exit)
        signal.signal(signal.SIGTERM, handle_exit)
        signal.signal(signal.SIGINT, handle_exit)
        main_loop(sys.argv, ser)