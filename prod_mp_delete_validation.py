import csv
import requests
from urllib.parse import urlparse
import concurrent.futures
import sys

requests.packages.urllib3.disable_warnings()
def process_url(row):
    source_hash = row['hash']
    print(source_hash)
    url = 'https://paulm-sony.test.edgekey.net/delete/validate?del=' + source_hash
    print(url)
    headers = {"Accept": "text/html"}
    response = requests.get(url, headers=headers, allow_redirects=False)
    #print(f'Response: {response.status_code}, Headers: {response.headers}')
    print(response.content)

def main():

    if len(sys.argv) < 2:
        print('No file provided, no rules to upload')
        sys.exit()
    else:
        file_name = sys.argv[1]

    with open(file_name, newline='') as csvfile:
        reader = csv.DictReader(csvfile)
        rows = list(reader)  # Convert iterator to list to reuse it

    num_threads = 2  # Define the number of threads you want to use

    with concurrent.futures.ThreadPoolExecutor(max_workers=num_threads) as executor:
        futures = [executor.submit(process_url, row) for row in rows]

        for future in concurrent.futures.as_completed(futures):
            future.result()  # This will raise exceptions if any occurred within a thread

if __name__ == "__main__":
    main()
