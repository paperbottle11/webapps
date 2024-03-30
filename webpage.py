from flask import Flask, send_from_directory, redirect, request, render_template, session, make_response, jsonify, abort
import firebase_admin
from firebase_admin import credentials, firestore
from firebase_admin.firestore import FieldFilter

app = Flask(__name__)
app.secret_key = "super secret key"

@app.route('/', methods=['GET'])
def index():
    return redirect('/home')

@app.route('/home')
def home():
    return send_from_directory(app.static_folder, path='home/index.html')

#region Bio
@app.route('/biosite/bio')
def bio():
    return send_from_directory(app.static_folder, path='biosite/html/bio.html')

@app.route('/biosite/schedule')
def schedule():
    return send_from_directory(app.static_folder, path='biosite/html/schedule.html')

@app.route('/biosite/favorites')
def links():
    return send_from_directory(app.static_folder, path='biosite/html/favorites.html')

#endregion

@app.route('/cringyss')
def cringe():
    return send_from_directory(app.static_folder, path='cringyss/cringe.html')

@app.route('/coolss')
def cool():
    return send_from_directory(app.static_folder, path='coolss/index.html')

#region Quiz
def quiz_results(bread, animal, icecream):
    breadIdx = ["white", "sourdough", "wholegrain", "french"].index(bread)
    animalIdx = ["wolf", "giraffe", "flyingsquirrel", "portabellamushroom"].index(animal)
    # icecreamIdx = ["pickle", "buffalosauce", "mayo"].index(icecream)
    result = [["speedster", "truck", "limittest", "dui"],
              ["speedster", "truck", "limittest", "dui"],
              ["demon", "beetledriver", "demon", "beetledriver"],
              ["speedster", "beetledriver", "limittest", "beetledriver"]]
    return result[breadIdx][animalIdx]

@app.route('/popquiz')
def popquiz():
    if request.method == 'GET' and "quiz" in request.args:
        num = int(request.args["quiz"])
        if num == 1:
            session["name"] = request.args["name"]
            session["bread"] = request.args["bread"]
        elif num == 2:
            session["animal"] = request.args["animal"]
        elif num == 3:
            session["icecream"] = request.args["icecream"]           
            result = quiz_results(session["bread"], session["animal"], session["icecream"])
            return render_template('popquiz/results.html', name=session["name"], bread=session["bread"], animal=session["animal"], icecream=session["icecream"], result=result)

        return render_template(f'popquiz/form{num+1}.html')
    return render_template('popquiz/form1.html')

#endregion

@app.route('/game')
def game():
    return send_from_directory(app.static_folder, path='game/index.html')

cred = credentials.Certificate("creds.json")
firebase_admin.initialize_app(cred)
db = firestore.client()

#region Survey
def login_is_required(function):  #a function to check if the user is authorized or not
    def wrapper(*args, **kwargs):
        if "sub" not in session:  #authorization required
            return redirect("/")
        else:
            return function()

    return wrapper

@app.route('/survey')
@login_is_required
def survey():
    return send_from_directory(app.static_folder, path='survey/index.html')

@app.route('/vote', methods=['POST'])
def vote():
    cookie = request.form.get('cookie')
    sub = session["sub"]
    if cookie:
        votes_ref = db.collection("votes")
        query = votes_ref.where(filter=FieldFilter("sub", "==", session.get("sub")))
        doc = query.stream()
        doc = list(doc)
        if len(doc) > 0:
            doc = doc[0]
        else:
            doc = None

        if doc:
            if doc.to_dict().get("sub") == session.get("sub"):
                db.collection('votes').document(doc.id).delete()
        
        vote_ref = db.collection('votes').add({
            'cookie': cookie,
            'sub': sub,
            'timestamp': firestore.SERVER_TIMESTAMP
        })
        print(vote_ref[-1].id)
        resp = make_response(redirect('/results'))
        resp.set_cookie('vote_id', vote_ref[-1].id)
        return resp
    return redirect('/survey')

@app.route('/check/<doc_id>', methods=['GET'])
def check_id(doc_id):
    doc_ref = db.collection('votes').document(doc_id)
    doc = doc_ref.get()
    if doc.exists:
        return jsonify({"exists": "yes"})
    else:
        return jsonify({"exists": "no"})

@app.route('/results')
def results():
    votes = {}
    docs = db.collection('votes').stream()
    for doc in docs:
        cookie = doc.to_dict().get('cookie')
        votes[cookie] = votes.get(cookie, 0) + 1

    userVote = None
    
    votes_ref = db.collection("votes")
    query = votes_ref.where(filter=FieldFilter("sub", "==", session.get("sub")))
    doc = query.stream()
    doc = list(doc)
    if len(doc) > 0:
        doc = doc[0]
    else:
        doc = None
    
    if doc:
        doc = doc.to_dict()
        if doc.get("sub") == session.get("sub"):
            userVote = doc.get('cookie')
            if userVote == "chocolatechip":
                userVote = "Chocolate Chip"
            elif userVote == "snickerdoodle":
                userVote = "Snickerdoodle"
            elif userVote == "oatmealraisin":
                userVote = "Oatmeal Raisin"
            elif userVote == "peanutbutter":
                userVote = "Peanut Butter"
    return render_template('survey/results.html', votes=votes, vote=userVote, session=session)

#endregion

#region Todo
@app.route('/todo')
def todo():
    return render_template('todolist/list.html')

@app.route('/list')
def todolist():
    docs = db.collection('todo_list').stream()
    output=[]
    for doc in docs:
        doc_dict=doc.to_dict()
        doc_dict["_id"]=doc.id
        output.append(doc_dict)
 
    return jsonify(output)
    
@app.route('/toggle/<doc_id>')
def toggle(doc_id):
    docref = db.collection('todo_list').document(doc_id)
    doc = docref.get()
    if doc.exists:
        is_complete = doc.to_dict().get('is_complete', False)
        docref.update({"is_complete": not is_complete})
    return ""

@app.route('/add', methods=['GET'])
def add_item():
    if "item" in request.args:
        item=request.args["item"]
        db.collection('todo_list').add({
            'item': item,
            'is_complete': False,
            'timestamp': firestore.SERVER_TIMESTAMP
        })
    return ""

@app.route('/remove/<doc_id>')
def remove(doc_id):
    docref = db.collection('todo_list').document(doc_id)
    doc = docref.get()
    if doc.exists:
        docref.delete()
    return ""

#endregion

from google.oauth2 import id_token
from google_auth_oauthlib.flow import Flow
import google.auth.transport.requests
from pip._vendor import cachecontrol
import os
import requests

os.environ["OAUTHLIB_INSECURE_TRANSPORT"] = "1" #REMOVE THIS WHEN YOU DEPLOY
GOOGLE_CLIENT_ID = "814599710052-ltc00tda5lapj8kna16rpqm2r6vm7kbp.apps.googleusercontent.com"


flow = Flow.from_client_secrets_file(  
	client_secrets_file="oauth.json",
	scopes=["https://www.googleapis.com/auth/userinfo.profile", "https://www.googleapis.com/auth/userinfo.email", "openid"],  
	redirect_uri="http://localhost:80/callback?page=results" #FIX THIS WHEN YOU DEPLOY
)

@app.route("/login")  #the page where the user can login
def login():
    authorization_url, state = flow.authorization_url()  #asking the flow class for the authorization (login) url
    session["state"] = state
    return redirect(authorization_url)

@app.route("/logout")  #the page where the user can login
def logout():
    session.clear()
    if "page" in request.args: page = request.args["page"]
    else: page = "home"
    return redirect(f"/{page}")

@app.route("/callback")  #this is the page that will handle the callback process meaning process after the authorization
def callback():
    flow.fetch_token(authorization_response=request.url)

    if not session["state"] == request.args["state"]:
        abort(500)  #state does not match!

    credentials = flow.credentials
    request_session = requests.session()
    cached_session = cachecontrol.CacheControl(request_session)
    token_request = google.auth.transport.requests.Request(session=cached_session)

    id_info = id_token.verify_oauth2_token(
        id_token=credentials._id_token,
        request=token_request,
        audience=GOOGLE_CLIENT_ID
    )
    id_info = dict(id_info)
    print(id_info["sub"])
    session.update(id_info)
    
    if "page" in request.args: page = request.args["page"]
    else: page = "home"
    return redirect(f"/{page}")

@app.route("/gifs")
def gifs():
    return send_from_directory(app.static_folder, "hshgifs/gifs.html")

if __name__ == '__main__':
    app.config['TEMPLATES_AUTO_RELOAD'] = True
    app.run(host="0.0.0.0", port=80)