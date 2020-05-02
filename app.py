import os,time, sys
from flask import Flask,request,redirect, flash,send_from_directory,jsonify
from flask_restful import Resource, Api
import json
from werkzeug.utils import secure_filename
import json_tools as jt
import json_delta as jd
import requests
from camelot import read_pdf,  plot

app = Flask(__name__)
api = Api(app)

UPLOAD_FOLDER = '.'
ALLOWED_EXTENSIONS = {'pdf'}

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        if 'file' not in request.files:
            flash('No file part')
            return redirect(request.url)
        file = request.files['file']
        if file.filename == '':
            flash('No selected file')
            return redirect(request.url)
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        filepath = app.config['UPLOAD_FOLDER']+'/'+filename
        print(filepath)
        tables = read_pdf(filepath, pages='all', flavor='stream', columns=['87,289,365'])
        json_array = []
        for table in tables:
            data = json.loads(table.df.to_json(orient='records'))
            json_array.append(data)

        return jsonify(json_array)

    return '''
    <!doctype html>
    <title>Upload new File</title>
    <h1>Upload new File</h1>
    <form method=post enctype=multipart/form-data>
      <input type=file name=file>
      <input type=submit value=Upload>
    </form>
    '''   
@app.route('/uploads/<filename>')
def uploaded_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'],
                               filename)
     
if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')