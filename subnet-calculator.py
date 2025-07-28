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
        displayText = value if not isinstance(value, list) else "\n".join(value[:20])
        tk.Label(resultWindow, text=f"{key}:").grid(row=row, column=0, sticky="w", padx=5)
        tk.Label(resultWindow, text=displayText).grid(row=row, column=1, sticky="w", padx=5)
        row += 1
    quitButton = tk.Button(resultWindow, text='Quit', command=resultWindow.destroy)
    quitButton.grid(row=row+1, column=1, sticky="w", padx=5)


def networkEval(networkBoth):
    theNetwork = ipaddress.ip_interface(networkBoth)
    theNetaddr = theNetwork.network.network_address
    logging.debug(f"Network address: {theNetaddr}")
    return {
        "Network Address": str(theNetwork.network.network_address),
        "Broadcast Address": str(theNetwork.network.broadcast_address),
        "Subnet Mask": str(theNetwork.netmask),
        "Wildcard Mask": str(theNetwork.hostmask),
        "Private Network Space": str(theNetwork.is_private),
        "Public Network Space": str(theNetwork.is_global),
        "Total Number of Hosts": len([str(host) for host in theNetwork.network.hosts()]) + 2,
        "Number of Usable Hosts": str(len([str(host) for host in theNetwork.network.hosts()])),
        "Available Hosts": [str(host) for host in theNetwork.network.hosts()]
    }



def windowCreation():
    window = tk.Tk()
    window.title("Subnet Calculator")
    window.eval('tk::PlaceWindow . center')
    window.geometry("420x60")


    greeting = tk.Label(window, text="Welcome to Subnet Calculator\n")
    # greeting.pack()
    #
    # tk.Label(window, text="Enter the IP:").grid(row=0)
    # tk.Label(window, text="Enter the subnet:").grid(row=1)
    tk.Label(window, text="Enter the IP and Subnet Mask:").grid(row=2)

    networkBoth = tk.Entry(window, width=25, justify="left")
    networkBoth.insert(10,'10.1.1.1/24')
    networkBoth.grid(row=2, column=1)

    runButton = tk.Button(window, text='Run', command=lambda:showResults(window,networkEval(networkBoth.get())))
    runButton.grid(row=3, column=0, sticky=tk.W, pady=5, padx=105)
    quitButton = tk.Button(window, text='Quit', command=window.destroy)
    quitButton.grid(row=3, column=1, sticky=tk.W, pady=5, padx=15)


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
    # Core Program Logic Goes HERE
    windowCreation()
    logging.info("Program finished.")
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

