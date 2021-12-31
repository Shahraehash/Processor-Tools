from flask import Blueprint


encoder = Blueprint(
    'encoder',
    __name__,
    url_prefix='/encoder'
)

@encoder.route("/process")
def process():
    print('test')
    return "test"
