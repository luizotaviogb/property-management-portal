from flask import Blueprint, jsonify, request
from ...models import PaymentStatus
from ...db import db

payment_status_bp = Blueprint('payment_status', __name__)

@payment_status_bp.route('/', methods=['GET'])
def get_payment_statuses():
    statuses = PaymentStatus.query.all()
    result = [{'paymentstatusid': s.paymentstatusid, 'description': s.description} for s in statuses]
    return jsonify({'data': result})

@payment_status_bp.route('/<int:id>', methods=['GET'])
def get_payment_status(id):
    status = PaymentStatus.query.get(id)
    if not status:
        return jsonify({'data': None, 'error': 'PaymentStatus not found'}), 404
    return jsonify({'data': {'paymentstatusid': status.paymentstatusid, 'description': status.description}})

@payment_status_bp.route('/', methods=['POST'])
def create_payment_status():
    data = request.json
    if not data or 'description' not in data:
        return jsonify({'data': None, 'error': 'Missing required field: description'}), 400
    try:
        new_status = PaymentStatus(description=data['description'])
        db.session.add(new_status)
        db.session.commit()
        return jsonify({'data': {'id': new_status.paymentstatusid, 'message': 'PaymentStatus created successfully'}}), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({'data': None, 'error': f'Failed to create payment status: {str(e)}'}), 400

@payment_status_bp.route('/<int:id>', methods=['PUT'])
def update_payment_status(id):
    data = request.json
    status = PaymentStatus.query.get(id)
    if not status:
        return jsonify({'data': None, 'error': 'PaymentStatus not found'}), 404
    if not data or 'description' not in data:
        return jsonify({'data': None, 'error': 'Missing required field: description'}), 400
    try:
        status.description = data['description']
        db.session.commit()
        return jsonify({'data': {'message': 'PaymentStatus updated successfully'}})
    except Exception as e:
        db.session.rollback()
        return jsonify({'data': None, 'error': f'Failed to update payment status: {str(e)}'}), 400

@payment_status_bp.route('/<int:id>', methods=['DELETE'])
def delete_payment_status(id):
    status = PaymentStatus.query.get(id)
    if not status:
        return jsonify({'data': None, 'error': 'PaymentStatus not found'}), 404
    try:
        db.session.delete(status)
        db.session.commit()
        return jsonify({'data': {'message': 'PaymentStatus deleted successfully'}})
    except Exception as e:
        db.session.rollback()
        return jsonify({'data': None, 'error': f'Failed to delete payment status: {str(e)}'}), 400
