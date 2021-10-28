from collections import OrderedDict, defaultdict
import pandas as pd 
import numpy as np 
import json


def remove_a_key(d, remove_key):
    if isinstance(d, dict):
        for key in list(d.keys()):
            if key == remove_key:
                del d[key]
            else:
                remove_a_key(d[key], remove_key)


js1 = pd.read_json('scrapy1.json')
js2  = pd.read_json('scrapy2.json')


df_inner = pd.merge(js1, js2, how='outer', left_on=[
    'pokemon_numero', 'pokemon_nome'], right_on=['pokemon_numero','pokemon_nome' ])

df_inner = df_inner.dropna()
df_inner = df_inner.to_dict('records')

new_dict = {}
for item in df_inner:
   name = item["pokemon_numero"]
   new_dict[name] = item


for x in list(new_dict):
    for y in list(new_dict[x]):
        if x is not None:
            new_dict[x]['Dano'] =dict (zip (new_dict[x]["pokemon_tipo_dano"],new_dict[x]["pokemon_dano"]))

remove_a_key(new_dict,"pokemon_tipo_dano")
remove_a_key(new_dict,"pokemon_dano")
remove_a_key(new_dict,"pokemon_numero")

#pega apenas a evolução
for x in new_dict:
    for y in new_dict[x]:
        lista = new_dict[x]['pokemon_evolucao']
        if (new_dict[x]['pokemon_nome'] in lista):
            index = lista.index(new_dict[x]['pokemon_nome'])
            new_dict[x]['pokemon_evolucao']=lista[index+1:]


#remover duplicados
for x in new_dict:
    for y in new_dict[x]:
      listaE = [] 
      [listaE.append(x) for x in new_dict[x]['pokemon_evolucao'] if x not in listaE]  
      new_dict[x]['pokemon_evolucao'] =listaE 

df = pd.DataFrame.from_dict(new_dict, orient="index")
df.to_csv('data.csv')



