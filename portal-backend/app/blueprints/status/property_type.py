from flask import Blueprint, jsonify, request
from ...models import PropertyType
from ...db import db

property_type_bp = Blueprint('property_type', __name__)

@property_type_bp.route('/', methods=['GET'])
def get_property_types():
    """
    Get all property types
    ---
    tags:
      - Property Type
    responses:
      200:
        description: A list of property types
        schema:
          type: object
          properties:
            property_types:
              type: array
              items:
                type: object
                properties:
                  propertytypeid:
                    type: integer
                    example: 1
                  description:
                    type: string
                    example: Apartment
    """
    types = PropertyType.query.all()
    result = [{'propertytypeid': t.PropertyTypeID, 'description': t.Description} for t in types]
    return jsonify({'property_types': result})

@property_type_bp.route('/<int:id>', methods=['GET'])
def get_property_type(id):
    """
    Get a single property type by ID
    ---
    tags:
      - Property Type
    parameters:
      - name: id
        in: path
        type: integer
        required: true
        description: The ID of the property type
    responses:
      200:
        description: A single property type
        schema:
          type: object
          properties:
            propertytypeid:
              type: integer
              example: 1
            description:
              type: string
              example: Apartment
      404:
        description: PropertyType not found
    """
    type_ = PropertyType.query.get(id)
    if not type_:
        return jsonify({'error': 'PropertyType not found'}), 404
    return jsonify({'propertytypeid': type_.PropertyTypeID, 'description': type_.Description})

@property_type_bp.route('/', methods=['POST'])
def create_property_type():
    """
    Create a new property type
    ---
    tags:
      - Property Type
    parameters:
      - name: body
        in: body
        required: true
        schema:
          type: object
          properties:
            description:
              type: string
              example: Apartment
    responses:
      201:
        description: PropertyType created successfully
      400:
        description: Invalid input
    """
    data = request.json
    new_type = PropertyType(Description=data['Description'])
    db.session.add(new_type)
    db.session.commit()
    return jsonify({'message': 'PropertyType created successfully'}), 201

@property_type_bp.route('/<int:id>', methods=['PUT'])
def update_property_type(id):
    """
    Update an existing property type
    ---
    tags:
      - Property Type
    parameters:
      - name: id
        in: path
        type: integer
        required: true
        description: The ID of the property type
      - name: body
        in: body
        required: true
        schema:
          type: object
          properties:
            description:
              type: string
              example: Apartment
    responses:
      200:
        description: PropertyType updated successfully
      404:
        description: PropertyType not found
      400:
        description: Invalid input
    """
    data = request.json
    type_ = PropertyType.query.get(id)
    if not type_:
        return jsonify({'error': 'PropertyType not found'}), 404
    type_.Description = data['Description']
    db.session.commit()
    return jsonify({'message': 'PropertyType updated successfully'})

@property_type_bp.route('/<int:id>', methods=['DELETE'])
def delete_property_type(id):
    """
    Delete a property type
    ---
    tags:
      - Property Type
    parameters:
      - name: id
        in: path
        type: integer
        required: true
        description: The ID of the property type
    responses:
      200:
        description: PropertyType deleted successfully
      404:
        description: PropertyType not found
    """
    type_ = PropertyType.query.get(id)
    if not type_:
        return jsonify({'error': 'PropertyType not found'}), 404
    db.session.delete(type_)
    db.session.commit()
    return jsonify({'message': 'PropertyType deleted successfully'})