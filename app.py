import os
from flask import *
from werkzeug.utils import secure_filename
from aux_functions import csv_to_sql, check_upload_status


UPLOAD_FOLDER = 'landing-files/'
ALLOWED_EXTENSIONS = {"csv"}

app = Flask(__name__)

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route("/", methods=["GET","POST"])
def upload_file():
    if request.method == 'POST':
        # upload file flask
        f = request.files.get('file')
      
        # Preventing user from giving wrong file format
        if f and allowed_file(f.filename):
            
            # Creating a filepath according to the template
            filename = secure_filename(f.filename)
            filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)

            # Saving the data into the /landing-files
            f.save(filepath)

            csv_to_sql(filepath, filename)

            return f"Reachout: 127.0.0.1:5000/uploadstatus/{filename} for checking the current status"#redirect(url_for('upload_status', name=filename))

    # GET Method
    return render_template("index.html")


@app.route('/uploadstatus/<name>')
def upload_status(name):
    
    status = check_upload_status(name)

    return f"<h1>The current status: {status}</h1>"

#TODO
# Calculate boxing by taking the smaller value and using that as the bondaries to create the region
@app.route("/query")
def query_data():
    lat1 = request.args.get("lat")
    lat2 = request.args.get("lat")
    long1 = request.args.get("long")
    long2 = request.args.get("long")
    region = request.args.get("region")