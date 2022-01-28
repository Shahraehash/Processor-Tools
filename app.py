from flask import Flask, send_from_directory
from flask_cors import CORS
import os

from modules.parent_preprocessor import parent_preprocessor

app = Flask(__name__,
            static_folder = "./dist/static",
            template_folder = "./dist")

#Enable CORS
CORS(app, resources={r'/*': {'origins': '*'}})

#Create file storage location if doesn't exist
app.config['UPLOAD_FOLDER'] = 'files'
if not os.path.exists(app.config['UPLOAD_FOLDER']):
    os.makedirs(app.config['UPLOAD_FOLDER'])

#Routes
@app.route('/')
def home(path='index.html'):
    return send_from_directory('dist', path)

#Modules
app.register_blueprint(parent_preprocessor)

if __name__ == '__main__':
    app.run()
