import numpy as np
import pandas as pd
import matplotlib.pyplot as plt



########################################################
# Open the exported list of assets with cves from tenable
#########################################################
machines = pd.read_csv('warfiles.csv', low_memory=False)

###########
# Because hosts with more than one cve are comma separated within the same 
# row, we need to Separate all cves respective rows maintaining other attributes
###########

machines["ComputerName"]=machines["ComputerName"].str.split(' ')
machinesseparated=(machines.explode("ComputerName").reset_index(drop=True))
machinesseparated.to_csv(r'warfilesfound.csv', index = False)
