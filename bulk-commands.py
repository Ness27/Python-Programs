"""
Filename: bulk-commands.py
Description: Brief overview of what this script does.
Author: Hunter R.
Date: 2025-07-26
"""

import argparse
import os
import logging
import sys, time
import pwinput
import ipaddress
import netmiko

# ️ Configure logging
logging.basicConfig(
    level=logging.DEBUG,
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[
        logging.StreamHandler(sys.stdout)
    ]
)


def callParser():
    parser = argparse.ArgumentParser(prog='bulk-commands.py',
                                     add_help=True,
                                     description='A Standard Interactive SSH Client and Automated Commands.',
                                     epilog='\nEnd of the help text.')
    subParser = parser.add_subparsers(title='subcommands', dest='command', required=True)
    hosts_parser = subParser.add_parser('hostfile',help='Run commands against a list of hosts in a .txt file.')
    hosts_parser.add_argument('hostfile', type=str, help='A .txt file with a list of hosts IP addresses.')
    hosts_parser.add_argument('commandsfile', type=str, help='A .txt file with a list of commands to run. One command per line.')
    hosts_parser.add_argument('-p','--port', metavar='<port>', required=False, dest='port', type=str, help='[Optional] Port to initiate connection to. Default = 22', default='22')

    ssh_parser = subParser.add_parser('ssh',help='Enter the IP address of a remote host to connect to and run commands against.')
    ssh_parser.add_argument('ip', type=str, help='IPv4 Address to connect to in the notation of X.X.X.X. Defaults = 127.0.0.1', default='127.0.0.1')
    ssh_parser.add_argument('-p','--port', metavar='<port>', required=False, dest='port', type=str, help='[Optional] Port to initiate connection to. Default = 22', default='22')
    ssh_parser.add_argument('commandsfile', type=str, help='A .txt file with a list of commands to run. One command per line.')

    arguments = parser.parse_args()
    return arguments


def connectSession(ip, username, password, port, commandsfile):
    try:
        theIP = format(ipaddress.ip_address(ip))
        logging.info("Connecting to {} over {} ".format(theIP, port))

        deviceInfo = {'host': theIP,
                      'port': port,
                      'device_type': 'cisco_ios',
                      'username': username,
                      'password': password}

        file_extension = os.path.splitext(commandsfile)
        if file_extension[1] == ".txt":
            ssh_connection = netmiko.ConnectHandler(**deviceInfo)
            ssh_connection.send_config_from_file(commandsfile)
            ssh_connection.disconnect()
        else:
            logging.error("The file <{}> is not a .txt file. Abort Connection.".format(commandsfile))
    except ValueError as val:
        logging.error('{}'.format(val))
        logging.error("Skipping {}".format(str(val).split(' ')[0]))
    except TimeoutError:
        logging.error("There was an error: {}".format("TimeoutError"))
        logging.error("Skipping {}".format(ip))
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
    logging.info("Initialization Complete.")
    logging.info("Starting Setup...")

    # Get arguments
    arguments = callParser()

    setupComplete = time.perf_counter()
    logging.info('Completed initialization in {} seconds.'.format(round(setupComplete-startTime,5)))

    # Get username and password to sign into device.
    arguments.username = input("Username: ")
    arguments.password = pwinput.pwinput(prompt="Password: ", mask='*')

    if arguments.command == 'hostfile':
        file_extension = os.path.splitext(arguments.hostfile)
        if file_extension[1] == ".txt":
            with open(arguments.hostfile, 'r') as file:
                for line in file:
                    theIp = line.strip()
                    connectSession(theIp, arguments.username, arguments.password, arguments.port, arguments.commandsfile)
        else:
            logging.error("The file <{}> is not a .txt file. - Exiting program.".format(arguments.hostfile))
            pass
    elif arguments.command == 'ssh':
        connectSession(arguments.ip, arguments.username, arguments.password, arguments.port, arguments.commandsfile)
    else:
        print("\n" + arguments.format_usage())

    logging.info("Program finished. - Exiting program.")
    finalTime = time.perf_counter()
    logging.info('Total running time: {} seconds.'.format(round(finalTime-startTime,5)))
    logging.shutdown()

if __name__ == "__main__":
    main()
