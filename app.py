from flask import Flask,render_template,send_from_directory,redirect, session, request, jsonify
from eagleapi import Eagle
from os import path
from datetime import timedelta
import datetime

app = Flask(__name__)
app.secret_key = 'EagleIsWashiInJapanese'
app.permanent = True
app.permanent_session_lifetime = timedelta(days=30)
app.config["JSON_AS_ASCII"] = False

@app.route('/images/<id>/<file>', methods=['GET'])
def images(id, file):
    eagle = Eagle(session.get('EagleLibraryPath'))
    folderpath = eagle.folderpath(id)
    session['EagleLibraryPath'] = eagle.dump()
    return send_from_directory(folderpath, file)

@app.route('/eagle', methods=['GET'])
def eagle_search():
    eagle = Eagle(session.get('EagleLibraryPath'))
    imgs = eagle.loadimages(60,folder=request.args.get('folder'), keyword=request.args.get('keyword'), tags=request.args.get('tags'))
    folders = eagle.loadfolders()
    foldername = eagle.getfoldername(request.args.get('folder'))
    session['EagleLibraryPath'] = eagle.dump()
    return render_template('images.html', list=imgs, folders=folders, foldername=foldername)

@app.route('/eagle/fetch', methods=['GET'])
@app.route('/eagle/fetch/<id>', methods=['GET'])
def eagle_fetch(id = None):
    eagle = Eagle(session.get('EagleLibraryPath'))
    imgs = eagle.loadimages(60,skipuntil=id,folder=request.args.get('folder'), keyword=request.args.get('keyword'), tags=request.args.get('tags'))
    session['EagleLibraryPath'] = eagle.dump()
    json = {"images":imgs, "finish": (len(imgs) < 60) }
    return jsonify(json)

@app.route('/eagle/update/<id>', methods=['POST'])
def eagle_update(id):
    eagle = Eagle(session.get('EagleLibraryPath'))
    json = request.get_json()
    imgs = eagle.update(id, json)
    session['EagleLibraryPath'] = eagle.dump()
    return jsonify(imgs)

@app.route('/eagle/updatedb', methods=['GET'])
def eagle_updatedb():
    now = datetime.datetime.now()
    eagle = Eagle(session.get('EagleLibraryPath'))
    eagle.updateDb();
    session['EagleLibraryPath'] = eagle.dump()
    lapse = datetime.datetime(2000,1,1,0,0,0,0) + (datetime.datetime.now() - now)
    return render_template('updatedb.html', lapse=lapse)

@app.route('/', methods=['GET'])
def index():
    return redirect('/eagle')

if __name__ == "__main__":
    app.run(port=5000, debug=True)