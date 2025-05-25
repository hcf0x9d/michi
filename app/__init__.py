from flask import Flask
from datetime import datetime

from app.utils.helpers import markdown_to_html, format_datetime, time_ago, icon_for_mime
from config import SECRET_KEY


def create_app(config_name=None):
    app = Flask(__name__, instance_relative_config=True)

    # Config loading
    app.config.from_object("config")  # default config
    app.config.from_pyfile("config.py", silent=True)  # instance/config override
    app.jinja_env.filters["icon"] = icon_for_mime
    app.jinja_env.filters["format_datetime"] = format_datetime
    app.jinja_env.filters["markdown"] = markdown_to_html
    app.jinja_env.filters["time_ago"] = time_ago

    @app.context_processor
    def inject_now():
        return {'now': datetime.now()}

    @app.context_processor
    def inject_resource():
        return dict(flagship_resource=app.config.get("RESOURCE", ""))

    @app.context_processor
    def inject_booking():
        return dict(booking_link=app.config.get("BOOKING_LINK", ""))

    @app.context_processor
    def inject_nav():
        return dict(nav_links=app.config.get("NAV_LINKS", []))

    @app.context_processor
    def inject_social():
        return dict(social_links=app.config.get("SOCIAL_LINKS", []))

    @app.context_processor
    def inject_global_vars():
        return dict(
            GTM_ID=app.config.get("GTM_ID"),
            ENVIRONMENT=app.config.get("ENVIRONMENT"),
            SECRET_KEY=app.config.get("SECRET_KEY")
        )

    from .routes.public import public_bp
    app.register_blueprint(public_bp)
    return app
