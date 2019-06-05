import dmxclient
import time
import random

dmx = dmxclient.DmxClient(dmxServerAddress='dmxserver.local', fixtureIds=[1, 2, 3])


def cycleColours():
    for cycles in range(10):
        for colour in range(100, 255):
            dmx.colours(red=colour)
            dmx.publish([1, 3])
            dmx.colours(blue=colour)
            dmx.publish([2])
            time.sleep(0.1)


def cyclePalette():
    palette = [[255, 0, 0], [0, 255, 0], [0, 0, 255]]

    for cycles in range(100):
        for colour in palette:
            # dmx.colours(red=colour[0], green=colour[1], blue=colour[2])
            # dmx.colours(colour[0], colour[1], colour[2])
            # alternatively set colour by property

            dmx.red = colour[0]
            dmx.green = colour[1]
            dmx.blue = colour[2]
            dmx.white = 0

            dmx.publish()
            time.sleep(0.5)


def simple():
    dmx.colours(255, 0, 255) # magenta
    dmx.publish()
    time.sleep(3)

    dmx.clear()
    dmx.red = 255
    dmx.publish(fixtureIds=[2])

    time.sleep(3)


def lightsOff():
    dmx.clear()  # will default to black
    dmx.publish()  # defaults to all fixtures


simple()
cycleColours()
cyclePalette()
lightsOff()
