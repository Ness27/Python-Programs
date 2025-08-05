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
        self._password = ''
        self.device_type = 'cisco_ios'
        self.port = '22'

    def __getitem__(self, item):
        if item == 'password':
            logging.critical('Cannot retrieve {}'.format(item))
            raise KeyError("Direct access to password is not allowed.")
        return self.get_connection_info().get(item)

    def get_connection_info(self, include_password=False):
        info = {
            'host': self.hostname,
            'port': str(self.port),
            'device_type': self.device_type,
            'username': self.username,
        }
        if include_password:
            info['password'] = self._password
        return info

    def set_user(self, user = '<USER>'):
        self.username = user

    def set_password(self, password = '<PASSWORD>'):
        self._password = password

    def set_host_ip(self, ip):
        self.hostname = ip

    def set_device_type(self, device_type):
        self.device_type = device_type

def connectSession(arguments, commands):
    try:
        theIP = format(ipaddress.ip_address(arguments['host']))
        logging.info("Connecting to {} over {} ".format(theIP, arguments['port']))


        connection = netmiko.ConnectHandler(**arguments.get_connection_info(include_password=True))
        for cmd in commands:
            output = connection.send_command(cmd)
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
    commandsToRun = ['show ip int br']

    deviceInfo = networkingDevice()
    deviceInfo.set_host_ip(input('Enter host ip: '))
    deviceInfo.set_user(input('Enter username: '))
    deviceInfo.set_password(pwinput.pwinput(prompt="Password: ", mask='*'))

    connectSession(deviceInfo, commandsToRun)


    logging.info("Program finished. - Exiting program.")
    finalTime = time.perf_counter()
    logging.info('Total running time: {} seconds.'.format(round(finalTime-startTime,5)))
    logging.shutdown()

if __name__ == "__main__":
    main()