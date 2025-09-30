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
    result = [{'propertystatusid': s.PropertyStatusID, 'description': s.Description} for s in statuses]
    return jsonify({'property_statuses': result})

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
        return jsonify({'error': 'PropertyStatus not found'}), 404
    return jsonify({'propertystatusid': status.PropertyStatusID, 'description': status.Description})

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
    new_status = PropertyStatus(Description=data['Description'])
    db.session.add(new_status)
    db.session.commit()
    return jsonify({'message': 'PropertyStatus created successfully'}), 201

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
        return jsonify({'error': 'PropertyStatus not found'}), 404
    status.Description = data['Description']
    db.session.commit()
    return jsonify({'message': 'PropertyStatus updated successfully'})

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
        return jsonify({'error': 'PropertyStatus not found'}), 404
    db.session.delete(status)
    db.session.commit()
    return jsonify({'message': 'PropertyStatus deleted successfully'})