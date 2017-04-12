from flask import Blueprint, Response
import models
import os

blueprint = Blueprint(os.path.dirname(os.path.realpath(__file__)).split("/")[-1], __name__, template_folder='templates', static_folder='static')

@blueprint.route('/')
def index():
    return ProfileSchema(many=True).jsonify(Profile.query.all)
