from flask import Flask
from flask_login import LoginManager
import logging.config


# Flask application instance
app = Flask(__name__)
app.config['SECRET_KEY'] = "gbsttu6sP9LGI4DF4N92W63FQVQdWsjl06Q8xvRSoZpFVfN9EO"

# mimetypes.init()
# mimetypes.add_type('image/svg+xml', '.svg')

# Flask login instance
signin = LoginManager(app)

# Log setup
logging.config.fileConfig("log_config.ini", disable_existing_loggers=False)
logging.getLogger("requests").setLevel(logging.WARNING)
logging.getLogger("urllib3").setLevel(logging.WARNING)
logging.getLogger("oauthlib").setLevel(logging.WARNING)
logging.getLogger("requests_oauthlib").setLevel(logging.WARNING)

from webapp import routes, analysis_routes
