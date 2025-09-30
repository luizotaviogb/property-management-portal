from flask import Blueprint, jsonify, request
from ...models import MaintenanceStatus
from ...db import db

maintenance_status_bp = Blueprint('maintenance_status', __name__)

@maintenance_status_bp.route('/', methods=['GET'])
def get_maintenance_statuses():
    statuses = MaintenanceStatus.query.all()
    result = [{'maintenancestatusid': s.MaintenanceStatusID, 'description': s.Description} for s in statuses]
    return jsonify({'maintenance_statuses': result})

@maintenance_status_bp.route('/<int:id>', methods=['GET'])
def get_maintenance_status(id):
    status = MaintenanceStatus.query.get(id)
    if not status:
        return jsonify({'error': 'MaintenanceStatus not found'}), 404
    return jsonify({'maintenancestatusid': status.MaintenanceStatusID, 'description': status.Description})

@maintenance_status_bp.route('/', methods=['POST'])
def create_maintenance_status():
    data = request.json
    new_status = MaintenanceStatus(Description=data['Description'])
    db.session.add(new_status)
    db.session.commit()
    return jsonify({'message': 'MaintenanceStatus created successfully'}), 201

@maintenance_status_bp.route('/<int:id>', methods=['PUT'])
def update_maintenance_status(id):
    data = request.json
    status = MaintenanceStatus.query.get(id)
    if not status:
        return jsonify({'error': 'MaintenanceStatus not found'}), 404
    status.Description = data['Description']
    db.session.commit()
    return jsonify({'message': 'MaintenanceStatus updated successfully'})

@maintenance_status_bp.route('/<int:id>', methods=['DELETE'])
def delete_maintenance_status(id):
    status = MaintenanceStatus.query.get(id)
    if not status:
        return jsonify({'error': 'MaintenanceStatus not found'}), 404
    db.session.delete(status)
    db.session.commit()
    return jsonify({'message': 'MaintenanceStatus deleted successfully'})