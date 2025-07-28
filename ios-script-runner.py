"""
Filename: ios-script-runner.py
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
from paramiko.client import AutoAddPolicy

# ️ Configure logging
logging.basicConfig(
    level=logging.DEBUG,
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[
        logging.StreamHandler(sys.stdout)
    ]
)

def connectSession(arguments):
    try:
        theIP = format(ipaddress.ip_address(arguments['host']))
        logging.info("Connecting to {} over {} ".format(theIP, arguments['port']))
        connection = netmiko.ConnectHandler(**arguments)

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

    commandsToRun = ['do show ip int br']

    deviceInfo = {'host':'10.132.101.252',
                  'port':'22',
                  'device_type':'cisco_ios',
                  'username':input('user:'),
                  'password':pwinput.pwinput(prompt="Password: ", mask='*')}

    connectSession(deviceInfo)


    logging.info("Program finished. - Exiting program.")
    logging.shutdown()

if __name__ == "__main__":
    main()
