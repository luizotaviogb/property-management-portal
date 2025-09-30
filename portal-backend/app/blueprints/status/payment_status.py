from flask import Blueprint, jsonify, request
from ...models import PaymentStatus
from ...db import db

payment_status_bp = Blueprint('payment_status', __name__)

@payment_status_bp.route('/', methods=['GET'])
def get_payment_statuses():
    statuses = PaymentStatus.query.all()
    result = [{'paymentstatusid': s.PaymentStatusID, 'description': s.Description} for s in statuses]
    return jsonify({'payment_statuses': result})

@payment_status_bp.route('/<int:id>', methods=['GET'])
def get_payment_status(id):
    status = PaymentStatus.query.get(id)
    if not status:
        return jsonify({'error': 'PaymentStatus not found'}), 404
    return jsonify({'paymentstatusid': status.PaymentStatusID, 'description': status.Description})

@payment_status_bp.route('/', methods=['POST'])
def create_payment_status():
    data = request.json
    new_status = PaymentStatus(Description=data['Description'])
    db.session.add(new_status)
    db.session.commit()
    return jsonify({'message': 'PaymentStatus created successfully'}), 201

@payment_status_bp.route('/<int:id>', methods=['PUT'])
def update_payment_status(id):
    data = request.json
    status = PaymentStatus.query.get(id)
    if not status:
        return jsonify({'error': 'PaymentStatus not found'}), 404
    status.Description = data['Description']
    db.session.commit()
    return jsonify({'message': 'PaymentStatus updated successfully'})

@payment_status_bp.route('/<int:id>', methods=['DELETE'])
def delete_payment_status(id):
    status = PaymentStatus.query.get(id)
    if not status:
        return jsonify({'error': 'PaymentStatus not found'}), 404
    db.session.delete(status)
    db.session.commit()
    return jsonify({'message': 'PaymentStatus deleted successfully'})