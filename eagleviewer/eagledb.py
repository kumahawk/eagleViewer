
import os
from sqlalchemy.ext.automap import automap_base
from sqlalchemy import create_engine

# SqlAlchemy を使うための共通変数を定義している
Base = automap_base()
engine = create_engine('sqlite:///' + os.environ.get('EAGLEVIEWERDB'))
Base.prepare(engine)

Images = Base.classes.images
Folders = Base.classes.folders
Tags = Base.classes.tags
Libraries = Base.classes.libraries