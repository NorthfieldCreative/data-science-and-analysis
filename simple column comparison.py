import pandas as pd


### open from a text file
ipsfromssdomainsfile = open('ssdomainips.txt', 'r')
ipsfromssfile = open('ssips.txt', 'r')
ipsfromextscanfile = open('extponurancescanips.txt', 'r')
ipsfromssdomainslist = []
ssipslist = []
extipslist = []
for i in ipsfromssdomainsfile.readlines():
    i = i.rstrip()
    ipsfromssdomainslist.append(i)

for i in ipsfromssfile.readlines():
    i = i.rstrip()
    ssipslist.append(i)

for i in ipsfromextscanfile.readlines():
    i = i.rstrip()
    extipslist.append(i)


allssips = ssipslist + ipsfromssdomainslist
df = pd.DataFrame()
df2 = pd.DataFrame()
results = pd.DataFrame()
df['allssips'] = allssips
df2['extips'] = extipslist


#results= currentdf[currentdf[[getmonth.getmonth(rawmonth)]].astype(str).sum(axis = 1).isin(tempdf[[i]].astype(str).sum(axis = 1))]

#results= df[df[['allssips']].astype(str).sum(axis = 1).isin(df2[['extips']].astype(str).sum(axis = 1))]
#df2=df[df['allssips'].isin(['extips'])]
#print(results)

'''
t1 = ['13f','1','2','3','4','5']
t2 = ['4','5','6','7','8','9','13f']
#t2 = ['4','5','6','7','8','a']
dft1 = pd.DataFrame()
dft2 = pd.DataFrame()
dft1['dft1'] = t1
dft2['dft2'] = t2
results= dft1[dft1['dft1'].isin(dft2['dft2'])]
'''
#results= df[df['allssips'].isin(df2['extips'])]
#results= df[df["allssips"].str.contains("|".join(extipslist))]
#results= df2[df2["extips"].str.contains("|".join(allssips))]
rawresults = set(extipslist) & set(allssips)
listresults = list(rawresults)
results['results']=listresults
#print(results)
#print(len(results))
#print(type(rawresults))
print(results)