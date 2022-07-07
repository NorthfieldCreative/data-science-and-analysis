
#########################################################
#                                                       #
#   This script loads exported vulnerability data from  #
#   Tenable, Tanium, and crowdstrike. It then creates   #
#   charts to visualize how many CVEs were discovered   #
#   from each tool in an attempt to determine which     #
#   discovers the greatest amount of CVEs               #
#                                                       #
#   Exporting the data first is of course a pre-req     #
#   before executing this                               #
#                                                       #
#########################################################

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import os.path


#########################################################
#   First we will open each CVE export to manage and    #
#   clean up all the data they contain, creating new    #
#   and consolidated dataframes for each respective     #
#   tool where each machine is listed with their CVEs   #
#########################################################


#########################################################
#                                                       #
#                                                       #
#           T   E   N   A   B   L   E                   #
#                                                       #
#                                                       #
#########################################################

#########################################################
# Open the export from tenable                          #
#########################################################
tenable = pd.read_csv('tenable.csv', low_memory=False)

#############################################################
# Because hosts with more than one cve are comma separated  #
# within the same row, we need to Separate all CVEs         #
# respecting their rows and maintaining other attributes    #
#############################################################
tenable["CVE"]=tenable["CVE"].str.split(',')
tenablewithseparatedcves=(tenable.explode("CVE").reset_index(drop=True))

#########################################################
# Dropping tenable columns that are not needed          #
#########################################################
tenablewithseparatedcves.drop(['Asset UUID', 'MAC Address', 'Name', 'CVSS', 'CVSS Base Score', 'CVSS Temporal Score', 'CVSS Temporal Vector', 'CVSS Vector', 'CVSS3 Base Score', 'CVSS3 Temporal Score', 'CVSS3 Temporal Vector', 'CVSS3 Vector', 'Description', 'Host End', 'Host Start', 'IP Address', 'NetBios', 'Plugin Family', 'Plugin ID', 'Plugin Output', 'Port', 'Protocol', 'Risk', 'See Also', 'Solution', 'Synopsis', 'System Type', 'Vulnerability Priority Rating (VPR)', 'Vulnerability State', 'Age', 'First Seen', 'Last Seen', 'Recast Reason'],axis=1, inplace=True)

#########################################################
# Renaming columns for easy reference                   #
#########################################################
tenablewithseparatedcves.rename(columns={'CVE': 'tenablecves', 'Host': 'tenablehostname', 'OS': 'tenableOSname'}, inplace=True)

#########################################################
# dropping machines exported from Tenable without       #
# a CVE from the table so the data can be parsed        #
#########################################################

tenablewithseparatedcves.dropna(subset=['tenablecves'], inplace=True)

#########################################################
#   Counting how many rows exist in the dataframe       #
#   This is the CVE count in the data                   #
#########################################################
tenablerowcount = len(tenablewithseparatedcves.index)

#########################################################
#   The tenable export was a little weird because the   #
#   FQDN and Host columns both contain hostname data,   #
#   however, the columns were not necessarily reliable  #
#   because blank rows exist. The FQDN column seemed    #
#   to be most accurate but also contained the blanks.  #
#   Where blanks exist, here we copy over the row data  #
#   from the Host column in an attempt to provide more  #
#   accurate reporting.                                 #
#########################################################
tenablewithseparatedcves["FQDN"].fillna(tenablewithseparatedcves["tenablehostname"], inplace=True)

#########################################################
#   Sorting by hostname. We do this to prevent          #
#   duplicates when we later create a concise list      #
#   of machines with their individual CVE counts        #
#########################################################
tenablewithseparatedcves.sort_values(by=['FQDN'], inplace=True)

#########################################################
#                                                       #
#   Creating a dataframe from where each machine gets   #
#   one row with a count of CVEs, referenced above      #
#                                                       #
#########################################################
if os.path.exists("tenablecves.csv"):
    print("tenablecves.csv already exists")
else:
    #####################################################
    #   Creating a new dataframe to store the list      #
    #   of machines with their CVE counts               #
    #####################################################
    tenablecves = pd.DataFrame(columns=['Hostname', 'cvecount'])
    row=["tenablehost", "tenablecve"]
    tenablecves.loc[len(tenablecves)] = row


    for i in tenablewithseparatedcves.FQDN:
        tenablehost = i
        tenablecve = tenablewithseparatedcves.FQDN.str.count(i).sum()

        if tenablecves['Hostname'].iloc[-1] == i:
            uselessvariable = 1
        else:
            row=[tenablehost, tenablecve]
            tenablecves.loc[len(tenablecves)] = row
            print(row)
    tenablecves.to_csv(r'tenablecves.csv', index = False)






#########################################################
#                                                       #
#                                                       #
#               T   A   N   I   U   M                   #
#                                                       #
#                                                       #
#########################################################

#########################################################
# Open the export from Tanium                           #
#########################################################
tanium = pd.read_csv('tanium.csv', low_memory=False)

#########################################################
# Dropping tanium columns that are not needed           #
#########################################################
tanium.drop(['Description', 'year', 'ip', 'number', 'cpe', 'vendor1', 'vendor2', 'date1', 'date2', 'based', 'os2'],axis=1, inplace=True)

#########################################################
# Renaming columns for easy reference                   #
#########################################################
tanium.rename(columns={'CVE': 'taniumcves', 'machine': 'taniumhostname', 'os': 'taniumosname'}, inplace=True)

#########################################################
#   Counting how many rows exist in the dataframe       #
#   This is the CVE count in the data                   #
#########################################################
taniumrowcount = len(tanium.index)

#########################################################
#   Sorting by hostname. We do this to prevent          #
#   duplicates when we later create a concise list      #
#   of machines with their individual CVE counts        #
#########################################################
tanium.sort_values(by=['taniumhostname'], inplace=True)

#########################################################
#                                                       #
#   Creating a dataframe from where each machine gets   #
#   one row with a count of CVEs, referenced above      #
#                                                       #
#########################################################
if os.path.exists("taniumcves.csv"):
    print("taniumcves.csv already exists")
else:
    #####################################################
    #   Creating a new dataframe to store the list      #
    #   of machines with their CVE counts               #
    #####################################################
    taniumcves = pd.DataFrame(columns=['Hostname', 'cvecount'])
    row=["taniumhost", "taniumcve"]
    taniumcves.loc[len(taniumcves)] = row


    for i in tanium.taniumhostname:
        taniumhost = i
        taniumcve = tanium.taniumhostname.str.count(i).sum()

        if taniumcves['Hostname'].iloc[-1] == i:
            uselessvariable = 1
        else:
            row=[taniumhost, taniumcve]
            taniumcves.loc[len(taniumcves)] = row
            print(row)
    taniumcves.to_csv(r'taniumcves.csv', index = False)











#########################################################
#                                                       #
#                                                       #
#       C   R   O   W   D   S   T   R   I   K   E       #
#                                                       #
#                                                       #
#########################################################

#########################################################
#   Open the data exported from Crowdstrike             #
#########################################################
crowdstrike = pd.read_csv('crowdstrike.csv', low_memory=False)

#########################################################
# Dropping crowdstrike columns that are not needed      #
#########################################################
crowdstrike.drop(['LocalIP', 'Exploit status label', 'Platform', 'HostType', 'MachineDomain', 'OU', 'SiteName', 'Product', 'CVE Description', 'Status', 'Severity', 'Created Date', 'Closed Date', 'Closed Dwell Time', 'Base Score', 'CVSS Version', 'Vector', 'Vendor Advisory', 'References', 'Recommended Remediations', 'Remediation Details', 'Remediation Links', 'Group Names', 'Tags', 'Host ID', 'Exploit status value', 'Vulnerable Product Versions', 'Closed Product Versions', 'RemediationLevel', 'ExPRT Rating'],axis=1, inplace=True)

#########################################################
# Renaming columns for easy reference                   #
#########################################################
crowdstrike.rename(columns={'Hostname': 'cshostname', 'OSVersion': 'csosversion', 'CVE ID': 'cscves'}, inplace=True)

#########################################################
#   Counting how many rows exist in the dataframe       #
#   This is the CVE count in the data                   #
#########################################################
crowdstrikerowcount = len(crowdstrike.index)

#########################################################
#   Sorting by hostname. We do this to prevent          #
#   duplicates when we later create a concise list      #
#   of machines with their individual CVE counts        #
#########################################################
crowdstrike.sort_values(by=['cshostname'], inplace=True)

#########################################################
#                                                       #
#   Creating a dataframe from where each machine gets   #
#   one row with a count of CVEs, referenced above      #
#                                                       #
#########################################################
if os.path.exists("cscves.csv"):
    print("cscves.csv already exists")
else:
    #####################################################
    #   Creating a new dataframe to store the list      #
    #   of machines with their CVE counts               #
    #####################################################
    cscves = pd.DataFrame(columns=['Hostname', 'cvecount'])
    #####################################################
    #   This is just temporary placeholder data so      #
    #   that machines can later be iterated and added   #
    #   to the list.    (prevents errors)               #
    #####################################################
    row=["cshost", "cscve"]
    cscves.loc[len(cscves)] = row

    #####################################################
    # Generating CVE counts by individual machine       #
    # realized by Crowdstrike                           #
    #####################################################
    for i in crowdstrike.cshostname:
        cshost = i
        cscve = crowdstrike.cshostname.str.count(i).sum()

        if cscves['Hostname'].iloc[-1] == i:
            uselessvariable = 1
        else:
            row=[cshost, cscve]
            cscves.loc[len(cscves)] = row
            print(row)
    cscves = cscves.iloc[1: , :]
    cscves.to_csv(r'cscves.csv', index = False)














#########################################################
#   Now we'll search for which machines discovered by   #
#   crowdstrike were also discovered by Tanium          #
#########################################################
tanlist = pd.read_csv('taniumcves.csv', low_memory=False)

#########################################################
#   First we'll compare Crowdstrike to Tanium           #
#########################################################
cslist = pd.read_csv('cscves.csv', low_memory=False) 
searchfor = cslist['Hostname']

#########################################################
# comparing the list and assigning it to another        #
# variable for further processing                       #
#########################################################
results = tanlist[tanlist['Hostname'].str.contains('|'.join(searchfor))]



#################################################
# Saving the results to a csv for review
#################################################
results.to_csv(r'crowdstrikecvesfoundintaniumresults.csv', index = False)





#########################################################
#   Now we'll search for which machines discovered by   #
#   Tenable were also discovered by Tanium              #
#########################################################
tanlist = pd.read_csv('taniumcves.csv', low_memory=False)

#########################################################
#   First we'll compare Tenable to Tanium               #
#########################################################
tenlist = pd.read_csv('tenablecves.csv', low_memory=False) 
searchfor = tenlist['Hostname']

#########################################################
# comparing the list and assigning it to another        #
# variable for further processing                       #
#########################################################
results = tanlist[tanlist['Hostname'].str.contains('|'.join(searchfor))]

#################################################
# Saving the results to a csv for review
#################################################
results.to_csv(r'tenablecvesfoundintaniumresults.csv', index = False)

















#########################################################
#########################################################
#                                                       #
#    *      R   E   P   O   R   T   I   N   G       *   #
#                                                       #
#########################################################
#########################################################

#########################################################
#   This chart shows all cves discovered from all       #
#   possible sources                                    #
#########################################################

#########################################################
#   These are just the labels loaded into a list for    #
#   reference in the chart                              #
#########################################################
sources = ['CVEs from Tenable', 'CVEs from Tanium', 'CVEs from Crowdstrike']

#########################################################
#   These are the counts of CVEs realized from each     #
#   tool to be displayed in the chart                   #
#########################################################
values = [tenablerowcount, taniumrowcount, crowdstrikerowcount]

fig = plt.figure(figsize = (10, 5))
######################################################### 
#   creating the bar plot                               #
#########################################################
plt.bar(sources, values, color ='maroon',
        width = 0.4)
#########################################################
#   These are the labels for the actual chart           #
#########################################################
plt.xlabel("Tools")
plt.ylabel("Count of CVEs discovered")
plt.title("All CVEs discovered by tools from available resources")
#plt.show()

plt.savefig("everything.png")
plt.close()











#########################################################
#   This chart shows and comparescves discovered from   #
#   each tool using Tanium as the master reference for  #
#   comparison. All machines will be iterated through   #
#########################################################

#########################################################
#   First we will load our cleaned and prepared         #
#   data sources                                        #
#########################################################
cleanedtaniumdata = pd.read_csv('taniumcves.csv', low_memory=False)
cleanedtenabledata = pd.read_csv('tenablecvesfoundintaniumresults.csv', low_memory=False)
cleanedcrowdstrikedata = pd.read_csv('crowdstrikecvesfoundintaniumresults.csv', low_memory=False)



cleancscount = cleanedcrowdstrikedata['cvecount'].sum()
cleantancount = cleanedtaniumdata['cvecount'].sum()
cleantencount = cleanedtenabledata['cvecount'].sum()

print("crowdstrike cves found: ", cleancscount)
print("Tanium cves found: ", cleantancount)
print("Tenable cves found: ", cleantencount)


#########################################################
#   These are just the labels loaded into a list for    #
#   reference in the chart                              #
#########################################################
sources = ['CVEs from Tenable', 'CVEs from Tanium', 'CVEs from Crowdstrike']

#########################################################
#   These are the counts of CVEs realized from each     #
#   tool to be displayed in the chart                   #
#########################################################
values = [cleantencount, cleantancount, cleancscount]

fig = plt.figure(figsize = (10, 5))
######################################################### 
#   creating the bar plot                               #
#########################################################
plt.bar(sources, values, color ='maroon',
        width = 0.4)
#########################################################
#   These are the labels for the actual chart           #
#########################################################
plt.xlabel("Tools")
plt.ylabel("Count of CVEs discovered")
plt.title("CVEs discovery comparison based on current (7/5/22) Tanium deployment")
#plt.show()

plt.savefig("accuratecomparison.png")
plt.close()






for i in cleanedtaniumdata.Hostname:
    
  
    tancvecount = cleanedtaniumdata.loc[cleanedtaniumdata['Hostname'] == i, 'cvecount'].iloc[0]
    try:
        cscvecount = cleanedcrowdstrikedata.loc[cleanedcrowdstrikedata['Hostname'] == i, 'cvecount'].iloc[0]
    except:
        cscvecount = 0
    try:
        tencvecount = cleanedtenabledata.loc[cleanedtenabledata['Hostname'] == i, 'cvecount'].iloc[0]
    except:
        tencvecount = 0
    #print(i, " ")

    # set width of bar
    barWidth = 0.2
    fig = plt.subplots(figsize =(20, 8))
 
    # set height of bar
    TAN = [tancvecount]
    CRWD = [cscvecount]
    TEN = [tencvecount]
 
    # Set position of bar on X axis
    br1 = np.arange(len(TAN))
    br2 = [x + barWidth for x in br1]
    br3 = [x + barWidth for x in br2]
 
    # Make the plot
    plt.bar(br1, TAN, color ='r', width = barWidth,
            edgecolor ='grey', label ='Tanium')
    plt.bar(br2, CRWD, color ='g', width = barWidth,
            edgecolor ='grey', label ='Crowdstrike')
    plt.bar(br3, TEN, color ='b', width = barWidth,
            edgecolor ='grey', label ='Tenable')
 
    # Adding Xticks
    plt.xlabel('Machines', fontweight ='bold', fontsize = 15)
    plt.ylabel('CVEs Discovered', fontweight ='bold', fontsize = 15)
    plt.xticks([r + barWidth for r in range(len(TAN))],
            [i])
 

    plt.legend()
    
    filename = i + ".png"
    print(filename)
    plt.savefig(filename)
    
    #plt.show()
    plt.close()
    
    


exit()