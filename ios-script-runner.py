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

def connectSession(ip, username, password, port, commandsfile):
    with SSHClient() as client:
        ## Allows for auto-adding server SSH key on client host - On First Connection
        client.set_missing_host_key_policy(AutoAddPolicy())
        try:
            theIP = format(ipaddress.ip_address(ip))
            logging.info("Connecting to {} over {} ".format(theIP, port))

            file_extension = os.path.splitext(commandsfile)
            if file_extension[1] == ".txt":
                client.connect(theIP, username=username, password=password, port=int(port))
                with open(commandsfile, 'r') as file:
                    for line in file:
                        print(line.strip())
                       # stdin, stdout, stderr = client.exec_command(line.strip())
                       # print(stdout.read().decode())
            else:
                logging.error("The file <{}> is not a .txt file. - Exiting program.".format(commandsfile))
                exit(1)
        except SSHException as e:
            print(e)
        except ValueError as val:
            logging.error('{}'.format(val))
            logging.error("Skipping {}".format(str(val).split(' ')[0]))
            return None
        except TimeoutError:
            logging.error("There was an error: {}".format("TimeoutError"))
            logging.error("Skipping {}".format(ip))
            return None
        except KeyboardInterrupt:
            logging.exception("User interrupt.")
            logging.error("There was an error: {}".format("KeyboardInterrupt"))
            logging.error("Exiting program.")
            exit(1)

    return None

def main():
    startTime = time.perf_counter()
    logging.info("Setup complete.")
    logging.info("Starting main program...")
    setupComplete = time.perf_counter()
    logging.info('Completed initialization in {} seconds.'.format(round(setupComplete-startTime,5)))

    commandsToRun = ['do show ip int br']

    deviceInfo = dict(host='10.132.101.252', device_type='cisco_ios', username=input('user:'), password=pwinput.pwinput(prompt="Password: ", mask='*'))



    logging.info("Program finished. - Exiting program.")
    logging.shutdown()

if __name__ == "__main__":
    main()
