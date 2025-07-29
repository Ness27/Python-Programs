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
import tkinter as tk
from tkinter import scrolledtext


# ️ Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[
        logging.StreamHandler(sys.stdout)
    ]
)

def getData(logOutput, theHosts, theCommands, theUser, thePass):

    deviceInfo = {'host':'',
                  'port':'22',
                  'device_type':'cisco_ios',
                  'username':'',
                  'password':''}

    hostList = theHosts.strip().splitlines()
    commandList = theCommands.strip().splitlines()

    for host in hostList:
        deviceInfo['host'] = host
        deviceInfo['username'] = theUser
        deviceInfo['password'] = thePass
        logOutput.config(state='normal')
        logOutput.insert(tk.END, "Connecting to {} over {}".format(deviceInfo['host'], deviceInfo['port']) + '\n')
        logOutput.see(tk.END)
        logOutput.config(state='disabled')
        logOutput.update()
        connectSession(deviceInfo, commandList)

    return None



def windowCreation():
    window = tk.Tk()
    window.title("IOS-XE Script Runner")
    window.eval('tk::PlaceWindow . center')
    window.geometry("1000x600")

    theTitle = tk.Label(window, text="Welcome to IOS Script Runner\n")

    hostLabel = tk.Label(window, text="Enter the hosts to connect to: (One host per line)",fg='black',justify='left')

    hostRequest = tk.Text(window, height=10, width=40, fg="black", bg="lightgrey")

    commandLabel = tk.Label(window, text="Enter the commands to execute on the host (one command per line):",fg='black',justify='left')

    commandRequest = tk.Text(window, height=10, width=40, fg="black", bg="lightgrey")

    usernameLabel = tk.Label(window, text="Enter your username:")
    usernameRequest = tk.Entry(window, width=40, fg="black", bg="lightgrey")
    passwordLabel = tk.Label(window, text="Enter your password:")
    passwordEntry = tk.Entry(window, width=40, fg="black", bg="lightgrey")

    logLabel = tk.Label(window, text="Script Output / Log:", fg='black', justify='left')
    logOutput = scrolledtext.ScrolledText(window, height=10, width=70, fg="white", bg="black", state='disabled')

    runButton = tk.Button(window, bg='green',fg='white', text='Run', command=lambda: getData(logOutput, hostRequest.get('1.0', tk.END),
                                                                                             commandRequest.get('1.0', tk.END),
                                                                                             usernameRequest.get(), passwordEntry.get()))
    quitButton = tk.Button(window, text='Quit', bg='darkred',fg='white', command=window.destroy)


    theTitle.grid(row=1, column=1)
    hostLabel.grid(row=1, column=1)
    hostRequest.grid(row=1, column=2)
    commandLabel.grid(row=2, column=1)
    commandRequest.grid(row=2, column=2)
    usernameLabel.grid(row=3, column=1)
    usernameRequest.grid(row=3, column=2)
    passwordLabel.grid(row=4, column=1)
    passwordEntry.grid(row=4, column=2)
    runButton.grid(row=5, column=1)
    quitButton.grid(row=5, column=2)
    logLabel.grid(row=6, column=1)
    logOutput.grid(row=6, column=2, columnspan=2)


    window.mainloop()

    return None

def connectSession(arguments, commands):
    try:
        theIP = format(ipaddress.ip_address(arguments['host']))
        logging.info("Connecting to {} over {} ".format(theIP, arguments['port']))


        connection = netmiko.ConnectHandler(**arguments)
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

    windowCreation()

    logging.info("Program finished. - Exiting program.")
    finalTime = time.perf_counter()
    logging.info('Total running time: {} seconds.'.format(round(finalTime-startTime,5)))
    logging.shutdown()

if __name__ == "__main__":
    main()
