from flask import *

app = Flask(__name__)

@app.route("/", methods=["GET","POST"])
def hello_world():
    if request.method == 'POST':
      # upload file flask
        f = request.files.get('file')
    return render_template("index.html")