import os, json
import pandas as pd
from pprint import pprint

'''
#formato do dataset
id

'''


rawData = '../data/bicicletar/estacoes.json'
dataset = pd.DataFrame(columns=['id','stationName','lat','lon','program','adress','neighborhood'])
dataset.loc[0] = [1,'test',123,321,'bicicletar','rua cariri','centro']
i = 0
with open(rawData) as rawFile:
	data = json.load(rawFile)
	for station in data['network']['stations']:
		if ('Minibicicletar' in station['name']):
			stationName = station['name'][0:-17]
			program = 'Minibicicletar'
		else:
			stationName = station['name']
			program = 'Bicicletar'
		dataset.loc[i] = [i+1,stationName,station['latitude'],station['longitude'],program,station['extra']['description'],'TODO']
		#pprint(station)
		i+=1
	
dataset.to_csv('../data/bicicletar/estacoesCompleto.csv')
print(dataset)
	
   

