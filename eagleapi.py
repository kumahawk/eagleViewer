import requests
import json
import os.path
from sqlalchemy.orm import Session
from sqlalchemy import desc
from eagledb import engine, Images, Folders, Tags, Libraries

MAXMETRIC = 256

class Eagle:
    _library = None
    _session = None

    def __init__(self, data = None):
        self.load(data)
    
    def __del__(self):
        if self._session:
            self._session.close()

    def getSession(self):
        if not self._session:
            self._session = Session(engine)
        return self._session
    
    def getFolders(self, pid, parents):
        session = self.getSession()
        output = []
        for f in session.query(Folders).filter(Folders.parent == pid):
            path = [*parents, f.name]
            output += [{"id": f.id,
                        "name":f.name,
                        "displayname":"|" * len(parents) + f.name,
                        "path": "/".join(path)
                        }]
            output += self.getFolders(f.id, path)
        return output

    
    def updatelibrary(self, id):
        session = self.getSession()
        if not self._library:
            self._library = session.query(Libraries).first()
        else:
            for l in session.query(Libraries):
                if os.path.isdir(os.path.join(l.path, 'images', id + '.info')):
                    self._library = l
                    return
    
    def loadLibrary(self, path):
        session = self.getSession()
        self._library = session.query(Libraries).filter(Libraries.path == path).one()

    def librarypath(self, id = None):
        if not self._library:
            self.updatelibrary(id)
        return self._library.path

    def folderpath(self, id):
        folderpath = os.path.join(self.librarypath(id), 'images', id + '.info')
        return folderpath

    def getimageinfo(self, id):
        img = self.getSession().get(Images, id)
        return { key:getattr(img, key) for key in img.__dict__ if hasattr(img, key) }

    def loadimages(self, n=100, offset=0, folder=None, keyword=None, tags=None):
        session = self.getSession()
        conditions = []
        if folder:
            f = session.get(Folders, folder)
            if f:
                conditions.append(Images.folders_collection.contains(f))
        if tags:
            tag = session.query(Tags).filter(Tags.name == tags).one_or_none()
            if tag != None:
                conditions.append(Images.tags_collection.contains(tag))
        if keyword:
            conditions.append(Images.annotation.like(f"%{keyword}%"))
        if conditions:
            imgs = session.query(Images).filter(*conditions).order_by(desc(Images.id)).offset(offset).limit(n)
        else:
            imgs = session.query(Images).order_by(desc(Images.id)).offset(offset).limit(n)
        result = []
        for img in imgs:
            i = { key:getattr(img, key) for key in img.__dict__ if hasattr(img, key) }
            if img.width < img.height:
                height = min(img.height, MAXMETRIC)
                width = int(img.width * height / img.height)
            else:
                width = min(img.width, MAXMETRIC)
                height = int(img.height * width / img.width)
            i['thumbwidth'] = width
            i['thumbheight'] = height
            i['folder'] = self.folderpath(img.id)
            if img.noThumbnail:
                i['thumbname'] = img.name + '.' + img.ext
            else:
                i['thumbname'] = img.name + '_thumbnail.' + img.ext
            result.append(i)
        return result

    def load(self, data):
        try:
            jsdata = json.loads(data) if data != None else {}
        except:
            jsdata = {}
        if 'librarypath' in jsdata:
            self.loadLibrary(jsdata.get('librarypath'))
        else:
            self._library = None
    
    def dump(self):
        return json.dumps({
            "librarypath": self._library.path if self._library else None,
            })
    
    def loadtags(self):
        libpath = self.librarypath()
        images = os.path.join(libpath, 'images')
        tags = {}
        decoder = json.JSONDecoder()
        for file in os.listdir(images):
            iddir = os.path.join(images, file)
            metadata = os.path.join(iddir, 'metadata.json')
            if os.path.isdir(iddir) and os.path.isfile(metadata):
                with open(metadata, encoding="utf-8") as f:
                    meta = decoder.raw_decode(f.readline())
                    for tag in meta[0]['tags']:
                        tags[tag] = tag
        return tags.values()

    def loadfolders(self):
        return self.getFolders(None, [])

if __name__ == "__main__":
    e = Eagle()
    imgs = e.loadimages()
    #imgs = e.loadimages(keyword="'NSFW'")
    #imgs = e.loadtags()
    print(imgs)
