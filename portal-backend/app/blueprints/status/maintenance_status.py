from flask import Blueprint, jsonify, request
from ...models import MaintenanceStatus
from ...db import db

maintenance_status_bp = Blueprint('maintenance_status', __name__)

@maintenance_status_bp.route('/', methods=['GET'])
def get_maintenance_statuses():
    statuses = MaintenanceStatus.query.all()
    result = [{'maintenancestatusid': s.maintenancestatusid, 'description': s.description} for s in statuses]
    return jsonify({'data': result})

@maintenance_status_bp.route('/<int:id>', methods=['GET'])
def get_maintenance_status(id):
    status = MaintenanceStatus.query.get(id)
    if not status:
        return jsonify({'data': None, 'error': 'MaintenanceStatus not found'}), 404
    return jsonify({'data': {'maintenancestatusid': status.maintenancestatusid, 'description': status.description}})

@maintenance_status_bp.route('/', methods=['POST'])
def create_maintenance_status():
    data = request.json
    if not data or 'description' not in data:
        return jsonify({'data': None, 'error': 'Missing required field: description'}), 400
    try:
        new_status = MaintenanceStatus(description=data['description'])
        db.session.add(new_status)
        db.session.commit()
        return jsonify({'data': {'id': new_status.maintenancestatusid, 'message': 'MaintenanceStatus created successfully'}}), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({'data': None, 'error': f'Failed to create maintenance status: {str(e)}'}), 400

@maintenance_status_bp.route('/<int:id>', methods=['PUT'])
def update_maintenance_status(id):
    data = request.json
    status = MaintenanceStatus.query.get(id)
    if not status:
        return jsonify({'data': None, 'error': 'MaintenanceStatus not found'}), 404
    if not data or 'description' not in data:
        return jsonify({'data': None, 'error': 'Missing required field: description'}), 400
    try:
        status.description = data['description']
        db.session.commit()
        return jsonify({'data': {'message': 'MaintenanceStatus updated successfully'}})
    except Exception as e:
        db.session.rollback()
        return jsonify({'data': None, 'error': f'Failed to update maintenance status: {str(e)}'}), 400

@maintenance_status_bp.route('/<int:id>', methods=['DELETE'])
def delete_maintenance_status(id):
    status = MaintenanceStatus.query.get(id)
    if not status:
        return jsonify({'data': None, 'error': 'MaintenanceStatus not found'}), 404
    try:
        db.session.delete(status)
        db.session.commit()
        return jsonify({'data': {'message': 'MaintenanceStatus deleted successfully'}})
    except Exception as e:
        db.session.rollback()
        return jsonify({'data': None, 'error': f'Failed to delete maintenance status: {str(e)}'}), 400
