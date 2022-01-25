from flask import Blueprint, current_app

from .shared import shared
from .column_reducer import column_reducer
from .colinearity import colinearity
from .feature_selector import feature_selector
from .train_test_split import train_test_split
from .encoder import encoder

import simplejson

parent_preprocessor = Blueprint(
    'parent_preprocessor',
    __name__,
    url_prefix='/preprocessor_api'
)

parent_preprocessor.register_blueprint(shared)
parent_preprocessor.register_blueprint(column_reducer)
parent_preprocessor.register_blueprint(colinearity)
parent_preprocessor.register_blueprint(feature_selector)
parent_preprocessor.register_blueprint(train_test_split)
parent_preprocessor.register_blueprint(encoder)

#Audit Tool for Routes
@parent_preprocessor.route('/route_map',methods=['POST'])
def preprocessor_route_map():
    routes = [str(p) for p in current_app.url_map.iter_rules()]
    result = list(filter(lambda x: parent_preprocessor.url_prefix in x, routes))
    return simplejson.dumps(result)
