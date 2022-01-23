from flask import Blueprint, current_app, jsonify, request, make_response
import pandas as pd
import numpy as np
import os
import time
import json

import uuid

from datetime import datetime

shared_routes = Blueprint(
    'shared_routes',
    __name__,
    url_prefix='/shared'
)

@shared_routes.route('/one',methods=['POST'])
def one():
    print('one')
    return make_response({'test':'test'})
