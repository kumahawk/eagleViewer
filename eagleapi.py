import requests
import json
import os.path

MAXMETRIC = 256

def checkresponse(result):
    if result.status_code != 200:
        result.raise_for_status()
    json = result.json()
    if json['status'] != 'success':
        raise Exception(json)
    return json

def _getimages(n = 10):
    imgs = requests.request('get', f'http://localhost:41595/api/item/list?limit={n}')
    imgs = checkresponse(imgs)
    return imgs['data']

def _getimageinfo(id):
    imgs = requests.request('get', f'http://localhost:41595/api/item/info?id={id}')
    imgs = checkresponse(imgs)
    return imgs['data']

def _getlibraries():
    libs = requests.request('get', 'http://localhost:41595/api/library/history')
    libs = checkresponse(libs)
    return libs['data']

def _refreshthumbnail(id):
    data = {"id":id}
    thumbs = requests.request('post', 'http://localhost:41595/api/item/refreshThumbnail', data=json.dumps(data))
    checkresponse(thumbs)

def _getthumbnail(id):
    thumbs = requests.request('get', f'http://localhost:41595/api/item/thumbnail?id={id}')
    thumbs = checkresponse(thumbs)
    return thumbs['data']

class Eagle:
    _librarypath = None

    def __init__(self, data = None):
        self.load(data)
    
    def updatelibrarypath(self, id):
        for p in _getlibraries():
            if os.path.isdir(os.path.join(p, 'images', id + '.info')):
                self._librarypath = p
                return
    
    def folderpath(self, id):
        folderpath = os.path.join(self._librarypath, 'images', id + '.info')
        if not os.path.isdir(folderpath):
            self.updatelibrarypath(id)
            folderpath = os.path.join(self._librarypath, 'images', id + '.info')
        return folderpath
        
    def getimageinfo(self, id):
        return _getimageinfo(id)

    def sessiondata(self):
        return self._librarypath

    def loadimages(self, n=100):
        imgs = _getimages(n)
        for img in imgs:
            if img['width'] < img['height']:
                height = min(img['height'], MAXMETRIC)
                width = int(img['width'] * height / img['height'])
            else:
                width = min(img['width'], MAXMETRIC)
                height = int(img['height'] * width / img['width'])
            img['thumbwidth'] = width
            img['thumbheight'] = height
            img['folder'] = self.folderpath(img['id'])
            thumbname = img['name'] + '_thumbnail.' + img['ext']
            if os.path.isfile(os.path.join(img['folder'], thumbname)):
                img['thumbname'] = thumbname
            else:
                img['thumbname'] = img['name'] + '.' + img['ext']
        return imgs

    def load(self, data):
        try:
            jsdata = json.loads(data) if data != None else {}
        except:
            jsdata = {}
        self._librarypath = jsdata.get('librarypath', '')
    
    def dump(self):
        return json.dumps({
            "librarypath":self._librarypath,
            })

if __name__ == "__main__":
    e = Eagle()
    imgs = e.loadimages()
