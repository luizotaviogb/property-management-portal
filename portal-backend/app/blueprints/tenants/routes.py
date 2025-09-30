from flask import Blueprint, jsonify, request
from ...models import Tenant, PaymentStatus, Property
from ...db import db

tenants_bp = Blueprint('tenants', __name__)

@tenants_bp.route('/', methods=['GET'])
def get_tenants():
    tenants = Tenant.query.join(PaymentStatus).join(Property).all()
    result = [
        {
            'id': t.tenantid,
            'name': t.name,
            'info': t.contactinfo,
            'leaseStart': t.leasetermstart.isoformat(),
            'leaseEnd': t.leasetermend.isoformat(),
            'paymentStatus': t.payment_status.description,
            'propertyId': t.propertyid
        } for t in tenants
    ]
    return jsonify({'tenants': result})

@tenants_bp.route('/<int:id>', methods=['PUT'])
def update_tenant(id):
    data = request.json
    tenant = Tenant.query.get(id)
    if not tenant:
        return jsonify({'error': 'Tenant not found'}), 404
    tenant.Name = data.get('name', tenant.Name)
    tenant.ContactInfo = data.get('contactinfo', tenant.ContactInfo)
    tenant.LeaseTermStart = data.get('leasetermstart', tenant.LeaseTermStart)
    tenant.LeaseTermEnd = data.get('leasetermend', tenant.LeaseTermEnd)
    tenant.PaymentStatusID = data.get('paymentstatusid', tenant.PaymentStatusID)
    tenant.PropertyID = data.get('propertyid', tenant.PropertyID)
    db.session.commit()
    return jsonify({'message': 'Tenant updated successfully'})

@tenants_bp.route('/<int:id>', methods=['DELETE'])
def delete_tenant(id):
    tenant = Tenant.query.get(id)
    if not tenant:
        return jsonify({'error': 'Tenant not found'}), 404
    db.session.delete(tenant)
    db.session.commit()
    return jsonify({'message': 'Tenant deleted successfully'})