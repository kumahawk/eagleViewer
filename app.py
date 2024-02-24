from flask import Flask,render_template,send_from_directory,redirect, session, request, jsonify
from eagleapi import Eagle
from os import path
from datetime import timedelta

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
def eagle():
    eagle = Eagle(session.get('EagleLibraryPath'))
    imgs = eagle.loadimages(folder=request.args.get('folder'), keyword=request.args.get('keyword'), tags=request.args.get('tags'))
    folders = eagle.loadfolders()
    foldername = eagle.getfoldername(request.args.get('folder'))
    session['EagleLibraryPath'] = eagle.dump()
    return render_template('images.html', list=imgs, folders=folders, foldername=foldername)

@app.route('/eagle/fetch/<id>/<int:num>', methods=['GET'])
def eagle_fetch(id, num):
    eagle = Eagle(session.get('EagleLibraryPath'))
    imgs = eagle.loadimages(num+200,skipuntil=id,folder=request.args.get('folder'), keyword=request.args.get('keyword'), tags=request.args.get('tags'))
    session['EagleLibraryPath'] = eagle.dump()
    json = {"images":imgs}
    return jsonify(json)

@app.route('/eagle2', methods=['GET'])
def eagle2():
    eagle = Eagle(session.get('EagleLibraryPath'))
    imgs = eagle.loadimages(folder=request.args.get('folder'), keyword=request.args.get('keyword'), tags=request.args.get('tags'))
    folders = eagle.loadfolders()
    foldername = eagle.getfoldername(request.args.get('folder'))
    session['EagleLibraryPath'] = eagle.dump()
    return render_template('images2.html', list=imgs, folders=folders, foldername=foldername, targetid=imgs[0]['id'])

@app.route('/', methods=['GET'])
def index():
    return redirect('/eagle')

if __name__ == "__main__":
    app.run(port=5000, debug=True)