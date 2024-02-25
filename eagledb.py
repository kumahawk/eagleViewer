
import os
from sqlalchemy.ext.automap import automap_base
from sqlalchemy import create_engine

# SqlAlchemy を使うための共通変数を定義している
Base = automap_base()
engine = create_engine('sqlite:///' + os.path.join(os.path.dirname(__file__), 'var', 'eagle.db'))
Base.prepare(engine)

Images = Base.classes.images
Folders = Base.classes.folders
Tags = Base.classes.tags
Libraries = Base.classes.libraries
