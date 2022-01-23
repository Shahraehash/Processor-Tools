from flask import Blueprint, current_app, jsonify, request, make_response

from preprocessor_modules.shared import shared
from preprocessor_modules.encoder import encoder

parent_preprocessor = Blueprint(
    'parent_preprocessor',
    __name__,
    url_prefix='/preprocessor'
)

parent_preprocessor.register_blueprint(shared)
parent_preprocessor.register_blueprint(encoder)
