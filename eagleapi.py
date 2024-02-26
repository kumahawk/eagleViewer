import requests
import json
import os.path
from sqlalchemy.orm import Session
from sqlalchemy import desc
from eagledb import engine, Images, Folders, Tags, Libraries
import dbbuilder

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
    
    def getFolders(self, pid):
        session = self.getSession()
        output = []
        for f in session.query(Folders).filter(Folders.parent == pid):
            output += [{"id": f.id,
                        "name":f.name,
                        "children": self.getFolders(f.id)
                        }]
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
        i = { key:getattr(img, key) for key in img.__dict__ if hasattr(img, key) }
        i['folders'] = [ f.name for f in img.folders_collection]
        i['tags'] = [ t.name for t in img.tags_collection]
        return i
    
    def loadimages(self, n=100, offset=0, folder=None, keyword=None, tags=None, skipuntil=None):
        session = self.getSession()
        conditions = []
        if folder:
            if folder == ',':
                conditions.append(~Images.folders_collection.any())
                conditions.append(Images.star == None)
            elif folder == 'star5':
                conditions.append(Images.star == 5)
            elif folder == 'star4':
                conditions.append(Images.star == 4)
            elif folder == 'star3':
                conditions.append(Images.star == 3)
            elif folder == 'star2':
                conditions.append(Images.star == 2)
            elif folder == 'star1':
                conditions.append(Images.star == 1)
            elif folder == 'star0':
                conditions.append(Images.star == 0)
            elif folder == 'star':
                conditions.append(Images.star > 0)
            else:
                for fid in folder.split(','):
                    if fid:
                        f = session.get(Folders, fid)
                        if f:
                            conditions.append(Images.folders_collection.contains(f))
        if tags:
            for t in tags.split(','):
                if t:
                    tag = session.query(Tags).filter(Tags.name == t).one_or_none()
                    if tag != None:
                        conditions.append(Images.tags_collection.contains(tag))
        if skipuntil:
            conditions.append(Images.id < skipuntil)
        if keyword:
            conditions.append(Images.annotation.like(f"%{keyword}%"))
        if conditions:
            imgs = session.query(Images).filter(*conditions).order_by(desc(Images.id)).offset(offset).limit(n)
        else:
            imgs = session.query(Images).order_by(desc(Images.id)).offset(offset).limit(n)
        result = []
        for img in imgs:
            i = {key:getattr(img, key) for key in ('id','name','ext','noThumbnail','annotation','star')}
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
            i['folders'] = [ f.name for f in img.folders_collection]
            i['tags'] = [ t.name for t in img.tags_collection]
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
        return self.getFolders(None)

    def getfoldername(self, fid):
        if not fid:
            return '全画像'
        elif fid == ',':
            return '未選択'
        elif fid.startswith('star'):
            return '星' + fid[len('star'):]
        else:
            folder = self.getSession().get(Folders, fid)
            return folder.name if folder else '全画像'
    
    def update(self, id, req):
        req["id"] = id
        response = requests.post(
            "http://localhost:41595/api/item/update",
            data=json.dumps(req),
            headers={"Content-Type": "application/json"}
        )
        if response.status_code == requests.codes.ok:
            session = self.getSession()
            image = session.get(Images, id)
            if image:
                image.star = req['star']
                session.commit()
        return json.loads(response.text)

    def updateDb(self):
        dbbuilder.builddb(self.librarypath())

if __name__ == "__main__":
    e = Eagle()
    imgs = e.loadimages()
    #imgs = e.loadimages(keyword="'NSFW'")
    #imgs = e.loadtags()
    print(imgs)
