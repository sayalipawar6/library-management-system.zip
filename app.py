# Main setup file that starts up our Flask web application.
# It configures settings, hooks up the database, and loads all the separate routes.
from flask import Flask, redirect, url_for

from config import Config
from db import init_db


def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)

    # Fire up the database tables
    init_db(app)

    # Pull in our distinct feature modules (Blueprints)
    from auth import bp as auth_bp
    from books import bp as books_bp
    from loans import bp as loans_bp
    from reports import bp as reports_bp

    # Register each section with our main app instance
    app.register_blueprint(auth_bp)
    app.register_blueprint(books_bp)
    app.register_blueprint(loans_bp)
    app.register_blueprint(reports_bp)

    # Basic error handler for broken URLs
    @app.errorhandler(404)
    def not_found(e):
        return "Page not found.", 404

    # Basic error handler for backend code crashes
    @app.errorhandler(500)
    def server_error(e):
        return "Something went wrong on our end.", 500

    return app


if __name__ == "_main_":
    app = create_app()
    app.run(debug=True)