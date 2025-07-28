"""
Filename: bulk-commands.py
Description: Brief overview of what this script does.
Author: Hunter R.
Date: 2025-07-26
"""

import argparse
import os
import logging
import sys
import pwinput
import ipaddress
from paramiko import SSHClient, SSHException
from paramiko.client import AutoAddPolicy

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
    arguments = callParser()
    logging.debug(arguments)
    logging.info("Setup complete.")
    logging.info("Starting main program...")
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
            exit(1)
    elif arguments.command == 'ssh':
        connectSession(arguments.ip, arguments.username, arguments.password, arguments.port, arguments.commandsfile)
    else:
        print("\n" + arguments.format_usage())

    logging.info("Program finished. - Exiting program.")
    logging.shutdown()

if __name__ == "__main__":
    main()
