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
        connectSession(logOutput, deviceInfo, commandList)

    logOutput.config(state='normal')
    logOutput.insert(tk.END, "✅ Completed Program." + '\n' + "✅ Now Exiting Program." + '\n')
    logOutput.see(tk.END)
    logOutput.config(state='disabled')
    logOutput.update()

    return None

def centerWindow(window, width=1200, height=900):
    window.update_idletasks()  # ensures geometry data is ready
    screen_width = window.winfo_screenwidth()
    screen_height = window.winfo_screenheight()

    x_position = int((screen_width / 2) - (width / 2))
    y_position = int((screen_height / 2) - (height / 2))

    window.geometry(f"{width}x{height}+{x_position}+{y_position}")




def windowCreation():
    window = tk.Tk()
    window.title("IOS-XE Script Runner")
    centerWindow(window)

    theTitle = tk.Label(window, text="Welcome to IOS Script Runner\n")

    hostLabel = tk.Label(window, text="Enter the hosts to connect to: (One host per line)",fg='black',justify='left')

    hostRequest = tk.Text(window, height=20, width=30, fg="black", bg="lightgrey")

    commandLabel = tk.Label(window, text="Enter the commands to execute on the host (one command per line):",fg='black',justify='left')

    commandRequest = tk.Text(window, height=10, width=60, fg="black", bg="lightgrey")

    usernameLabel = tk.Label(window, text="Enter your username:")
    usernameRequest = tk.Entry(window, width=40, fg="black", bg="lightgrey")
    passwordLabel = tk.Label(window, text="Enter your password:")
    passwordEntry = tk.Entry(window, width=40, fg="black", bg="lightgrey", show="*")

    logLabel = tk.Label(window, text="Script Log:", fg='black', justify='left')
    logOutput = scrolledtext.ScrolledText(window, height=15, width=100, fg="white", bg="black", state='disabled')

    runButton = tk.Button(window, bg='green',fg='white', text='Run', command=lambda: getData(logOutput, hostRequest.get('1.0', tk.END),
                                                                                             commandRequest.get('1.0', tk.END),
                                                                                             usernameRequest.get(), passwordEntry.get()))
    quitButton = tk.Button(window, text='Quit', bg='darkred',fg='white', command=window.destroy)


    # theTitle.grid(row=1, column=1)
    hostLabel.grid(row=1, column=1)
    hostRequest.grid(row=1, column=2)
    commandLabel.grid(row=2, column=1)
    commandRequest.grid(row=2, column=2)
    usernameLabel.grid(row=3, column=1)
    usernameRequest.grid(row=3, column=2)
    passwordLabel.grid(row=4, column=1)
    passwordEntry.grid(row=4, column=2)
    runButton.grid(row=5, column=1, pady=10)
    quitButton.grid(row=5, column=2, pady=10)
    logLabel.grid(row=6, column=1)
    logOutput.grid(row=6, column=2, columnspan=2, pady=10)


    window.mainloop()

    return None

def connectSession(logOutput, arguments, commands):
    def logMessage(msg):
        logOutput.config(state='normal')
        logOutput.insert(tk.END, msg + '\n')
        logOutput.see(tk.END)
        logOutput.config(state='disabled')
        logOutput.update()
    try:
        theIP = format(ipaddress.ip_address(arguments['host']))
        logging.info(f"Connecting to {theIP} over {arguments['port']}")
        logMessage(f"🔌 Connecting to {theIP} over port {arguments['port']}...")

        connection = netmiko.ConnectHandler(**arguments)
        logMessage(f"✅ Connected to {arguments['host']}")

        for cmd in commands:
            logMessage(f"📤 Sending command: {cmd}")
            try:
                output = connection.send_command(cmd)
                logging.info(output)
                logMessage(f"📥 Output from <{cmd}>:\n{output}")
            except Exception as cmdError:
                logMessage(f"❌ Error executing command <{cmd}>: {cmdError}")
                logging.error(f"Command execution error: {cmdError}")

        connection.disconnect()
        logMessage("🔒 Disconnected.\n")

    except ValueError as val:
        msg = str(val).split(' ')[0]
        logging.error(val)
        logging.error(f"Skipping {msg}")
        logMessage(f"❌ ValueError: {val}\nSkipping {msg}")
    except TimeoutError:
        logging.error("TimeoutError")
        logging.error(f"Skipping {arguments['host']}")
        logMessage(f"⏳ TimeoutError on {arguments['host']}\nSkipping host.")
    except KeyboardInterrupt:
        logging.exception("User interrupt.")
        logging.error("KeyboardInterrupt - Exiting.")
        logMessage("🛑 Interrupted by user. Exiting...")
        exit(1)
    except netmiko.exceptions.NetMikoTimeoutException as theError:
        logging.error(f"NetMikoTimeoutException: {theError}")
        logMessage(f"⚠️ Connection timeout on {arguments['host']}: {theError}")

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
