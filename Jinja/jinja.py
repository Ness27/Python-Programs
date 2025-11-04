"""
Filename: jinja.py
Description: Sample Jinja Script for Templating
Author: Hunter R.
Date: 2025-11-03
"""

import sys, time
import logging
import subprocess
from subprocess import check_output
import os
import jinja2
import re


# ️ Configure logging
logging.basicConfig(
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[
        logging.StreamHandler(sys.stdout)
    ],
    level=logging.INFO,
)

def my_logging(func):
    import time
    def wrapper(*args, **kwargs):
        start_time = time.perf_counter()
        logging.info("Initializing {}() function.".format(func.__name__))
        result = func(*args, **kwargs)
        end_time = time.perf_counter()
        logging.info(
            f"Finished running {func.__name__}() function with args={args}, kwargs={kwargs} "
            f"in {end_time - start_time:.5f} seconds."
        )
        return result
    return wrapper


@my_logging
def main():
    """Main Function."""

    logging.info('Running Jinja2 Enviroment from File System Loader on Directory --> {}'.format(os.getcwd()))
    jinja_env = jinja2.Environment(loader=jinja2.FileSystemLoader(os.getcwd()))
    logging.info("Jinja2 Environment initialized.")
    template = jinja_env.get_template('j-template.txt')

    pattern = re.compile(r'(\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})')

    theCalledHost = input('Input Hostname: ').strip()

    returnedOutput = subprocess.check_output(f'nslookup {theCalledHost}').decode('utf-8')

    ipAddrList = pattern.findall(returnedOutput)
    logging.info("host list: {}".format(ipAddrList))
    result = template.render(ipList=ipAddrList, hostname=theCalledHost)
    logging.info(f'\n{result}\n')


    # for ipAddr in ipAddrList:
    #     result = template.render(ip_address=ipAddr, hostname=theCalledHost)
    #     logging.info(f'\n{result}\n')

    theDict = {'ip_address': '10.1.1.1', 'hostname': 'google.com', 'port': '22'}

    time.sleep(0.1)


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        logging.warning("Interrupted by user.")
        sys.exit(0)
