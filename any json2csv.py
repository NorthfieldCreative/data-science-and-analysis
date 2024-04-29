import pandas as pd
import json

def flatten_json(data, prefix=''):
    if isinstance(data, dict):
        flattened_data = {}
        for key, value in data.items():
            new_key = f'{prefix}.{key}' if prefix else key
            flattened_data.update(flatten_json(value, prefix=new_key))
        return flattened_data
    elif isinstance(data, list):
        flattened_data = {}
        for idx, item in enumerate(data):
            new_key = f'{prefix}.{idx}' if prefix else str(idx)
            flattened_data.update(flatten_json(item, prefix=new_key))
        return flattened_data
    else:
        return {prefix: data}

# Read the JSON data from the file
with open('dei-prod.json') as json_file:
    data = json.load(json_file)

# Flatten the JSON data
flattened_data = flatten_json(data)

# Convert the flattened data to a DataFrame
df = pd.DataFrame([flattened_data])

# Specify the output CSV file name
output_file = 'output.csv'

# Save the DataFrame to a CSV file
df.to_csv(output_file, index=False)