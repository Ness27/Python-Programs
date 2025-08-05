"""
Filename: default-command-runner.py
Description: Run Commands on an IOS-XE Networking Device.
Author: Hunter R.
Date: 2025-07-28
"""

import netmiko
import sys
import logging
import ipaddress
import time
import pwinput

# ️ Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[
        logging.StreamHandler(sys.stdout)
    ]
)

class networkingDevice():
    def __init__(self):
        self.hostname = ''
        self.username = ''
        self.password = ''
        self.device_type = 'cisco_ios'
        self.port = '22'
        self.results = {}
        self.__compile__()

    def __compile__(self):
        self.results = {'host': self.hostname,
                   'port': self.port,
                   'device_type': self.device_type,
                   'username': self.username,
                   'password': self.password}

    def __getitem__(self, item):
        return self.results[item]

    def getDeviceInfo(self):
        return self.results

    def setUser(self, user = '<USER>'):
        self.username = user
        self.__compile__()

    def setPassword(self, password = '<PASSWORD>'):
        self.password = password
        self.__compile__()

    def setHostIp(self, ipaddr):
        self.hostname = ipaddr
        self.__compile__()

    def setDeviceType(self, device_type):
        self.device_type = device_type
        self.__compile__()

def connectSession(arguments, commands):
    try:
        theIP = format(ipaddress.ip_address(arguments['host']))
        logging.info("Connecting to {} over {} ".format(theIP, arguments['port']))


        connection = netmiko.ConnectHandler(**arguments.getDeviceInfo())
        output = connection.send_command(commands)
        logging.info(output)

        connection.disconnect()

    except ValueError as val:
        logging.error('{}'.format(val))
        logging.error("Skipping {}".format(str(val).split(' ')[0]))
        return None
    except TimeoutError:
        logging.error("There was an error: {}".format("TimeoutError"))
        logging.error("Skipping {}".format(arguments['host']))
        return None
    except KeyboardInterrupt:
        logging.exception("User interrupt.")
        logging.error("There was an error: {}".format("KeyboardInterrupt"))
        logging.error("Exiting program.")
        exit(1)
    except netmiko.exceptions.NetMikoTimeoutException as theError:
        logging.error("There was an error: {}".format(theError))

    return None

def main():
    startTime = time.perf_counter()
    logging.info("Setup complete.")
    logging.info("Starting main program...")
    setupComplete = time.perf_counter()
    logging.info('Completed initialization in {} seconds.'.format(round(setupComplete-startTime,5)))

    # When sending EXEC commands - you cannot give a list unless you iterate over the list. Must be TYPE='str'
    commandsToRun = 'show ip int br'

    deviceInfo = networkingDevice()
    deviceInfo.setHostIp(input('Enter host ip: '))
    deviceInfo.setUser(input('Enter username: '))
    deviceInfo.setPassword(pwinput.pwinput(prompt="Password: ", mask='*'))

    connectSession(deviceInfo, commandsToRun)


    logging.info("Program finished. - Exiting program.")
    finalTime = time.perf_counter()
    logging.info('Total running time: {} seconds.'.format(round(finalTime-startTime,5)))
    logging.shutdown()

if __name__ == "__main__":
    main()