from flask import Blueprint, jsonify, request
from ...models import PropertyStatus
from ...db import db

property_status_bp = Blueprint('property_status', __name__)

@property_status_bp.route('/', methods=['GET'])
def get_property_statuses():
    """
    Get all property statuses
    ---
    tags:
      - Property Status
    responses:
      200:
        description: A list of property statuses
        schema:
          type: object
          properties:
            property_statuses:
              type: array
              items:
                type: object
                properties:
                  propertystatusid:
                    type: integer
                    example: 1
                  description:
                    type: string
                    example: 'Available'
    """
    statuses = PropertyStatus.query.all()
    result = [{'propertystatusid': s.propertystatusid, 'description': s.description} for s in statuses]
    return jsonify({'data': result})

@property_status_bp.route('/<int:id>', methods=['GET'])
def get_property_status(id):
    """
    Get a single property status by ID
    ---
    tags:
      - Property Status
    parameters:
      - name: id
        in: path
        type: integer
        required: true
        description: The ID of the property status
    responses:
      200:
        description: A single property status
        schema:
          type: object
          properties:
            propertystatusid:
              type: integer
              example: 1
            description:
              type: string
              example: 'Available'
      404:
        description: PropertyStatus not found
    """
    status = PropertyStatus.query.get(id)
    if not status:
        return jsonify({'data': None, 'error': 'PropertyStatus not found'}), 404
    return jsonify({'data': {'propertystatusid': status.propertystatusid, 'description': status.description}})

@property_status_bp.route('/', methods=['POST'])
def create_property_status():
    """
    Create a new property status
    ---
    tags:
      - Property Status
    parameters:
      - name: body
        in: body
        required: true
        schema:
          type: object
          properties:
            description:
              type: string
              example: 'Available'
    responses:
      201:
        description: PropertyStatus created successfully
      400:
        description: Invalid input
    """
    data = request.json
    if not data or 'description' not in data:
        return jsonify({'data': None, 'error': 'Missing required field: description'}), 400
    try:
        new_status = PropertyStatus(description=data['description'])
        db.session.add(new_status)
        db.session.commit()
        return jsonify({'data': {'id': new_status.propertystatusid, 'message': 'PropertyStatus created successfully'}}), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({'data': None, 'error': f'Failed to create property status: {str(e)}'}), 400

@property_status_bp.route('/<int:id>', methods=['PUT'])
def update_property_status(id):
    """
    Update an existing property status
    ---
    tags:
      - Property Status
    parameters:
      - name: id
        in: path
        type: integer
        required: true
        description: The ID of the property status
      - name: body
        in: body
        required: true
        schema:
          type: object
          properties:
            description:
              type: string
              example: 'Unavailable'
    responses:
      200:
        description: PropertyStatus updated successfully
      404:
        description: PropertyStatus not found
      400:
        description: Invalid input
    """
    data = request.json
    status = PropertyStatus.query.get(id)
    if not status:
        return jsonify({'data': None, 'error': 'PropertyStatus not found'}), 404
    if not data or 'description' not in data:
        return jsonify({'data': None, 'error': 'Missing required field: description'}), 400
    try:
        status.description = data['description']
        db.session.commit()
        return jsonify({'data': {'message': 'PropertyStatus updated successfully'}})
    except Exception as e:
        db.session.rollback()
        return jsonify({'data': None, 'error': f'Failed to update property status: {str(e)}'}), 400

@property_status_bp.route('/<int:id>', methods=['DELETE'])
def delete_property_status(id):
    """
    Delete a property status
    ---
    tags:
      - Property Status
    parameters:
      - name: id
        in: path
        type: integer
        required: true
        description: The ID of the property status
    responses:
      200:
        description: PropertyStatus deleted successfully
      404:
        description: PropertyStatus not found
    """
    status = PropertyStatus.query.get(id)
    if not status:
        return jsonify({'data': None, 'error': 'PropertyStatus not found'}), 404
    try:
        db.session.delete(status)
        db.session.commit()
        return jsonify({'data': {'message': 'PropertyStatus deleted successfully'}})
    except Exception as e:
        db.session.rollback()
        return jsonify({'data': None, 'error': f'Failed to delete property status: {str(e)}'}), 400