import pandas as pd
import hashlib
import csv

# Master file with all the rules
filename = "test-uploader2.xlsx"
#print(filename)

# Output CSV file name
output_csv = "delete-prod-test-upload.csv"

# Header for the CSV file
header = ['hash', 'source', 'destination', 'host']

# Read spreadsheet, openpyxl is required for .xlsx files
df = pd.read_excel(filename, engine='openpyxl')

# Prepare data for writing
data_to_write = []

for index, row in df.iterrows():
    source_data = row['source']
    source_hash = hashlib.sha256(str(source_data).encode('utf-8')).hexdigest()
    destination = row['destination']
    host = row['hostname']
    ekvitem = [source_hash, source_data, destination, host]
    data_to_write.append(ekvitem)

# Write data to a single CSV file
with open(output_csv, 'w', newline='') as csvfile:
    writer = csv.writer(csvfile)
    writer.writerow(header)  # Write the header
    writer.writerows(data_to_write)  # Write the data

print(f"Data written to {output_csv}")
