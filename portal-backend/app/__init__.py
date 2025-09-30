from flask import Flask
from .db import db
from .config import Config
from .blueprints.properties.routes import properties_bp
from .blueprints.tenants.routes import tenants_bp
from .blueprints.maintenance.routes import maintenance_bp

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    db.init_app(app)

    app.register_blueprint(properties_bp, url_prefix='/properties')
    app.register_blueprint(tenants_bp, url_prefix='/tenants')
    app.register_blueprint(maintenance_bp, url_prefix='/maintenance')

    return app