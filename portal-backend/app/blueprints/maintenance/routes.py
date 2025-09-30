from flask import Blueprint, jsonify
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