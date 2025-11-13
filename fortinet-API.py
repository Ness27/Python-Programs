"""
Filename: Fortinet-API.py
Description: Run Commands on FortiOS / FortiGates through the REST API.
Author: Hunter R.
Date: 2025-11-12
"""
import logging, time, sys, csv, json
import requests

# ️ Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[
        logging.StreamHandler(sys.stdout)
    ]
)

def writeData(data):
    fieldHeaders = ['name', 'subnet', 'type', 'interface']
    fieldHeaderUsed = ['Address Name', 'Address Subnet', 'Type of Addr', 'Interface']

    with open('results.csv', 'w', newline='') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=fieldHeaders, extrasaction='ignore')
        csvfile.write(','.join(fieldHeaderUsed))
        csvfile.write('\n')
        writer.writerows(data)

    return None

def printData(data):
    parsed_data = json.loads(data.text)
    output_data = json.dumps(parsed_data, indent=4)
    logging.info(output_data)

    return None


def main():
    startTime = time.perf_counter()
    logging.info("Starting main program...")
    setupComplete = time.perf_counter()
    logging.info('Completed initialization in {} seconds.'.format(round(setupComplete-startTime,5)))

    url = "https://10.48.101.250:8443/api/v2/cmdb/firewall/address/"

    payload = {}
    headers = {
        'Authorization': 'Bearer <API-KEY>'
    }

    theResponse = requests.get(url, headers=headers, params=payload, verify=False)

    to_dict = theResponse.json()

    # writeData(to_dict['results'])
    printData(theResponse)


    logging.info("Program finished. - Exiting program.")
    finalTime = time.perf_counter()
    logging.info('Total running time: {} seconds.'.format(round(finalTime-startTime,5)))
    logging.shutdown()


if __name__ == "__main__":
    main()