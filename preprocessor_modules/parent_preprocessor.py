from flask import Blueprint, current_app, jsonify, request, make_response

from preprocessor_modules.shared_routes import shared_routes
from preprocessor_modules.encoder import encoder

parent_preprocessor = Blueprint(
    'parent_preprocessor',
    __name__,
    url_prefix='/preprocessor'
)

parent_preprocessor.register_blueprint(shared_routes)
parent_preprocessor.register_blueprint(encoder)
