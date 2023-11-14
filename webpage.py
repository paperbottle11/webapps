from flask import Flask, send_from_directory, redirect, request, render_template, session, make_response, jsonify
import firebase_admin
from firebase_admin import credentials, firestore

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
@app.route('/survey')
def survey():
    if request.cookies.get('vote_id'):
        return redirect('/results')
    return send_from_directory(app.static_folder, path='survey/index.html')

@app.route('/vote', methods=['POST'])
def vote():
    cookie = request.form.get('cookie')
    if cookie:
        vote_ref = db.collection('votes').add({
            'cookie': cookie,
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
    return render_template('survey/results.html', votes=votes)

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
 
    return output
    
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

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=80)