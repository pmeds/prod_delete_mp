import csv
import json
import sys
import requests
import concurrent.futures

# Function to suppress warnings from 'requests' about SSL certificate verification
requests.packages.urllib3.disable_warnings()

def process_row(row):
    json_data = json.dumps(row)
    print(json_data)
    url = 'https://paulm-sony.test.edgekey.net/delete'
    headers = {
        "Content-type": "application/json",
        "User-Agent": "paul-python",
        "Pragma": "akamai-x-ew-debug-rp, akamai-x-ew-onclientrequest, akamai-x-ew-debug-subs, akamai-x-get-client-ip, akamai-x-get-extracted-values,  akamai-x-get-request-id, akamai-x-ew-debug"
    }
    response = requests.post(url, data=json_data, headers=headers, verify=False)
    print(response.status_code, response.headers)

def main(file_name):
    if not file_name:
        print('File not found, no rules to upload')
        return

    with open(file_name, mode='r', newline='', encoding='utf-8-sig') as file:
        reader = csv.DictReader(file)
        rows = list(reader)  # Pre-load all rows into memory for multiprocessing

    # Define the number of processes you want to use
    num_processes = 2

    # Use ProcessPoolExecutor to handle multiprocessing
    with concurrent.futures.ProcessPoolExecutor(max_workers=num_processes) as executor:
        futures = [executor.submit(process_row, row) for row in rows]

        for future in concurrent.futures.as_completed(futures):
            future.result()  # This will raise exceptions if any occurred within a process

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print('No file provided, no rules to upload')
        sys.exit()
    else:
        file_name = sys.argv[1]
        main(file_name)
