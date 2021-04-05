from flask import Blueprint, redirect, url_for


drink = Blueprint('drink', __name__)


@drink.route('/upload')
def upload():
    # TODO
    return redirect(url_for('main.gallery'))
