from flask import Flask, send_from_directory, redirect, request

app = Flask(__name__)

@app.route('/', methods=['GET'])
def index():
    return redirect('/home')

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

@app.route('/cringyss')
def cringe():
    return send_from_directory(app.static_folder, path='cringyss/cringe.html')

# Query Demo
@app.route('/gettest', methods=['GET'])
def gettest():
    if request.method == 'GET' and "color" in request.args:
        website=f"""
                <html>
                <style>
                body {{
                    background: {request.args.get("color")};
                }}
                </style>
                <body>
                {request.args.get("q")}
                </body>
                </html>
        """
        return website
    else: return "No Got..."
    
        

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=80)