
import os
from sqlalchemy.ext.automap import automap_base
from sqlalchemy import create_engine
from sqlalchemy import event

# SqlAlchemy を使うための共通変数を定義している
Base = automap_base()
engine = create_engine('sqlite:///' + os.environ.get('EAGLEVIEWERDB'))
Base.prepare(engine)

Images = Base.classes.images
Folders = Base.classes.folders
Tags = Base.classes.tags
Libraries = Base.classes.libraries

@event.listens_for(engine, "connect")
def set_sqlite_pragma(dbapi_connection, connection_record):
    cursor = dbapi_connection.cursor()
    cursor.execute("PRAGMA foreign_keys = ON")
    cursor.close()
