
# coding: utf-8

# In[164]:


import pandas as pd
import numpy as np
from operator import itemgetter
from math import hypot
import matplotlib.pyplot as plt
get_ipython().magic(u'matplotlib inline')

## iz simulation atributa izvuci vrijednosti
x_GW = 240
y_GW = 240
df = pd.read_csv('adresa.csv') #, usecols = ["run","attrname" "name", "value", "type"])
Df = df[(df.name == 'address') | (df.name == 'numberOfReceivedPacketsPerNode') | (df.name == 'sentPackets') | (df.name == 'addressNode') |
       (df.name == 'positionX') | (df.name == 'positionY')]
dfAddressNode = df[(df.name == 'addressNode')]
dfAddressNode.rename(columns={'value': 'nodeAddress'}, inplace=True)


dfSentPackets = df[df.name == 'sentPackets']
dfSentPackets.rename(columns={'value': 'sentPackets'}, inplace=True)

dfPositionX = df[(df.name == 'positionX')]
dfPositionY = df[(df.name == 'positionY')]
#dfPosition.rename(columns={'value': 'positionX'}, inplace=True)

dfNumOfRecPkPerNode = df[df.name == 'numberOfReceivedPacketsPerNode']
dfNumOfRecPkPerNode.rename(columns={'value': 'numOfRecPkPerNode'}, inplace=True)

dfKnownNodes = df[df.name == 'address']
dfKnownNodes.rename(columns={'value': 'nodeAddress'}, inplace=True)

udaljenost = []
runX = []
x = []

moduleX = []
for index, row in dfPositionX.iterrows():
    x.append(row.value)
    runX.append(row.run)
    moduleX.append(row.module)
dX = pd.DataFrame({'run': runX, 'positionX': x, 'module': moduleX})

runY = []
moduleY = []
y = []
for index, row in dfPositionY.iterrows():
    runY.append(row.run)
    moduleY.append(row.module)
    y.append(row.value)

dY = pd.DataFrame({'run': runY, 'positionY': y, 'module': moduleY})
dfDistance = pd.merge(dX, dY[['module', 'positionY']], on='module')
#dfMerge2 = pd.merge(dfMerge, dfNumOfRecPkPerNodeByGWSum[['recPkByGw', 'nodeAddress']], on='nodeAddress')
#dfDistance = pd.DataFrame({'run': run, 'positionX': x, 'positionY': y, 'module': module})

    #dist = hypot(x_GW-x, y_GW-y)
    #dist = sqrt( (x_GW - x)**2 + (y_GW - y)**2 )
    #udaljenost.append(dist)

print(dX)
print(dY)
print(dfDistance)
    


receivedPk = []
runRec = []
for index, row in dfNumOfRecPkPerNode.iterrows():
    receivedPk.append(row.numOfRecPkPerNode)
    runRec.append(row.run)
    
knownNodes = []
for index, row in dfKnownNodes.iterrows():
    knownNodes.append(row.nodeAddress)

dfNumOfRecPkPerNodeByGW = pd.DataFrame({'run': runRec, 'recPkByGw': receivedPk, 'nodeAddress': knownNodes})
print(dfNumOfRecPkPerNodeByGW)
dfNumOfRecPkPerNodeByGWSum = dfNumOfRecPkPerNodeByGW.groupby(['nodeAddress'],as_index = False).sum()
#dfNumOfRecPkPerNodeByGWSum['run'] = run
print(dfNumOfRecPkPerNodeByGWSum)
#sentPacketsByNodesTotal = sentPacketsDf.groupby(['run']).sum()
#print(dfNumOfRecPkPerNodeByGW)

number = []
#dfAddressNode = dfAddressNode.assign(qname)
for index, row in dfAddressNode.iterrows():
    module = row.module
    split = module.split('.')
    #print(split)
    strip = split[1].strip(']')
    strip = strip.split('[')
    number.append(int(strip[1]))
dfAddressNode['nodeId'] = number
numbers = []

dfSentPackets = pd.merge(dfSentPackets, dfDistance[['positionX','positionY', 'module']], on = 'module')
#print(dfSentPackets)
for index, row in dfSentPackets.iterrows():
    module = row.module
    split = module.split('.')
    #print(split)
    strip = split[1].strip(']')
    strip = strip.split('[')
    #print(strip[1])
    numbers.append(int(strip[1]))
dfSentPackets['nodeId'] = numbers
#print(dfSentPackets)

dfMerge = pd.merge(dfAddressNode[['run', 'nodeId', 'nodeAddress']], dfSentPackets[['run','positionX','positionY','sentPackets','nodeId']], on = 'nodeId')
#print(dfMerge)
dfMerge2 = pd.merge(dfMerge, dfNumOfRecPkPerNodeByGWSum[['recPkByGw', 'nodeAddress']], on='nodeAddress')
#dfMerge2.fillna('0', inplace=True)
#print(dfMerge2)

udaljenost = []
dist = 0
for index, row in dfMerge2.iterrows():
    dist = hypot(x_GW-row.positionX, y_GW-row.positionY)
    
    #dist = sqrt( (x_GW - x)**2 + (y_GW - y)**2 )
    udaljenost.append(dist)
    
dfMerge2['distance'] = udaljenost
#print(dfMerge2)

dfSort = dfMerge2.sort_values(['distance']).reset_index(drop=True)
print(dfSort)

tmp = []
xAxis = []
yAxis = []
for index, row in dfSort.iterrows():
    #tmp.append([row.distance, (row.recPkByGw/row.sentPackets)])
    xAxis.append(row.distance)
    yAxis.append(row.recPkByGw/row.sentPackets)

dataframe = pd.DataFrame({'distance': xAxis, 'deliveryRatio': yAxis})    
dataframe.plot.scatter(x='distance', y='deliveryRatio')
#df.plot.scatter(x='a', y='b');
#plt.plot.kde(xAxis, yAxis)
#plt.plot(style='.--', markevery=1)
plt.xlabel('udaljenost od gatewaya')
plt.ylabel('deliveryRatio')
plt.show

    
    

#what = pd.merge(names, info, how="outer")
#what.fillna('unknown', inplace=True)

