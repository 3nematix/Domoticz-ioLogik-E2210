"""

    This code is to get Output/Input status and upload it to domoticz smart home control system.
    Built on - Moxa controller (ioLogik E2210).
    Made by - 3nematix (github)

"""

try:
    import sys
    import time
    import datetime
    import pprint

    from requests import ReadTimeout, ConnectTimeout, HTTPError, Timeout, ConnectionError
    from threading import Thread

    import requests

except ModuleNotFoundError as missing_m:
    print(missing_m, 'was not found..')
    time.sleep(2)
    sys.exit()

moxaIP = '192.168.1.220'
moxaAccessURL = f'{moxaIP}/getParam.cgi?'

domoticzIP = '192.168.1.124'
domoticzPORT = 8080

# Settings

MAX_REQUEST_PMIN = 30  # Sets the max requests sets sent per minute to 30.

DIGITAL_OUTPUTS = 8
ALLOWED_DO_VALUES = [0, 1, None]  # (Off,On)
ALLOWED_DO_ACTIONS = [0, 1]  # (GET, SET)
ALLOWED_DO_CHANNELS = [0, 1, 2, 3, 4, 5, 6, 7]

DIGITAL_INPUTS = 12
ALLOWED_DI_VALUES = [0, 1, None]
ALLOWED_DI_ACTIONS = [0, 1]
ALLOWED_DI_CHANNELS = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11]

idx_list = {0: '39',
            1: '40',
            2: '41',
            3: '42',
            4: '43',
            5: '44',
            6: '45',
            7: '46',
            8: '47',
            9: '48',
            10: '49',
            11: '50'
            }  # This list contains idx values for inputs

idx_list2 = {0: '51',
             1: '52',
             2: '53',
             3: '54',
             4: '55',
             5: '56',
             6: '57',
             7: '58'
             }  # This list contains idx values for outputs

class MoxaEngine:

    def __init__(self, ip):
        self.ip = ip

    def do(self, action, channel,  value):
        try:
            self.action = action
            self.channel = channel
            self.value = value

            if self.value not in ALLOWED_DO_VALUES:
                return None

            if self.channel not in ALLOWED_DO_CHANNELS:
                return None

            if self.action not in ALLOWED_DI_ACTIONS:
                return None

            if self.action == 0:  # GET
                try:

                    self.req_data = requests.get(f'http://{self.ip}/getParam.cgi?DOStatus_0{self.channel}=?', timeout=5)
                    self.req = self.req_data.text.replace(f'DOStatus_0{self.channel}', '').replace('=', '').replace('<br>', '')
                    return True if self.req == '1' else False

                except (ConnectTimeout, HTTPError, ReadTimeout, Timeout, ConnectionError):
                    return None

            if self.action == 1:  # SET
                try:

                    self.req_data = requests.get(f'http://{self.ip}/setParam.cgi?DOStatus_0{self.channel}={self.value}', timeout=5)
                    self.req = self.req_data.text.replace(f'DOStatus_0{self.channel}', '').replace('=', '').replace('<br>', '')
                    return True if self.req == str(self.value) else False

                except (ConnectTimeout, HTTPError, ReadTimeout, Timeout, ConnectionError):
                    return None

        except Exception as er:
            print(er)
            return None

    def di(self, action, channel,  value):
        try:
            self.action = action
            self.channel = channel
            self.value = value

            if self.value not in ALLOWED_DI_VALUES:
                return None

            if self.channel not in ALLOWED_DI_CHANNELS:
                return None

            if self.action not in ALLOWED_DI_ACTIONS:
                return None

            if self.action == 0:  # GET
                try:

                    self.req_data = requests.get(f'http://{self.ip}/getParam.cgi?DIStatus_0{self.channel}=?', timeout=5)
                    self.req = self.req_data.text.replace(f'DIStatus_0{self.channel}', '').replace('=', '').replace('<br>', '')
                    return True if self.req == '1' else False

                except (ConnectTimeout, HTTPError, ReadTimeout, Timeout, ConnectionError):
                    return None

            elif self.action == 1:  # SET
                try:
                    print(f'http://{self.ip}/setParam.cgi?DIStatus_0{self.channel}={self.value}')
                    self.req_data = requests.get(f'http://{self.ip}/setParam.cgi?DIStatus_0{self.channel}={self.value}', timeout=5)
                    self.req = self.req_data.text.replace(f'DIStatus_0{self.channel}', '').replace('=', '').replace('<br>', '')
                    return True if self.req == str(self.value) else False

                except (ConnectTimeout, HTTPError, ReadTimeout, Timeout, ConnectionError):
                    return None

        except Exception as er:
            print(er)
            return None


Moxa = MoxaEngine(moxaIP)

if '__main__' == __name__:
    try:

        action = 1
        channel = int(sys.argv[1])
        value = int(sys.argv[2])
        type = sys.argv[3]

        # Now we can update the value
        if type.lower() == 'do':
            resp = Moxa.do(action, channel, value)
            print('updated') if resp is True else print('not updated')

        if type.lower() == 'di':
            resp = Moxa.di(action, channel, value)
            print('updated') if resp is True else print('not updated')

    except Exception as er:
        print('No argv were provided... (channel, value, type)')
        sys.exit()

