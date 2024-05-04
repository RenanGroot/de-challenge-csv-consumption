import os
from flask import *
from werkzeug.utils import secure_filename
from aux_functions import csv_to_sql, check_upload_status, weekly_avg_reg


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
    if request.args.get("region"):
        region = request.args.get("region")
        average = weekly_avg_reg(region)
        return str(average)

    else:
        lat1 = request.args.get("lat1")
        lat2 = request.args.get("lat2")
        long1 = request.args.get("long1")
        long2 = request.args.get("long2")
        lat_min = min(lat1, lat2)
        lat_max = max(lat1, lat2)
        long_min = min(long1, long2)
        long_max = max(long1, long2)