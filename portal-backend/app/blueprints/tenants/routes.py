from flask import Blueprint, jsonify
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