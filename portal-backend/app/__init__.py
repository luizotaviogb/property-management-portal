from flask import Flask, send_from_directory
from .db import db
from .config import Config
from .blueprints.properties.routes import properties_bp
from .blueprints.tenants.routes import tenants_bp
from .blueprints.maintenance.routes import maintenance_bp
from .blueprints.status.property_status import property_status_bp
from .blueprints.status.payment_status import payment_status_bp
from .blueprints.status.maintenance_status import maintenance_status_bp
from .blueprints.status.property_type import property_type_bp
from flask_restful import Api, Resource
from flasgger import Swagger
import os

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    db.init_app(app)

    app.register_blueprint(properties_bp, url_prefix='/properties')
    app.register_blueprint(tenants_bp, url_prefix='/tenants')
    app.register_blueprint(maintenance_bp, url_prefix='/maintenance')
    app.register_blueprint(property_status_bp, url_prefix='/property_status')
    app.register_blueprint(payment_status_bp, url_prefix='/payment_status')
    app.register_blueprint(maintenance_status_bp, url_prefix='/maintenance_status')
    app.register_blueprint(property_type_bp, url_prefix='/property_type')

    swagger = Swagger(app)
    api = Api(app)

    return app