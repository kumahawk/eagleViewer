from flask import Flask,render_template,send_from_directory
import eagleapi
from os import path

app = Flask(__name__)

library_root = None

@app.route('/images/<id>/<file>', methods=['GET'])
def images(id, file):
    global library_root
    return send_from_directory(path.join(library_root, 'images', id + '.info\\', file)

@app.route('/', methods=['GET'])
def index():
    global library_root
    if not library_root:
        library_root = eagleapi.getlibraries()[0]
    imgs = eagleapi.getimages()
    return render_template('images.html', list=imgs)

if __name__ == "__main__":
    app.run(port=8000, debug=True)