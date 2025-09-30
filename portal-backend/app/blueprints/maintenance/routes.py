from flask import Blueprint, jsonify, request
from ...models import Maintenance, MaintenanceStatus, Property
from ...db import db

maintenance_bp = Blueprint('maintenance', __name__)

@maintenance_bp.route('/', methods=['GET'])
def get_maintenance():
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
    return jsonify({'maintenance': result})

@maintenance_bp.route('/<int:id>', methods=['PUT'])
def update_maintenance(id):
    data = request.json
    maintenance = Maintenance.query.get(id)
    if not maintenance:
        return jsonify({'error': 'Maintenance task not found'}), 404
    maintenance.Description = data.get('description', maintenance.Description)
    maintenance.MaintenanceStatusID = data.get('maintenancestatusid', maintenance.MaintenanceStatusID)
    maintenance.ScheduledDate = data.get('scheduleddate', maintenance.ScheduledDate)
    maintenance.PropertyID = data.get('propertyid', maintenance.PropertyID)
    db.session.commit()
    return jsonify({'message': 'Maintenance task updated successfully'})

@maintenance_bp.route('/<int:id>', methods=['DELETE'])
def delete_maintenance(id):
    maintenance = Maintenance.query.get(id)
    if not maintenance:
        return jsonify({'error': 'Maintenance task not found'}), 404
    db.session.delete(maintenance)
    db.session.commit()
    return jsonify({'message': 'Maintenance task deleted successfully'})