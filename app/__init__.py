from flask import Flask
import os
from dotenv import load_dotenv

load_dotenv()

def create_app():
    app = Flask(__name__)
    app.config['DEBUG'] = os.getenv('FLASK_DEBUG', '0') == '1'
    from . import routes
    app.register_blueprint(routes.bp)

    return app