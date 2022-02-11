import xml.etree.ElementTree as ET
import pandas as pd
import os
import matplotlib.pyplot as plt


################################################
####    This first parses the XML and outputs 
####    to a comma separated format for easier 
####    handling
################################################

tree = ET.parse("incidents.xml")
root = tree.getroot()
get_range = lambda col: range(len(col))
l = [{r[i].tag:r[i].text for i in get_range(r)} for r in root]
df = pd.DataFrame.from_dict(l)
df.to_csv('convertedxml.csv')



#####Opens up the parsed XML for handling
xmlconverted = pd.read_csv('convertedxml.csv', low_memory=False)

#####opens up the raw CSV file for handling
csvraw = pd.read_csv('incidents.csv', low_memory=False)

#####sorts the incidents in the csv file by incident ID. This will later be used to match the XML data
csvraw.sort_values(by='ID', inplace=True, ascending=True)

##### to make life easier, saving the sorted CSV file to open back up again later
csvraw.to_csv(r'sorted.csv', index = False)




##### extracting just the columns we want into a new variable
userjustifications = xmlconverted[['{http://www.vontu.com/enforce/export/incident/schema}userJustification', '{http://www.vontu.com/enforce/export/incident/schema}incidentId']]

##### sorting by the incident ID. Again, this will help line things up when joining the data.
userjustifications.sort_values(by='{http://www.vontu.com/enforce/export/incident/schema}incidentId', inplace=True, ascending=True)

##### saving the sorted justifications out to a file
userjustifications.to_csv(r'userjustifications.csv', index = False)



sortedcolumns = pd.read_csv('sorted.csv', low_memory=False)



##### remember when the sorted CSV data was saved to a file? Now we're opening it back up for use
sortedjustify = pd.read_csv('userjustifications.csv', low_memory=False)

##### Assigning all of the incident IDs from the XML file to a variable
sortedjustifyids = sortedjustify["{http://www.vontu.com/enforce/export/incident/schema}incidentId"]

##### Assigning all of the user justifications from the XML file to a variable
sortedjustifyjustifications = sortedjustify["{http://www.vontu.com/enforce/export/incident/schema}userJustification"]



##### Adding the incident IDs from the Original XML file to the CSV document. 
##### By doing this, both ID columns should have the same ID. If they don't,
##### that means something has gon wrong somewhere
sortedcolumns = sortedcolumns.join(sortedjustifyids)

##### Adding the justifications to the CSV data
sortedcolumns = sortedcolumns.join(sortedjustifyjustifications)




##### Renaming the columns from the XML data to something a little more friendly
sortedcolumns.rename(columns = {'{http://www.vontu.com/enforce/export/incident/schema}userJustification':'Justifications'}, inplace = True)
sortedcolumns.rename(columns = {'{http://www.vontu.com/enforce/export/incident/schema}incidentId':'XML_ID'}, inplace = True)


##### Finally, outputing the consolidated data to a CSV file.
sortedcolumns.to_csv(r'consolidatedjustifications.csv', index = False)




####################################
####################################
#                                  #
#            CLEANUP               #
#                                  #
#                                  #
####################################
####################################
os.remove("convertedxml.csv")
os.remove("sorted.csv")
os.remove("userjustifications.csv")
os.remove("incidents.csv")
os.remove("incidents.xml")






##########################################
##  making the charts starting with a count
##  of all justifications
##########################################
alldata = pd.read_csv('consolidatedjustifications.csv', low_memory=False)

ax = alldata['Justifications'].value_counts(dropna=True).plot(kind='barh')
ax.set_title("Count of all Justifications", fontsize=12)
for i in ax.patches:
    # get_width pulls left or right; get_y pushes up or down
    ax.text(i.get_width()+.1, i.get_y()+.31, \
            str(round((i.get_width()), 2)), fontsize=12, color='dimgrey')
plt.tight_layout()
plt.show()





###########################################
#############
#############   policies
#############
##############################################

ax = alldata.groupby('Policy').agg('Justifications').value_counts(dropna=True).plot(kind='barh')
ax.set_title("Justifications by all Policies", fontsize=12)
for i in ax.patches:
    # get_width pulls left or right; get_y pushes up or down
    ax.text(i.get_width()+.1, i.get_y()+.31, \
            str(round((i.get_width()), 2)), fontsize=12, color='dimgrey')

plt.tight_layout()
plt.show()





###########################################
#############
#############   Users
#############
##############################################




ax = alldata.groupby(['User']).Justifications.value_counts().nlargest(10).plot(kind='barh')


ax.set_title("Top 10 Justifications by all Users", fontsize=12)
for i in ax.patches:
    # get_width pulls left or right; get_y pushes up or down
    ax.text(i.get_width()+.1, i.get_y()+.31, \
            str(round((i.get_width()), 2)), fontsize=12, color='dimgrey')

plt.tight_layout()
plt.show()

