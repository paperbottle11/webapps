from flask import Flask, send_from_directory, redirect

app = Flask(__name__)

@app.route('/', methods=['GET'])
def index():
    return redirect('/home', code=303)

@app.route('/home')
def home():
    return send_from_directory(app.static_folder, path='home/index.html')

@app.route('/biosite/bio')
def bio():
    return send_from_directory(app.static_folder, path='biosite/html/bio.html')
    # return open("static/html/bio.html").read()

@app.route('/biosite/schedule')
def schedule():
    return send_from_directory(app.static_folder, path='biosite/html/schedule.html')

@app.route('/biosite/favorites')
def links():
    return send_from_directory(app.static_folder, path='biosite/html/favorites.html')

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=80)