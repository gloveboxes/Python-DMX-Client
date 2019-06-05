import json
import paho.mqtt.client as mqtt
import time


class DmxClient:
    def __init__(self, dmxServerAddress, fixtureIds):
        self.msg = {'red': 0, 'green': 0, 'blue': 0, 'white': 0}
        if not type(fixtureIds == 'list'):
            print("Fixture Ids must be a Python list - eg [1,2,3]")
            return

        self.dmxServerAddress = dmxServerAddress
        self.fixtureIds = fixtureIds
        self.mqttDmxDataTopic = "dmx/data"

        self.mqttConnected = False
        self.client = mqtt.Client()
        self.client.on_connect = self.__on_connect
        self.client.on_disconnect = self.__on_disconnect
        self.client.connect_async(dmxServerAddress, 1883, 60)
        self.client.loop_start()

    def __on_connect(self, client, userdata, flags, rc):
        print("Connected to DMX Server '{0}' with result code {1}".format(
            self.dmxServerAddress, rc))
        self.mqttConnected = True

    def __on_disconnect(self, client, userdata, rc):
        print("Disconnected from DMX Server '{0}' with result code {1}".format(
            self.dmxServerAddress, rc))
        self.mqttConnected = False

    def colours(self, red=0, green=0, blue=0, white=0):
        if not (0 <= red < 256 and 0 <= green < 256 and 0 <= blue < 256 and 0 <= white < 256):
            print('Invalid Colour. Vallid colour range is 0..255')
            return

        self.msg['red'] = red
        self.msg['green'] = green
        self.msg['blue'] = blue
        self.msg['white'] = white

    @property
    def red(self):
        return self.msg['red']

    @red.setter
    def red(self, value):
        if 0 <= value < 256:
            self.msg['red'] = value

    @property
    def green(self):
        return self.msg['green']

    @green.setter
    def green(self, value):
        if 0 <= value < 256:
            self.msg['green'] = value

    @property
    def blue(self):
        return self.msg['blue']

    @blue.setter
    def blue(self, value):
        if 0 <= value < 256:
            self.msg['blue'] = value

    @property
    def white(self):
        return self.msg['white']

    @white.setter
    def white(self, value):
        if 0 <= value < 256:
            self.msg['white'] = value

    def clear(self):
        red = 0
        green = 0
        blue = 0
        white = 0

    def publish(self, fixtureIds=None):
        retryCount = 0

        if fixtureIds is None:
            self.msg['id'] = self.fixtureIds
        else:
            if self.__validateFixtureIds(fixtureIds):
                self.msg['id'] = fixtureIds
            else:
                print(
                    "Fixture Ids must be a Python list, eg [1,2,3], and be found in the declared fixtures {0}".format(self.fixtureIds))
                return

        while retryCount < 4:
            if self.mqttConnected:
                self.client.publish(self.mqttDmxDataTopic,
                                    json.dumps(self.msg))
                break
            retryCount += 1
            time.sleep(retryCount)
        else:
            print('Send failed, not connected to DMX Server {0}'.format(
                self.dmxServerAddress))

    def __validateFixtureIds(self, fixtureIds):
        if not type(fixtureIds == 'list'):
            return False
        for id in fixtureIds:
            if id not in self.fixtureIds:
                return False
        return True
