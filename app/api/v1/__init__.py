
from flask import Blueprint
from flask_restful import Api

bp = Blueprint('v1', __name__)
api = Api(bp)

from . import views
