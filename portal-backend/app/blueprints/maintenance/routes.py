from flask import Blueprint, jsonify, request
from ...models import Maintenance, MaintenanceStatus, Property
from ...db import db

maintenance_bp = Blueprint('maintenance', __name__)

@maintenance_bp.route('/', methods=['GET'])
def get_maintenance():
    """
    Get a list of maintenance tasks
    ---
    tags:
      - Maintenance
    responses:
      200:
        description: A list of maintenance tasks
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
                  description:
                    type: string
                  status:
                    type: string
                  scheduledDate:
                    type: string
                    format: date-time
                  propertyId:
                    type: integer
    """
    maintenance_tasks = Maintenance.query.join(MaintenanceStatus).join(Property).all()
    result = [
        {
            'id': m.taskid,
            'description': m.description,
            'status': m.maintenance_status.description,
            'scheduledDate': m.scheduleddate.isoformat(),
            'propertyId': m.propertyid
        } for m in maintenance_tasks
    ]
    return jsonify({'data': result})

@maintenance_bp.route('/<int:id>', methods=['GET'])
def get_maintenance_by_id(id):
    """
    Get a maintenance task by its ID
    ---
    tags:
      - Maintenance
    parameters:
      - name: id
        in: path
        type: integer
        required: true
        description: The ID of the maintenance task
    responses:
      200:
        description: A maintenance task object
      404:
        description: Maintenance task not found
    """
    maintenance = Maintenance.query.join(MaintenanceStatus).join(Property).filter(Maintenance.taskid == id).first()
    if not maintenance:
        return jsonify({'data': None, 'error': 'Maintenance task not found'}), 404
    result = {
        'id': maintenance.taskid,
        'description': maintenance.description,
        'status': maintenance.maintenance_status.description,
        'statusId': maintenance.maintenancestatusid,
        'scheduledDate': maintenance.scheduleddate.isoformat(),
        'propertyId': maintenance.propertyid
    }
    return jsonify({'data': result})

@maintenance_bp.route('/', methods=['POST'])
def create_maintenance():
    """
    Create a new maintenance task
    ---
    tags:
      - Maintenance
    parameters:
      - name: body
        in: body
        required: true
        schema:
          type: object
          required:
            - description
            - maintenancestatusid
            - scheduleddate
            - propertyid
          properties:
            description:
              type: string
              example: "Replace broken window"
            maintenancestatusid:
              type: integer
              example: 3
            scheduleddate:
              type: string
              format: date
              example: "2024-03-15"
            propertyid:
              type: integer
              example: 1
    responses:
      201:
        description: Maintenance task created successfully
      400:
        description: Invalid input
    """
    data = request.json

    if not data:
        return jsonify({'data': None, 'error': 'No data provided'}), 400

    required_fields = ['description', 'maintenancestatusid', 'scheduleddate', 'propertyid']
    missing_fields = [field for field in required_fields if field not in data]
    if missing_fields:
        return jsonify({'data': None, 'error': f'Missing required fields: {", ".join(missing_fields)}'}), 400

    try:
        new_maintenance = Maintenance(
            description=data['description'],
            maintenancestatusid=data['maintenancestatusid'],
            scheduleddate=data['scheduleddate'],
            propertyid=data['propertyid']
        )
        db.session.add(new_maintenance)
        db.session.commit()
        return jsonify({'data': {'id': new_maintenance.taskid, 'message': 'Maintenance task created successfully'}}), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({'data': None, 'error': f'Failed to create maintenance task: {str(e)}'}), 400

@maintenance_bp.route('/<int:id>', methods=['PUT'])
def update_maintenance(id):
    """
    Update a maintenance task
    ---
    tags:
      - Maintenance
    parameters:
      - name: id
        in: path
        type: integer
        required: true
        description: The ID of the maintenance task
    requestBody:
      required: true
      content:
        application/json:
          schema:
            type: object
            properties:
              description:
                type: string
              maintenancestatusid:
                type: integer
              scheduleddate:
                type: string
                format: date
              propertyid:
                type: integer
    responses:
      200:
        description: Maintenance task updated successfully
      404:
        description: Maintenance task not found
    """
    data = request.json
    maintenance = Maintenance.query.get(id)
    if not maintenance:
        return jsonify({'data': None, 'error': 'Maintenance task not found'}), 404
    maintenance.description = data.get('description', maintenance.description)
    maintenance.maintenancestatusid = data.get('maintenancestatusid', maintenance.maintenancestatusid)
    maintenance.scheduleddate = data.get('scheduleddate', maintenance.scheduleddate)
    maintenance.propertyid = data.get('propertyid', maintenance.propertyid)
    db.session.commit()
    return jsonify({'data': {'message': 'Maintenance task updated successfully'}})

@maintenance_bp.route('/<int:id>', methods=['DELETE'])
def delete_maintenance(id):
    """
    Delete a maintenance task
    ---
    tags:
      - Maintenance
    parameters:
      - name: id
        in: path
        type: integer
        required: true
        description: The ID of the maintenance task
    responses:
      200:
        description: Maintenance task deleted successfully
      404:
        description: Maintenance task not found
    """
    maintenance = Maintenance.query.get(id)
    if not maintenance:
        return jsonify({'data': None, 'error': 'Maintenance task not found'}), 404
    db.session.delete(maintenance)
    db.session.commit()
    return jsonify({'data': {'message': 'Maintenance task deleted successfully'}})