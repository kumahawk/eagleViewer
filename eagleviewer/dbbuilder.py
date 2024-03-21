from .eagledb import engine, Folders, Tags, Libraries, Images
from sqlalchemy.orm import Session
import datetime
import os
import json
import threading
import logging

logger = logging.getLogger(__name__)

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

def threadmain(me, path):
    me.run(path)

mylock = threading.Lock()

class Worker:
    _thread = None
    _progress = 0
    _fullgage = 0
    _processed = 0
    _error = ""
    _abort = False
    _start = datetime.datetime.now()

    def builddb(self, path):
        decoder = json.JSONDecoder()
        with Session(engine) as session:
            library = session.query(Libraries).filter(Libraries.path == path).one()
            logger.debug(f"build DB start {self._start}:{library.lastupdate}")
            imagesdir = os.path.join(path, "images")
            with os.scandir(imagesdir) as it:
                files = [entry.name for entry in it if entry.name.endswith('.info') and entry.is_dir()]
            self._fullgage = len(files)
            with open(os.path.join(path, "metadata.json"), encoding="utf-8") as f:
                folders = decoder.raw_decode(f.readline())[0]
            addFolder(session, library, folders["folders"], None)
            session.flush()
            for i in range(len(files)):
                if self._abort:
                    self._error = "中止しました"
                    return
                self._progress = i
                file = os.path.join(imagesdir, files[i], "metadata.json")
                try:
                    sresult = os.stat(file)
                    if library.lastupdate == None or library.lastupdate.timestamp() < sresult.st_mtime:
                        logger.debug(f"process {library.lastupdate.timestamp()}:{sresult.st_mtime}")
                        with open(file, encoding="utf-8") as f:
                            img = decoder.raw_decode(f.readline())[0]
                        addImages(session, img, library)
                        session.flush()
                        self._processed += 1
                except:
                    pass
            self._progress = len(files)
            library.lastupdate = self._start
            session.commit()

    def run(self, path):
        try:
            self.builddb(path)
        except Exception as e:
            self._error = e
        except:
            self._error = "不明なエラー"
        finally:
            self._thread = None

    def start(self, path):
        with mylock:
            if self._thread == None:
                self._thread = threading.Thread(target = threadmain, args = (self, path))
                self._progress = 0
                self._fullgage = 0
                self._processed = 0
                self._error = ""
                self._abort = False
                self._start = datetime.datetime.now()
                try:
                    self._thread.start()
                except Exception as e:
                    self._error = e
                    self._thread = None
                except:
                    self._error = "不明なエラー"
                    self._thread = None

    def wait(self, timeout):
        thread = self._thread
        if thread and thread.is_alive():
            thread.join(timeout)
        now = datetime.datetime.now()
        logger.debug(f"build DB end {now}:{self._processed}")
        return { "error": self._error, "fullgage": self._fullgage, "aborted": self._abort,
                 "progress": self._progress, "running": thread.is_alive() if thread else False,
                 "processed": self._processed, "elapsed": str(now - self._start) }

    def abort(self):
        self._abort = True

worker = Worker()

def start(path):
    worker.start(path)

def wait(timeout):
    return worker.wait(timeout)

def abort():
    worker.abort()