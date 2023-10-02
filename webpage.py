from flask import Flask, send_from_directory, redirect, request, render_template, session
app = Flask(__name__)
app.secret_key = "super secret key"

@app.route('/', methods=['GET'])
def index():
    return redirect('/home')

@app.route('/home')
def home():
    return send_from_directory(app.static_folder, path='home/index.html')

@app.route('/biosite/bio')
def bio():
    return send_from_directory(app.static_folder, path='biosite/html/bio.html')

@app.route('/biosite/schedule')
def schedule():
    return send_from_directory(app.static_folder, path='biosite/html/schedule.html')

@app.route('/biosite/favorites')
def links():
    return send_from_directory(app.static_folder, path='biosite/html/favorites.html')

@app.route('/cringyss')
def cringe():
    return send_from_directory(app.static_folder, path='cringyss/cringe.html')

@app.route('/coolss')
def cool():
    return send_from_directory(app.static_folder, path='coolss/index.html')

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

@app.route('/game')
def game():
    return send_from_directory(app.static_folder, path='game/index.html')

@app.route("/ajax")
def ajaxdemo():
    return send_from_directory(app.static_folder ,"AJAXdemo/demo.html")

import random
@app.route('/random')
def rand():
    return str(random.randint(0, 100))

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=80)