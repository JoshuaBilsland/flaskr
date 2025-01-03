import os

from flask import Flask


def create_app(test_config=None):
    # Create and configure the app
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(
        # Default key "dev" is overriden with value in instance/config.py
        SECRET_KEY="dev",
        DATABASE=os.path.join(app.instance_path, 'flaskr.sqlite'),
    )

    if test_config is None:
        # Load the instance config, if it exists, when not testing
        app.config.from_pyfile('config.py', silent=True)
    else:
        # Load the test config if passed in
        app.config.from_mapping(test_config)

    # Ensure the instance folder exists
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    # A simple page that says hello
    @app.route('/hello')
    def hello():
        return 'Hello, World!'

    # Used to register the database functions with the application
    # and therefore lets you run the "init-db" command from the command line
    from . import db
    db.init_app(app)

    # Used to register the authentication blueprint with the application
    from . import auth
    app.register_blueprint(auth.bp)

    return app
