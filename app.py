from flask import Flask, render_template, g, jsonify, request, redirect, url_for, session, flash, make_response, send_file
from flask_cors import CORS
import os

app = Flask(__name__,
            static_folder = "./dist/static",
            template_folder = "./dist")

#Enable CORS
CORS(app, resources={r'/*': {'origins': '*'}})

#Modules
from preprocessor_modules.parent_preprocessor import parent_preprocessor
app.register_blueprint(parent_preprocessor)

#Create file storage location if doesn't exist
if not os.path.exists('files'):
    os.makedirs('files')
#Upload configuration
UPLOAD_FOLDER = 'files'
app.config['UPLOAD_FOLDER'] =  UPLOAD_FOLDER

#Routes
@app.route('/')
def home():
    #clearFiles()
    return render_template("index.html")

@app.route('/', defaults={'path': ''})
@app.route('/<path:path>')
def index(path):
    try:
        #clearFiles()
        return render_template('index.html')
    except Exception as e:
        print(e)
        print('change')
        return str(e)
