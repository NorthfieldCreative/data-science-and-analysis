import numpy as np
import pandas as pd
import matplotlib.pyplot as plt


authdomains = pd.read_csv('freemail.csv', low_memory=False) 



df1 = pd.DataFrame({'domains': ['intelisecure', 'hotmail', 'gmail', 'user@gmail.com']})


extdomains = pd.read_csv('extdomains.csv', low_memory=False)

###########
# Because messages with more than one recipient are comma separated within the same 
# row, we need to Separate all recipients into a new column
###########
#s = extdomains['domains'].str.split(',').apply(pd.Series, 1).stack()
s = extdomains['domains'].str.split(',').apply(pd.Series, 1).stack()
    #name that new column "all recipients")
s.name = 'All Recipients'


#loading TCH pre-authorized domains into a variable for easier handling

searchfor = authdomains['freemaildomains']
#searchfor = df1['domains']

#creates a new variable "authdomainsfound". Searches for pre authorized domains in the list
#of all recipients that was created above. All pre authorized domains found within the list
#of all recipients are stored within "authdomains found
authdomainsfound = s[s.str.contains('|'.join(searchfor))]

df3 = pd.DataFrame(data=authdomainsfound)
df3.to_csv(r'data.csv', index = False)











##########################################################
#s = extdomains['domains'].apply(pd.Series, 1).stack()
    #name that new column "all recipients")
#s.name = 'All Recipients'
#
#searchfor = authdomains['freemaildomains']
#authdomainsfound2 = s[s.str.contains('|'.join(searchfor))]
#authdomainsfound2 = authdomainsfound2.str.extract("_(.*)#ext#")
#df4 = pd.DataFrame(data=authdomainsfound2)
#
#
#
#frames = [df3,df4]
#result = pd.concat(frames)
#result.to_csv(r'alldata.csv', index = False)
##########################################################



###################
#endpoint = endpoint.fillna({'Recipient(s)': 'Unknown'})
#eprsearch = endpoint['Recipient(s)']
#eprsearch.name = 'endpoint recipients search'
#EPauthdomainsfound = eprsearch[eprsearch.str.contains('|'.join(searchfor))]
######################














#df = pd.DataFrame({'col1': ['a', 'b', 'c', 'b'],
#                   'col2': ['a123','b456','d789', 'a']})
#df['contained'] = df.apply(lambda x: x.col1 in x.col2, axis=1)
#df.to_csv(r'data.csv', index = False)






#df1 = pd.DataFrame({'col': ['a', 'b', 'c', 'xm']})
#df2 = pd.DataFrame({'col': ['a123','b456','xl789', 'a']})
#print(np.where(df2.col.isin(df1.col), df1.col, 'NO_MATCH'))
