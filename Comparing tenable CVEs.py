import numpy as np
import pandas as pd
import matplotlib.pyplot as plt




df1 = pd.DataFrame({'domains': ['intelisecure', 'hotmail', 'gmail', 'user@gmail.com']})


tenableassets = pd.read_csv('tenableassets.csv', low_memory=False)

###########
# Because hosts with more than one cve are comma separated within the same 
# row, we need to Separate all cves into a new column
###########
tenableassets["CVE"]=tenableassets["CVE"].str.split(',')
assetswithseparatedcves=(tenableassets.explode("CVE").reset_index(drop=True))

##assetswithseparatedcves.to_csv(r'cvelist.csv', index = False)

cisalist = pd.read_csv('cisaknownexploited.csv', low_memory=False) 
searchfor = cisalist['cveID']


assetswithseparatedcves.dropna(subset=['CVE'], inplace=True)
#assetswithseparatedcves['results'] = assetswithseparatedcves[assetswithseparatedcves['CVE'].str.contains('|'.join(searchfor))]
results = assetswithseparatedcves[assetswithseparatedcves['CVE'].str.contains('|'.join(searchfor))]

#assetswithseparatedcves.dropna(subset=['results'], inplace=True)

results.drop(['Asset UUID', 'CVSS', 'CVSS Base Score', 'CVSS Temporal Score', 'CVSS Temporal Vector', 'CVSS Vector', 'CVSS3 Base Score', 'CVSS3 Temporal Score', 'CVSS3 Temporal Vector', 'CVSS3 Vector', 'Host End', 'Host Start', 'NetBios', 'Plugin Family', 'Plugin ID', 'Port', 'Protocol', 'Risk', 'System Type', 'Vulnerability Priority Rating (VPR)', 'Vulnerability State', 'First Seen', 'Last Seen', 'Recast Reason'],axis=1, inplace=True)
#results.drop('Asset UUID',axis=1, inplace=True)
results.to_csv(r'results.csv', index = False)