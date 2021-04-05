from flask import Blueprint


drink = Blueprint('drink', __name__)


@drink.route('/upload')
def upload(self):
    return "Hello World!"
