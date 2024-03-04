from eagleviewer import app
from flask import render_template,send_from_directory,redirect, session, request, jsonify
from .eagleapi import Eagle
from datetime import timedelta

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
    return render_template('images.html', list=imgs, folders=folders, foldername=foldername, URLBASE=app.URLBASE)

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

@app.route('/eagle/updatedb/start', methods=['POST'])
def eagle_updatedbstart():
    eagle = Eagle(session.get('EagleLibraryPath'))
    response = eagle.updatedb();
    session['EagleLibraryPath'] = eagle.dump()
    return jsonify(response)

@app.route('/eagle/updatedb/wait', methods=['GET'])
def eagle_updatedbwait():
    eagle = Eagle(session.get('EagleLibraryPath'))
    response = eagle.waitupdatedb();
    session['EagleLibraryPath'] = eagle.dump()
    return jsonify(response)

@app.route('/eagle/updatedb/abort', methods=['POST'])
def eagle_updatedbabort():
    eagle = Eagle(session.get('EagleLibraryPath'))
    eagle.abortupdatedb();
    session['EagleLibraryPath'] = eagle.dump()
    return jsonify({})

@app.route('/', methods=['GET'])
def index():
    return redirect('/eagle')