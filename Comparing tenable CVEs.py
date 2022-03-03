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



############################################
# loading the CISA list and assigning the CVE column to 
# a variable that can be searched
############################################

cisalist = pd.read_csv('cisaknownexploited.csv', low_memory=False) 
searchfor = cisalist['cveID']


##################################
# dropping machines without a CVE from the 
# table so the data can be parsed
##################################

assetswithseparatedcves.dropna(subset=['CVE'], inplace=True)


#############################################
# comparing the list of known exploitable CVEs to the
# list available from the tenable export and assigning it
# to another variable for further processing
##############################################

results = assetswithseparatedcves[assetswithseparatedcves['CVE'].str.contains('|'.join(searchfor))]


#################################################
# Dropping all of the columns that don't provide
# too much value during remediation
##################################################

results.drop(['Asset UUID', 'CVSS', 'CVSS Base Score', 'CVSS Temporal Score', 'CVSS Temporal Vector', 'CVSS Vector', 'CVSS3 Base Score', 'CVSS3 Temporal Score', 'CVSS3 Temporal Vector', 'CVSS3 Vector', 'Host End', 'Host Start', 'NetBios', 'Plugin Family', 'Plugin ID', 'Port', 'Protocol', 'Risk', 'System Type', 'Vulnerability Priority Rating (VPR)', 'Vulnerability State', 'First Seen', 'Last Seen', 'Recast Reason'],axis=1, inplace=True)

#################################################
# Saving the results to a csv for review
#################################################

results.to_csv(r'results.csv', index = False)