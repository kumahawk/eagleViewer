from flask import Flask,render_template,send_from_directory,redirect, session
from eagleapi import Eagle
from os import path
from datetime import timedelta

app = Flask(__name__)
app.secret_key = 'EagleIsWashiInJapanese'
app.permanent_session_lifetime = timedelta(minutes=30)

@app.route('/images/<id>/<file>', methods=['GET'])
def images(id, file):
    eagle = Eagle(session.get('EagleLibraryPath'))
    session['EagleLibraryPath'] = eagle.sessiondata()
    return send_from_directory(path.join(eagle.librarypath(), 'images', id + '.info'), file)

@app.route('/eagle/<id>', methods=['GET'])
def eagleimage(id):
    eagle = Eagle(session.get('EagleLibraryPath'))
    img = eagle.getimageinfo(id)
    session['EagleLibraryPath'] = eagle.sessiondata()
    return render_template('eagleimage.html', img=img)

@app.route('/eagle', methods=['GET'])
def eagle():
    eagle = Eagle(session.get('EagleLibraryPath'))
    imgs = eagle.loadimages()
    session['EagleLibraryPath'] = eagle.sessiondata()
    return render_template('images.html', list=imgs)

@app.route('/', methods=['GET'])
def index():
    return redirect('/eagle')

if __name__ == "__main__":
    app.run(port=8000, debug=True)