from flask import Blueprint, jsonify
from ...models import Property, PropertyType, PropertyStatus
from ...db import db

properties_bp = Blueprint('properties', __name__)

@properties_bp.route('/', methods=['GET'])
def get_properties():
    properties = Property.query.join(PropertyType).join(PropertyStatus).all()
    result = [
        {
            'id': p.propertyid,
            'address': p.address,
            'type': p.property_type.description,
            'status': p.property_status.description,
            'purchaseDate': p.purchasedate.isoformat(),
            'price': float(p.price)
        } for p in properties
    ]
    return jsonify({'properties': result})