import pandas as pd
from pandas.io.json import json_normalize
import json
import xml.etree.ElementTree as ET
import xmltodict
import json
import collections

### re opens the JSON file for further processing   ### 
with open('tempfile.json') as json_file: 
    data = json.load(json_file) 
  



### Function to completely flatten the JSON ##
### This will be used to create a Pandas    ##
### dataframe. From there it will be saved  ##
### as a CSV.

crumbs = False  ### True creates a verbose output
def flatten(dictionary, parent_key=False, separator='.'):
    """
    Turn a nested dictionary into a flattened dictionary
    :param dictionary: The dictionary to flatten
    :param parent_key: The string to prepend to dictionary's keys
    :param separator: The string used to separate flattened keys
    :return: A flattened dictionary
    """

    items = []
    for key, value in dictionary.items():
        if crumbs: print('checking:',key)
        new_key = str(parent_key) + separator + key if parent_key else key
        if isinstance(value, collections.MutableMapping):
            if crumbs: print(new_key,': dict found')
            if not value.items():
                if crumbs: print('Adding key-value pair:',new_key,None)
                items.append((new_key,None))
            else:
                items.extend(flatten(value, new_key, separator).items())
        elif isinstance(value, list):
            if crumbs: print(new_key,': list found')
            if len(value):
                for k, v in enumerate(value):
                    items.extend(flatten({str(k): v}, new_key).items())
            else:
                if crumbs: print('Adding key-value pair:',new_key,None)
                items.append((new_key,None))
        else:
            if crumbs: print('Adding key-value pair:',new_key,value)
            items.append((new_key, value))
    return dict(items)





### Using the function and sending the JSON data to it  ##
ans = flatten(data)

### Getting the data pandas ready
prep = json_normalize(ans)

### creating a pandas dataframe 
df = pd.DataFrame(prep)

### saving the dataframe to a CSV
df.to_csv('results.csv')
