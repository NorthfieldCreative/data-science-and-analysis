import numpy as np
import pandas as pd
import matplotlib.pyplot as plt



########################################################
# Open the exported list of assets with cves from tenable
#########################################################
tenableassets = pd.read_csv('tenableassets.csv', low_memory=False)

###########
# Because hosts with more than one cve are comma separated within the same 
# row, we need to Separate all cves respective rows maintaining other attributes
###########
tenableassets["CVE"]=tenableassets["CVE"].str.split(',')
assetswithseparatedcves=(tenableassets.explode("CVE").reset_index(drop=True))
assetswithseparatedcves.to_csv(r'allcves.csv', index = False)