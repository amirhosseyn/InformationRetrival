import json
import os

# a = json.load(open('news.json','r'))
# print(a[0]['meta_tags'][0])
urls = json.load(open(os.path.dirname(os.path.realpath(__file__)) + '\\news1.json', "r"))

def query(docids):

    return [urls[i] for i in docids]