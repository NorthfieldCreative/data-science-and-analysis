import numpy as np
import pandas as pd
import matplotlib.pyplot as plt


datatest = pd.read_csv('test.csv', low_memory=False)
#datatest['result'] = np.where(datatest['column1'] == datatest['column2'], '1', '0')
cisalist = pd.read_csv('cisaknownexploited.csv', low_memory=False)
searchfor = cisalist['cveID']

# if any part is in
#datatest['results'] = datatest[datatest['column2'].str.contains('|'.join(searchfor))]
datatest['results'] = datatest[datatest['column2'].str.contains('|'.join(searchfor))]

datatest.dropna(subset=['results'], inplace=True)
datatest.to_csv(r'datatestresults.csv', index = False)