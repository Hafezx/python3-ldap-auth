from flask_apiblueprint import APIBlueprint

api = APIBlueprint('api_v1', __name__)

from . import urls
