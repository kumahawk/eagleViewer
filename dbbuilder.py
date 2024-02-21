from eagledb import engine, Folders, Tags, Libraries, Images
from sqlalchemy.orm import Session
import datetime
import os
import json

def addFolder(session, library, folders, parent):
    for f in folders:
        if f['modificationTime'] / 1000 > library.lastupdate.timestamp():
            folder = session.get(Folders, f['id'])
            if not folder:
                folder = Folders(id=f["id"])
                session.add(folder)
            folder.name = f['name']
            folder.modificationTime = datetime.datetime.fromtimestamp(f['modificationTime']/1000)
            folder.parent = parent
            if f['children']:
                addFolder(session, f['children'], f['id'])

def addTags(session, tagname, library):
    tag = session.query(Tags).filter(Tags.name == tagname).one_or_none()
    if tag == None:
        tag = Tags()
        session.add(tag)
        tag.name = tagname
        tag.prefered = 0
        tag.libid = library.id
    return tag

def addImages(session, i, library):
    img = session.get(Images, i["id"])
    if img == None:
        img = Images(id=i["id"])
        session.add(img)
    img.libId = library.id
    img.name = i['name']
    img.size = i["size"]
    img.btime = datetime.datetime.fromtimestamp(i["btime"]/1000)
    img.mtime = datetime.datetime.fromtimestamp(i["mtime"]/1000)
    img.ext = i["ext"]
    img.annotation = i["annotation"]
    img.modificationTime = datetime.datetime.fromtimestamp(i["modificationTime"]/1000)
    img.height = i["height"]
    img.width = i["width"]
    img.noThumbnail = i.get("noThumbnail", False)
    img.lastModified = datetime.datetime.fromtimestamp(i["lastModified"]/1000)
    img.star = i.get("star")
    img.tags_collection = [addTags(session, tag, library) for tag in i["tags"]]
    img.folders_collection = [session.get(Folders, fid) for fid in i["folders"]]
    img.isDeleted = i["isDeleted"]

def builddb(path):
    decoder = json.JSONDecoder()
    now = datetime.datetime.now()
    with Session(engine) as session:
        library = session.query(Libraries).filter(Libraries.path == path).one()
        with open(os.path.join(path, "metadata.json"), encoding="utf-8") as f:
            folders = decoder.raw_decode(f.readline())[0]
        addFolder(session, library, folders["folders"], None)
        session.flush()
        imagesdir = os.path.join(path, "images")
        for imginfo in os.listdir(imagesdir):
            file = os.path.join(imagesdir, imginfo, "metadata.json")
            if os.path.isfile(file):
                sresult = os.stat(file)
                with open(file, encoding="utf-8") as f:
                    img = decoder.raw_decode(f.readline())[0]
                if img['isDeleted'] or library.lastupdate == None or library.lastupdate.timestamp() < sresult.st_mtime:
                    addImages(session, img, library)
                    session.flush()
        library.lastupdate = now
        session.commit()

builddb("C:\\exchange\eagle\\SD.library")