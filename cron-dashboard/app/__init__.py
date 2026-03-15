from flask import Flask
from werkzeug.middleware.proxy_fix import ProxyFix

from app.config import Config
from app.models import db


def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    db.init_app(app)
    with app.app_context():
        db.create_all()

    from app.routes import api, dashboard, logs, tasks
    app.register_blueprint(dashboard.bp)
    app.register_blueprint(tasks.bp, url_prefix='/tasks')
    app.register_blueprint(logs.bp, url_prefix='/logs')
    app.register_blueprint(api.bp, url_prefix='/api')

    from app.scheduler import init_scheduler
    init_scheduler(app)

    app.wsgi_app = ProxyFix(app.wsgi_app, x_prefix=1, x_for=1, x_proto=1, x_host=1)

    return app
