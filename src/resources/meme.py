from flask import Blueprint, redirect, url_for


meme = Blueprint('meme', __name__)


@meme.route('/upload')
def upload():
    # TODO
    return redirect(url_for('main.gallery'))
