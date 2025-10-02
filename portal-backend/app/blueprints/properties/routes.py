from flask import Blueprint, jsonify, request
from sqlalchemy.exc import IntegrityError
from ...models import Property, PropertyType, PropertyStatus
from ...db import db
from datetime import datetime

properties_bp = Blueprint('properties', __name__)

@properties_bp.route('/', methods=['GET'])
def get_properties():
    """
    Get a list of properties
    ---
    tags:
      - Properties
    parameters:
      - name: status
        in: query
        type: string
        description: Filter by property status
      - name: type
        in: query
        type: string
        description: Filter by property type
      - name: sort
        in: query
        type: string
        description: Sort by field (price, purchaseDate)
      - name: order
        in: query
        type: string
        description: Sort order (asc, desc)
    responses:
      200:
        description: A list of properties
        schema:
          type: object
          properties:
            data:
              type: array
              items:
                type: object
                properties:
                  id:
                    type: integer
                  address:
                    type: string
                  type:
                    type: string
                  status:
                    type: string
                  purchaseDate:
                    type: string
                    format: date-time
                  price:
                    type: number
                    format: float
    """
    query = Property.query.join(PropertyType).join(PropertyStatus)

    status_filter = request.args.get('status')
    if status_filter:
        query = query.filter(PropertyStatus.description.ilike(f'%{status_filter}%'))

    type_filter = request.args.get('type')
    if type_filter:
        query = query.filter(PropertyType.description.ilike(f'%{type_filter}%'))

    sort_by = request.args.get('sort', 'propertyid')
    order = request.args.get('order', 'asc')

    if sort_by == 'price':
        query = query.order_by(Property.price.asc() if order == 'asc' else Property.price.desc())
    elif sort_by == 'purchaseDate':
        query = query.order_by(Property.purchasedate.asc() if order == 'asc' else Property.purchasedate.desc())
    else:
        query = query.order_by(Property.propertyid.asc() if order == 'asc' else Property.propertyid.desc())

    properties = query.all()
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
    return jsonify({'data': result})

@properties_bp.route('/', methods=['POST'])
def create_property():
    """
    Create a new property
    ---
    tags:
      - Properties
    parameters:
      - name: body
        in: body
        required: true
        schema:
          type: object
          required:
            - address
            - typeId
            - statusId
            - purchaseDate
            - price
          properties:
            address:
              type: string
              example: "123 Main St, Paris, 75001"
            typeId:
              type: integer
              example: 1
            statusId:
              type: integer
              example: 1
            purchaseDate:
              type: string
              format: date
              example: "2024-01-15"
            price:
              type: number
              format: float
              example: 500000.00
    responses:
      201:
        description: Property created successfully
        schema:
          type: object
          properties:
            data:
              type: object
              properties:
                id:
                  type: integer
                message:
                  type: string
      400:
        description: Invalid input
    """
    data = request.json

    if not data:
        return jsonify({'data': None, 'error': 'No data provided'}), 400

    required_fields = ['address', 'typeId', 'statusId', 'purchaseDate', 'price']
    missing_fields = [field for field in required_fields if field not in data]
    if missing_fields:
        return jsonify({'data': None, 'error': f'Missing required fields: {", ".join(missing_fields)}'}), 400

    if not isinstance(data.get('address'), str) or len(data['address'].strip()) == 0:
        return jsonify({'data': None, 'error': 'Address must be a non-empty string'}), 400

    try:
        price = float(data['price'])
        if price < 0:
            return jsonify({'data': None, 'error': 'Price cannot be negative'}), 400
    except (ValueError, TypeError):
        return jsonify({'data': None, 'error': 'Price must be a valid number'}), 400

    try:
        datetime.strptime(str(data['purchaseDate']), '%Y-%m-%d')
    except ValueError:
        return jsonify({'data': None, 'error': 'Purchase date must be in YYYY-MM-DD format'}), 400

    try:
        new_property = Property(
            address=data['address'],
            propertytypeid=data['typeId'],
            propertystatusid=data['statusId'],
            purchasedate=data['purchaseDate'],
            price=data['price']
        )
        db.session.add(new_property)
        db.session.commit()
        return jsonify({'data': {'id': new_property.propertyid, 'message': 'Property created successfully'}}), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({'data': None, 'error': f'Failed to create property: {str(e)}'}), 400

@properties_bp.route('/<int:id>', methods=['GET'])
def get_property_by_id(id):
    """
    Get a property by its ID
    ---
    tags:
      - Properties
    parameters:
      - name: id
        in: path
        type: integer
        required: true
        description: The ID of the property
    responses:
      200:
        description: A property object
        schema:
          type: object
          properties:
            data:
              type: object
              properties:
                id:
                  type: integer
                address:
                  type: string
                type:
                  type: string
                status:
                  type: string
                typeId:
                  type: integer
                statusId:
                  type: integer
                purchaseDate:
                  type: string
                  format: date-time
                price:
                  type: number
                  format: float
      404:
        description: Property not found
    """
    property = Property.query.join(PropertyType).join(PropertyStatus).filter(Property.propertyid == id).first()
    if not property:
        return jsonify({'data': None, 'error': 'Property not found'}), 404
    result = {
        'id': property.propertyid,
        'address': property.address,
        'type': property.property_type.description,
        'status': property.property_status.description,
        'typeId': property.propertytypeid,
        'statusId': property.propertystatusid,
        'purchaseDate': property.purchasedate.isoformat(),
        'price': float(property.price)
    }
    return jsonify({'data': result})

@properties_bp.route('/<int:id>', methods=['PUT'])
def update_property(id):
    """
    Update a property
    ---
    tags:
      - Properties
    parameters:
      - name: id
        in: path
        type: integer
        required: true
        description: The ID of the property
    requestBody:
      required: true
      content:
        application/json:
          schema:
            type: object
            properties:
              address:
                type: string
              typeId:
                type: integer
              statusId:
                type: integer
              purchaseDate:
                type: string
                format: date-time
              price:
                type: number
                format: float
    responses:
      200:
        description: Property updated successfully
      404:
        description: Property not found
    """
    data = request.json
    property_ = Property.query.get(id)
    if not property_:
        return jsonify({'data': None, 'error': 'Property not found'}), 404
    property_.address = data.get('address', property_.address)
    property_.propertytypeid = data.get('typeId', property_.propertytypeid)
    property_.propertystatusid = data.get('statusId', property_.propertystatusid)
    property_.purchasedate = data.get('purchaseDate', property_.purchasedate)
    property_.price = data.get('price', property_.price)
    db.session.commit()
    return jsonify({'data': {'message': 'Property updated successfully'}})

@properties_bp.route('/<int:id>', methods=['DELETE'])
def delete_property(id):
    """
    Delete a property
    ---
    tags:
      - Properties
    parameters:
      - name: id
        in: path
        type: integer
        required: true
        description: The ID of the property
    responses:
      200:
        description: Property deleted successfully
      404:
        description: Property not found
      409:
        description: Cannot delete property due to related records
    """
    property_ = Property.query.get(id)
    if not property_:
        return jsonify({'data': None, 'error': 'Property not found'}), 404

    try:
        db.session.delete(property_)
        db.session.commit()
        return jsonify({'data': {'message': 'Property deleted successfully'}})
    except IntegrityError:
        db.session.rollback()
        return jsonify({
            'data': None,
            'error': 'Cannot delete property because it has associated leases or maintenance records. Please delete or reassign them first.'
        }), 409