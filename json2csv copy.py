import json
import csv

# Read the JSON data from the file
with open('dei-prod.json') as json_file:
    data = json.load(json_file)

# Extract the "Patches" list from the JSON data
patches = data['Patches']

# Define the field names for the CSV file
field_names = ['Title', 'KBId', 'Classification', 'Severity', 'State', 'InstalledTime', 'CVEIds']

# Specify the output CSV file name
output_file = 'dei-prod.csv'

# Open the CSV file in write mode
with open(output_file, 'w', newline='') as csv_file:
    # Create a CSV writer object
    writer = csv.DictWriter(csv_file, fieldnames=field_names)

    # Write the field names as the header row in the CSV file
    writer.writeheader()

    # Write each patch as a row in the CSV file
    for patch in patches:
        writer.writerow(patch)