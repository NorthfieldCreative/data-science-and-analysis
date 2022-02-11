import pandas as pd
rawdata1 = pd.read_csv('1.csv', low_memory=False)
rawdata2 = pd.read_csv('2.csv', low_memory=False)
rawdata3 = pd.read_csv('3.csv', low_memory=False)
rawdata4 = pd.read_csv('4.csv', low_memory=False)
rawdatacleanup = [rawdata1, rawdata2, rawdata3, rawdata4]

consolidateddata = pd.concat(rawdatacleanup)

consolidateddata.to_csv(r'consolidated data.csv', index = False)