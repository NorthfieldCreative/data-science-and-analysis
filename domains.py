import pandas as pd, tldextract
from pandas import DataFrame





#df1 = pd.read_csv('ep2.csv', low_memory=False)

df = pd.read_csv('ep2.csv', low_memory=False)

'''
rawdata['rawDomain'] = rawdata['recipients'].apply(lambda url: tldextract.extract(url).domain)
raw.to_csv('withdomains.csv')
'''



#Sdf1 = df1['url']


#print(df1)
#df1.to_csv('ep4.csv')






#df = pd.DataFrame([{'url':'https://google.com'}]*12)
#df = pd.DataFrame(df1)
#df = pd.DataFrame(df['url'])
df['Domain'] = df['url'].apply(lambda url: tldextract.extract(url).domain)
print(df)

df.to_csv('ep4.csv')

'''
listed = tldextract.extract(rawdata['recipients'][4])
dom_name = listed.domain
print(dom_name)
'''