"""
Filename: cli-script-fortinet.py
Description: Run Commands on FortiOS / FortiGates.
Author: Hunter R.
Date: 2025-11-04
"""

import netmiko
from netmiko.fortinet import FortinetSSH
import sys
import logging
import ipaddress
import time
import pwinput
from networking import networkingDevice
import re, jinja2, os

# ️ Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[
        logging.StreamHandler(sys.stdout)
    ]
)

def generateJinjaTemplates(data):
    jinja_env = jinja2.Environment(loader=jinja2.FileSystemLoader(os.getcwd()))
    logging.info("Jinja2 Environment initialized.")
    template = jinja_env.get_template('template.csv')
    result = template.render(extip=data['extip'],port=data['port'], hostname=data['hostname'], internal_ip=data['internal_ip'],vip=data['vip'])
    document = open('output.csv', 'w')
    document.write(result)
    document.close()
    logging.info(f'\n{result}\n')

    return None

def obtainData(output):
    ext_pattern = re.compile(r'extip (\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})')
    mapped_pattern = re.compile(r'mappedip "(\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})"')
    extport_pattern = re.compile(r'extport (\d+)')
    hostName_pattern = re.compile(r'(\w+-FW\w+)')
    vipName_pattern = re.compile(r'edit "(\w+)"')

    logging.info(output)
    getExtIP = ext_pattern.findall(output)
    getMappedIP = mapped_pattern.findall(output)
    getExtPort = extport_pattern.findall(output)
    getHostName = hostName_pattern.findall(output)
    vipName = vipName_pattern.findall(output)
    data = {'extip': getExtIP,
            'hostname': getHostName[0],
            'port': getExtPort,
            'internal_ip': getMappedIP,
            'vip': vipName}

    return data

def connectSession(arguments, commands):
    try:
        theIP = format(ipaddress.ip_address(arguments['host']))
        logging.info("Connecting to {} over {} ".format(theIP, arguments['port']))

        connection = netmiko.ConnectHandler(**arguments.get_connection_info(include_password=True))

        # Needs to be TYPE <list> and configuration commands
        # connection.send_config_set(commands)

        # Needs to be TYPE <list> for send_multiline
        output = connection.send_multiline(commands)

        # Filter and obtain needed data for template.
        data_dict = obtainData(output)

        # Generate the output based on the data handed to the Jinja Templates.
        writeTemplate = generateJinjaTemplates(data_dict)

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

    commandsToRun = ['show firewall vip', 'get system status']

    deviceInfo = networkingDevice(hostname=input('Enter hostname: '), username=input('Enter username: '), device_type='fortinet')
    deviceInfo.set_password(pwinput.pwinput(prompt="Password: ", mask='*'))

    connectSession(deviceInfo, commandsToRun)


    logging.info("Program finished. - Exiting program.")
    finalTime = time.perf_counter()
    logging.info('Total running time: {} seconds.'.format(round(finalTime-startTime,5)))
    logging.shutdown()

if __name__ == "__main__":
    main()