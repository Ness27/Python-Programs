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
from networking import networkingDevice

# ️ Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[
        logging.StreamHandler(sys.stdout)
    ]
)

def connectSession(arguments, commands):
    try:
        theIP = format(ipaddress.ip_address(arguments['host']))
        logging.info("Connecting to {} over {} ".format(theIP, arguments['port']))

        # connection = netmiko.ConnectHandler(**arguments)
        connection = netmiko.ConnectHandler(**arguments.get_connection_info(include_password=True))

        # Needs to be TYPE <list> for send_multiline
        # connection.send_multiline(commands)

        # Needs to be TYPE <list> and configuration commands
        # connection.send_config_set(commands)
        
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

    # Core Logic Starts Here
    
    # deviceInfo = {'host': input('Enter hostname or IP address: '),
    #           'port': '22',
    #           'device_type': 'cisco_ios',
    #           'username': input('user:'),
    #           'password': pwinput.pwinput(prompt="Password: ", mask='*')}

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