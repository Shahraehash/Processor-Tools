from flask import Flask, render_template
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
app.config['UPLOAD_FOLDER'] = 'files'
if not os.path.exists(app.config['UPLOAD_FOLDER']):
    os.makedirs(app.config['UPLOAD_FOLDER'])

#Routes
@app.route('/')
def home():
    #clearFiles()
    return render_template("index.html")

@app.route('/', defaults={'path': ''})
@app.route('/<path:path>')
def index():
    try:
        #clearFiles()
        return render_template('index.html')
    except Exception as e:
        print(e)
        print('change')
        return str(e)
