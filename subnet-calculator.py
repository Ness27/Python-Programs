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

# ️ Configure logging
logging.basicConfig(
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[
        logging.StreamHandler(sys.stdout)
    ]
)


def windowCreation():
    window = tk.Tk()
    window.title("Subnet Calculator")
    window.eval('tk::PlaceWindow . center')

    greeting = tk.Label(window, text="Welcome to Subnet Calculator\n")
    # greeting.pack()

    tk.Label(window, text="Enter the IP:").grid(row=0)
    tk.Label(window, text="Enter the subnet:").grid(row=1)
    # netAddGrt.pack()

    networkAddress = tk.Entry(window, width=80, justify="left").grid(row=0, column=1)
    networkSubnet = tk.Entry(window, width=80, justify="left").grid(row=1, column=1)
    # networkAddress.insert(0, "x.x.x.x")
    # networkAddress.pack()
    save_ip = ''
    # Bind the Return key (Enter) to save_ip
    # networkAddress.bind("<Return>", save_ip)
    logging.info('ip is {}'.format(save_ip))

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
        logging.getLogger().setLevel(logging.INFO)
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
    logging.debug("TEST")
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

