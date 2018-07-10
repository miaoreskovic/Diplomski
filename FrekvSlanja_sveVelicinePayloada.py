
# coding: utf-8

# In[40]:


import pandas as pd
import numpy as np
from operator import itemgetter
import matplotlib.pyplot as plt
get_ipython().magic(u'matplotlib inline')
df = pd.read_csv('sim5_SF12v2.csv', usecols = ["run","attrname", "name", "value", "type", "attrvalue"]) #, usecols = ["run","attrname" "name", "value", "type"])

sentPacketsDf = df[(df.name == 'sentPackets')]

#broj cvorova u pojedinom run-u
sentPacketsByNumberOfNodes = sentPacketsDf.groupby(['run']).size().reset_index(name='brojCvorova')
#print(sentPacketsByNumberOfNodes)

#ukupan broj poslanih paketa po pojedinom run-u
sentPacketsByNodesTotal = sentPacketsDf.groupby(['run']).sum()
#print(sentPacketsByNodesTotal['value'])
sentPacketsByNodesTotal.rename(columns={'value': 'brojPoslanihPaketa'}, inplace=True)

#broj ponavaljanja po pojedinom run-u
repetition = df[(df.attrname == 'repetition')]
repetition.rename(columns={'attrvalue': 'repetition'}, inplace=True)

#frekvencija slanja paketa po pojedinom run-u
payload = df[(df.attrname) == 'iterationvars']
#payload.rename(columns={'attrvalue': 'payload'}, inplace=True)

#broj primljeni paketa na GW po pojedinom run-u
packetReceivedDf = df[(df.name == 'LoRa_GWPacketReceived:count') & (df.type == 'scalar')]
#print(packetReceivedDf)
packetReceivedDf.rename(columns={'value': 'brojPrimPkGW'}, inplace=True)
#packetReceivedByGateway = packetReceivedDf.groupby(['run'], as_index = False )
#packetReceivedByGatewayGroupedBy = packetReceivedDf.groupby(['run'])

run = []
payloadPacket = []
frekvSlanja = []
frekvSlanjaTmp = []
splitaneVarIteracije = []
for index, row in payload.iterrows():
    run.append(row.run)
    payload_sendingFreq = row.attrvalue # varijable iteracije
    splitaneVarIteracije = payload_sendingFreq.split('=')
    print(splitaneVarIteracije[7])
    payloadPacket.append(int(splitaneVarIteracije[7]))
    frekvSlanjaTmp = splitaneVarIteracije[3].split(',')
    frekvSlanja.append(int(frekvSlanjaTmp[0].strip('(min')))
    #print(frekvSlanja)
    
print(payloadPacket)
print(frekvSlanja)
#novi dataframe koji ce sadrzavati stupce run i frekvSlanja
df_payload = pd.DataFrame({'run': run, 'payload': payloadPacket})
df_sendingFreq = pd.DataFrame({'run': run, 'frekvSlanja': frekvSlanja})
#print("\n\n Sending freq\n")
#print(df_payload)
    
    
df = pd.merge(sentPacketsByNodesTotal, repetition[['run','repetition']], on='run')
df2 = pd.merge(df, sentPacketsByNumberOfNodes, on='run')
df3 = pd.merge(df2, df_sendingFreq, on='run')
df4 = pd.merge(df3, df_payload, on='run')
df5 = pd.merge(df4, packetReceivedDf[['run','brojPrimPkGW']], on='run')
print(df5)

dfSort = df5.sort_values(['frekvSlanja','payload', 'repetition']).reset_index(drop=True)
print("Sortirani dataframe po frekvslanja a zatim po payloada, potom po repetitionu\n")
print(dfSort)

tmp = []
curFrekvSlanja = dfSort.iloc[0]['frekvSlanja']
curPayload = dfSort.iloc[0]['payload']
sumDeliveryRatio = 0.0
repetition = 0

for index, row in dfSort.iterrows():
    if((row.frekvSlanja == curFrekvSlanja) & (row.payload == curPayload)):
        if(row.brojPrimPkGW != 0):

            sumDeliveryRatio = sumDeliveryRatio + (row.brojPrimPkGW/row.brojPoslanihPaketa)
            repetition = repetition + 1
        else:
            sumDeliveryRatio = sumDeliveryRatio + 0

    
    else:
        if(sumDeliveryRatio != 0.0):
            tmp.append([curFrekvSlanja, (sumDeliveryRatio/repetition)*100, curPayload])
        else:
            tmp.append([curFrekvSlanja, 0.0, curPayload])
        sumDeliveryRatio = 0
        repetition = 0
        curFrekvSlanja = row.frekvSlanja
        curBrojCvorova = row.brojCvorova
        curPayload = row.payload
        if (row.brojPrimPkGW != 0):
            sumDeliveryRatio = sumDeliveryRatio + (row.brojPrimPkGW/row.brojPoslanihPaketa)
            repetition = repetition + 1

            
if(sumDeliveryRatio != 0.0):
    tmp.append([curFrekvSlanja, (sumDeliveryRatio/repetition)*100, curPayload])
else:
    tmp.append([curFrekvSlanja, 0.0, curPayload])
    
tmp.sort(key=lambda x: x[0])

yAxisPayload5 = []
yAxisPayload10 = []
yAxisPayload20 = []

xAxis = []
payload = 0

for item in tmp:
    if item[0] not in xAxis:
        print("item is in array already")
        xAxis.append(item[0])
    payload = item[2]
    #brojCV = item[2]
    if (payload == 5):
        yAxisPayload5.append((item[1]));
    elif (payload == 10):
        yAxisPayload10.append((item[1]));
    elif (payload == 20):
        yAxisPayload20.append((item[1]));
    else:
        print("Delivery ratio se zeli spremiti u nepostojece polje!")
print(yAxisPayload5)
print(yAxisPayload10)
print(yAxisPayload20)

plt.plot(xAxis, yAxisPayload5, label = 'teret = 5')
plt.plot(xAxis, yAxisPayload10, label = 'teret = 10')
plt.plot(xAxis, yAxisPayload20, label = 'teret = 20')

plt.legend()
plt.xlabel(u"frekvencija slanja paketa (min)")
plt.ylabel(u"uspješnost isporuke paketa (%)")
plt.title(u"BW = 125 kHz, CR = 4/8, SF = 12, n = 300")
plt.ylim(ymax = 100, ymin = 0)
plt.rcParams['axes.titlepad'] = 20 
plt.rcParams['figure.figsize'] = [15,20]

plt.savefig('sim5_SF12v2-100dpi.svg', dpi = 100)
plt.savefig('sim5_SF12v2-100dpi.png', dpi = 100)


plt.savefig('sim5_SF12v2-300dpi.svg', dpi = 300)
plt.savefig('sim5_SF12v2-300dpi.png', dpi = 300)


plt.show()

