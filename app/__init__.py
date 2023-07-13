# -*- coding: UTF-8 -*-
import traceback
from flask import Flask, g, jsonify, request, Response
from werkzeug.exceptions import HTTPException
from app.api.v1 import api as api_v1
import config
from flask import Flask

from app.api.v1.repositories.healthz import admin_panel_login_ms_health_check
from app.services.app_exceptions import CustomException


def create_app():
    app = Flask(__name__)
    app.config.from_object(config)
    app.config['JSON_AS_ASCII'] = False
    app.config['SECRET_KEY'] = 'any secret string'

    @app.route("/healthz", methods=["GET"])
    def health_checking():
        return admin_panel_login_ms_health_check()

    @app.errorhandler(CustomException)
    def handle_invalid_usage(error):
        response = jsonify(error.to_dict())
        response.status_code = error.status_code
        return response

    if not app.debug:
        @app.errorhandler(Exception)
        def handle_error(e):
            code = 500
            if isinstance(e, HTTPException):
                code = e.code
            print(traceback.format_exc())
            return jsonify(error=str(e)), code


    @api_v1.before_request
    def relogin_if_needed():
        pass

    @api_v1.after_request
    def set_auth_header(response):
        response.headers['Access-Control-Expose-Headers'] = "Authorization"

        user_token = g.get('user_token', None)
        if user_token:
            response.headers['User-Group'] = user_token['user_groups']
        user_group = g.get('user_group_in_login', None)
        if user_group:
            response.headers['User-Group'] = user_group

        response.headers['Cache-Control'] = 'no-cache'

        return response

    app.register_blueprint(api_v1, url_prefix='/api/v1')

    return app
