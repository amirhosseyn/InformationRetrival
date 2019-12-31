import json
import os

urls = json.load(open(os.path.dirname(os.path.realpath(__file__)) + '\\news.json', "r"))
List2={}
for i in range(100):
   List2[i]=urls[i]
print(List2)
