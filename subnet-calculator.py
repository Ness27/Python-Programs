"""
Filename: subnet-calculator.py
Description: An application for network administrators and engineers to calculator network subnets.
Author: Hunter R.
Date: 2025-07-27
"""

import argparse
import logging
import sys
import tkinter as tk
import ipaddress
import time

# ️ Configure logging
logging.basicConfig(
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[
        logging.StreamHandler(sys.stdout)
    ]
)

def showResults(theWindow, resultData):
    resultWindow = tk.Toplevel()
    resultWindow.title("Network Results")
    resultWindow.geometry("400x500")
    theWindow.eval(f'tk::PlaceWindow {str(resultWindow)} center')

    row = 0
    for key, value in resultData.items():
        displayText = value if not isinstance(value, list) else "\n".join(value)
        tk.Label(resultWindow, text=f"{key}:").grid(row=row, column=0, sticky="w", padx=5)
        tk.Label(resultWindow, text=displayText).grid(row=row, column=1, sticky="w", padx=5)
        row += 1
        if row > 20:
            break
    quitButton = tk.Button(resultWindow, text='Close', bg='darkred',fg='white',command=resultWindow.destroy)
    quitButton.grid(row=row+1, column=1, sticky="w", padx=5)


def networkEval(networkBoth):
    theNetwork = ipaddress.ip_interface(networkBoth)
    net = theNetwork.network

    show_Hosts = [str(ip) for idx, ip in enumerate(net.hosts()) if idx < 20]

    return {
        "Network Address": str(net.network_address),
        "Broadcast Address": str(net.broadcast_address),
        "Subnet Mask": str(theNetwork.netmask),
        "Wildcard Mask": str(theNetwork.hostmask),
        "Private Network Space": str(theNetwork.is_private),
        "Public Network Space": str(theNetwork.is_global),
        "Total Number of Hosts": str(net.num_addresses),
        "Number of Usable Hosts": str(max(net.num_addresses - 2, 0)),
        "Available Hosts": show_Hosts
    }



def windowCreation():
    window = tk.Tk()
    window.title("Subnet Calculator")
    window.eval('tk::PlaceWindow . center')
    window.geometry("420x200")
    # window.frame()

    theTitle = tk.Label(window, text="Welcome to Subnet Calculator\n")

    # tk.Label(window, text="Enter the IP:").grid(row=0)
    # tk.Label(window, text="Enter the subnet:").grid(row=1)
    enterIP = tk.Label(window, text="Enter the IP and Subnet Mask:",fg='black',justify='left')

    networkBoth = tk.Entry(window, width=25, justify="left", fg="black", bg="lightgrey")
    networkBoth.insert(10,'10.1.1.1/24')

    runButton = tk.Button(window, bg='green',fg='white', text='Run', command=lambda:showResults(window,networkEval(networkBoth.get())))
    quitButton = tk.Button(window, text='Quit', bg='darkred',fg='white', command=window.destroy)

    theTitle.place(x=125, y=10)
    enterIP.place(x=50, y=50,width=200)
    networkBoth.place(x=245, y=50)
    runButton.place(x=160, y=120, width=100)
    quitButton.place(x=160, y=145, width=100)

    window.mainloop()




def setup(args):
    """Initial setup before main logic runs."""
    if args.debug:
        logging.getLogger().setLevel(logging.DEBUG)
    elif args.error:
        logging.getLogger().setLevel(logging.ERROR)
    elif args.info:
        logging.getLogger().setLevel(logging.INFO)
    else:
        logging.getLogger().setLevel(logging.DEBUG)
    logging.info("Setup complete.")

def main():
    """Main entry point of the script."""
    startTime = time.perf_counter()
    parser = argparse.ArgumentParser(prog='subnet-calculator.py',
                                     add_help=True,
                                     description='An application for network administrators and engineers to calculator network subnets.',
                                     epilog='\nEnd of the help text.')
    parser.add_argument('-e', '--error', action='store_true',help='Enable ERROR level logging', required=False, default=False, dest='error')
    parser.add_argument('-i', '--info', action='store_true',help='Enable INFO level logging', required=False, default=True, dest='info')
    parser.add_argument('-d', "--debug", action="store_true", help="Enable DEBUG level logging", required=False, default=False, dest="debug")
    # Add more arguments as needed

    args = parser.parse_args()
    setup(args)
    logging.info("Starting main program...")
    setupComplete = time.perf_counter()
    logging.info('Completed initialization in {} seconds.'.format(round(setupComplete-startTime,5)))
    # Core Program Logic Goes HERE
    windowCreation()
    logging.info("Program finished.")
    finalTime = time.perf_counter()
    logging.info('Total running time: {} seconds.'.format(round(finalTime-startTime,5)))
    logging.shutdown()

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        logging.warning("Interrupted by user.")
        sys.exit(0)
    except Exception as e:
        logging.exception(f"An unexpected error occurred: {e}")
        sys.exit(1)

