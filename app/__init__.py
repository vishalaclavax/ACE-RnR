from flask import Flask
from flask.cli import load_dotenv
from flask_wtf.csrf import CSRFProtect
from flask_mail import Mail
from flask.sessions import SessionInterface
# from flask_compress import Compress
from flask_htmlmin import HTMLMIN

#from app.utils.cosmos_connect import CosmosConnect
from app.services.api_client_service import APIClient
from flask_socketio import SocketIO

csrf = CSRFProtect() # https://flask-wtf.readthedocs.io/en/v0.14.2/csrf.html
#cosmos = CosmosConnect()
# compress = Compress()
socketio = SocketIO()

mail=Mail()

def create_app(config=None):
    load_dotenv()

    app = Flask(__name__, instance_relative_config=True)

    app.url_map.strict_slashes = False
    app.jinja_env.trim_blocks = True
    app.jinja_env.lstrip_blocks = True

    # load default config
    app.config.from_object('app.config')
    # load instance config
    app.config.from_pyfile('config.py', silent=True)
    # load app specific config
    if config is not None:
        if isinstance(config, dict):
            app.config.update(config)
        elif isinstance(config, str) and config.endswith('.py'):
            app.config.from_pyfile(config)

    # extensions
    # sess.init_app(app)
    csrf.init_app(app)
    #cosmos.init_app(app)
    mail.init_app(app)
    socketio.init_app(app)
    # compress.init_app(app)
    htmlmin = HTMLMIN(app)
    
    APIClient.logger = app.logger

    from . import blueprints
    blueprints.register(app)

    return app
