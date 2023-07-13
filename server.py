import traceback
from flask import jsonify
from werkzeug.exceptions import HTTPException
from app import create_app
import config

app = create_app()

if __name__ == '__main__':
    app.run(debug=config.DEBUG, host=config.HOST, port=int(config.PORT))


if not app.debug:
    @app.errorhandler(Exception)
    def handle_error(e):
        code = 500
        if isinstance(e, HTTPException):
            code = e.code
        print(traceback.format_exc())
        return jsonify(error=str(e)), code
