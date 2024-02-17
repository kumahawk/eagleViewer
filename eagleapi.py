import requests
import re

def checkresponse(result):
    if result.status_code != 200:
        result.raise_for_status()
    json = result.json()
    if json['status'] != 'success':
        raise Exception(json)
    return json

def getimages():
    imgs = requests.request('get', 'http://localhost:41595/api/item/list?limit=10')
    imgs = checkresponse(imgs)
    return imgs['data']

def getlibraries():
    libs = requests.request('get', 'http://localhost:41595/api/library/history')
    libs = checkresponse(libs)
    return libs['data']

if __name__ == "__main__":
    imgs = getimages()
