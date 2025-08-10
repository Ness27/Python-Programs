"""
Filename: dir-walk.py
Description: Brief overview of what this script does.
Author: Hunter/Ness27
Date: 2025-08-09
"""

import sys
import os

def main():
    """Main Function."""

    selectDir = input('Enter a directory to walk: ')
    if selectDir == '' or (not os.path.exists(selectDir)):
        print('<{}> is not a valid directory.'.format(selectDir))
        selectDir = os.getcwd()
    else:
        selectDir = os.path.abspath(selectDir)

    print('\nCurrent Directory-> {}\n'.format(selectDir))

    skipdir = os.getcwd() + '.git'
    print(' ')
    for directory, subdirectories, files in os.walk(selectDir):
        if set(skipdir).issubset(directory):
            pass
        else:
            print('Directory -> {}\t'.format(directory))
            if len(subdirectories) > 0:
                for item in subdirectories:
                    print('Subdirectory -> {}'.format(item))
            else:
                print('Subdirectory -> NONE')
            if len(files) > 0:
                for item in files:
                    print('File -> {}'.format(item))
            else:
                print('File -> NONE')
            print(' ')



if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("Interrupted by user.")
        sys.exit(0)
