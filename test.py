"""
Filename: test.py
Description: Brief overview of what this script does.
Author: Hunter R.
Date: 2025-08-02
"""

import argparse
import logging
import sys, time

# ️ Configure logging
logging.basicConfig(
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[
        logging.StreamHandler(sys.stdout)
    ]
)

def callParser():
    parser = argparse.ArgumentParser(prog='test.py',
                                     add_help=True,
                                     description='A Standard Python Template.',
                                     epilog='\nEnd of the help text.')
    parser.add_argument('-e', '--error', action='store_true',help='Enable ERROR level logging', required=False, default=False, dest='error')
    parser.add_argument('-i', '--info', action='store_true',help='Enable INFO level logging', required=False, default=True, dest='info')
    parser.add_argument('-d', "--debug", action="store_true", help="Enable DEBUG level logging", required=False, default=False, dest="debug")
    # Add more arguments as needed

    args = parser.parse_args()

    if len(sys.argv) <= 1:
        parser.print_usage()

    return args

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
    """Main Function."""
    startTime = time.perf_counter()
    logging.info("Initialization Complete.")
    logging.info("Starting Setup...")

    args = callParser()
    setup(args)

    setupComplete = time.perf_counter()
    logging.info('Completed initialization in {} seconds.'.format(round(setupComplete-startTime,5)))

    # Core Program Logic Goes HERE

    logging.info("Program finished. - Exiting program.")
    finalTime = time.perf_counter()
    logging.info('Total running time: {} seconds.'.format(round(finalTime-startTime,5)))
    logging.shutdown()

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        logging.warning("Interrupted by user.")
        sys.exit(0)
