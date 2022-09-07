# developed by: Samiulhaq Chardiwall
# LinkedIn: https://www.linkedin.com/in/chardiwall/
# start time: 20/july/2022

# Document Name: __init__.py
# Application Name: Medical Care Final Year Project


# --------------------------------Libraries---------------------------------
import os
from flask import Flask

# --------------------------------------------------------------------------------
def create_app():
    app = Flask('Medical Care')

    app.config['SECRET_KEY'] = os.urandom(30)


    # blueprint for auth routes in our app
    from .auth import auth as auth_blueprint
    app.register_blueprint(auth_blueprint)

    # blueprint for non-auth parts of app
    from .main import main as main_blueprint
    app.register_blueprint(main_blueprint)

    return app