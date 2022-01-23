from flask import Blueprint, current_app, jsonify, request, make_response

from preprocessor_modules.shared import shared
from preprocessor_modules.colinearity import colinearity
from preprocessor_modules.encoder import encoder

parent_preprocessor = Blueprint(
    'parent_preprocessor',
    __name__,
    url_prefix='/preprocessor_api'
)

parent_preprocessor.register_blueprint(shared)
parent_preprocessor.register_blueprint(colinearity)
parent_preprocessor.register_blueprint(encoder)
