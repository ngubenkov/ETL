import collections
import os
import pprint


s = "http://newsapi.org/v2/everything?q=RUSSIA&from={DATA_DATE}&to={DATA_DATE}&sortBy=popularity&apiKey={TOKEN}"

os.environ['DATA_DATE'] = '2020-10-01'
os.environ['TEST'] = 'TEST'

#for k, v in os.environ.items(): print(f'{k}={v}')



d =  collections.defaultdict(str)
d.update(os.environ)
pprint.pprint(d)



