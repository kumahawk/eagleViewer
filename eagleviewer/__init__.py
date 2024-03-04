from flask import Flask

app = Flask(__name__)
app.URLBASE = ''

import eagleviewer.views