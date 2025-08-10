"""
Filename: datetime-calculator.py
Description: Brief overview of what this script does.
Author: Hunter/Ness27
Date: 2025-08-09
"""

import sys
import datetime
import time
from dateutil.relativedelta import relativedelta


def change_date_format(date_str):
    formats = ["%Y-%m-%d", "%m-%d-%Y", "%d-%m-%Y"]
    for fmt in formats:
        try:
            parsed = datetime.datetime.strptime(date_str, fmt)
            # print(f"Format matched: {fmt} → Parsed date: {parsed.date().strftime(fmt)}")
            # print('Returning Date in Format of: {}'.format(parsed.date().strftime("%Y-%m-%d")))
            return parsed.date().strftime("%Y-%m-%d")
        except ValueError:
            continue
    return "Unknown or unsupported date format."


def main():
    """Main Function."""
    print('*' * 100 + '\n' + '*' * 100 + '\n')
    print('Datetime Calculator\n')
    print('*' * 100 + '\n' + '*' * 100 + '\n')

    currentDay = datetime.date.today()
    theDay = currentDay.strftime("%A %d, %B %Y")
    print(f"\nCurrent Day -> \t\t{theDay} ({change_date_format(currentDay.strftime("%d-%m-%Y"))})\n\n")

    enterDate = input('Enter destination date (yyyy-mm-dd) or (mm-dd-yyy): ')
    enterDate = change_date_format(enterDate)

    try:
        destinationDate = datetime.date(
            int(enterDate[0:4]),
            int(enterDate[5:7]),
            int(enterDate[8:10])
        )
    except ValueError:
        print("Invalid date format.")
        return

    # Calculate difference
    if destinationDate >= currentDay:
        delta = relativedelta(destinationDate, currentDay)
        direction = "from now"
    else:
        delta = relativedelta(currentDay, destinationDate)
        direction = "ago"

    timing = 0
    while timing < 3:
        print('.', end='', flush=True)  # flush forces immediate output
        time.sleep(1)
        timing += 1

    print(f"\n\nCurrent Day -> \t\t{theDay} ({change_date_format(currentDay.strftime("%d-%m-%Y"))})")
    print(f"Destination Date -> \t{destinationDate.strftime('%A %d, %B %Y')} ({enterDate})")
    print(f"Time Delta -> \t\t{delta.years} years, {delta.months} months, {delta.days} days {direction}\n")




if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\nInterrupted by user.")
        sys.exit(0)
