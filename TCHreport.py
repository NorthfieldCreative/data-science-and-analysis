import pandas as pd
#opens up our source files for processing
network = pd.read_csv('Network.csv', low_memory=False)
endpoint = pd.read_csv('endpoint.csv', low_memory=False)
#this is a list of the preauthorized domains as provided by TCH
authdomains = pd.read_csv('authdomains.csv', low_memory=False) 


#####Creates a new column to indicate the source of the data once it has all been combined
network['Side'] = "Network"
endpoint['Side'] = "Endpoint"


#########
# Creating a new column for just the month and year. First the sent column is looked at
# and evaluated, and then the month and year are extracted and put into a new 
# column named month
##########

network['Sent'] = pd.to_datetime(network['Sent'])
network['month'] = network['Sent'].dt.strftime('%b-%Y')
monthforfile = network.iloc[0,35]
#timestamp = network.iloc[0,3]






############
# just like we did for the network side, making a new column for month
#############
endpoint['Occurred On'] = pd.to_datetime(endpoint['Occurred On'])
endpoint['month'] = endpoint['Occurred On'].dt.strftime('%b-%Y')



###########
# Because messages with more than one recipient are comma separated within the same 
# row, we need to Separate all recipients into a new column
###########
s = network['Recipient(s)'].str.split(',').apply(pd.Series, 1).stack()
    #name that new column "all recipients")
s.name = 'All Recipients'


#loading TCH pre-authorized domains into a variable for easier handling
searchfor = authdomains['Suggested domains']


#creates a new variable "authdomainsfound". Searches for pre authorized domains in the list
#of all recipients that was created above. All pre authorized domains found within the list
#of all recipients are stored within "authdomains found
authdomainsfound = s[s.str.contains('|'.join(searchfor))]

endpoint = endpoint.fillna({'Recipient(s)': 'Unknown'})
eprsearch = endpoint['Recipient(s)']
eprsearch.name = 'endpoint recipients search'
EPauthdomainsfound = eprsearch[eprsearch.str.contains('|'.join(searchfor))]




#removing usernames from recipients found in the data that belong to authorized domains
authdomainsfo und = authdomainsfound.str.extract("@(.*)")


#Naming the column with the extracted domains
authdomainsfound.columns = ['Authorized Domains Found in Network Recipients']

#creates dataframes from the data to be concatenated for output
df2 = pd.DataFrame(data=s)
df3 = pd.DataFrame(data=authdomainsfound)
df4 = pd.DataFrame(data=EPauthdomainsfound)

df4.columns = ['Authorized Domains Found in Endpoint Recipients']


#concatenating the dataframes, and creating a new variable (result) to hold the concatenation
#concatenating the dataframes, and creating a new variable (result) to hold the concatenation
frames = [network, endpoint, df2, df3, df4]
result = pd.concat(frames)

#saving the data
result.to_csv(r'TCH ' + monthforfile + ' clean data.csv', index = False)





#print(df3.head)
#print(pd.__version__)
