from flask import Blueprint, jsonify, request
from ...models import Lease, Tenant, Property, PaymentStatus
from ...db import db
from datetime import datetime
from sqlalchemy import and_, or_

leases_bp = Blueprint('leases', __name__)

def check_lease_overlap(property_id, start_date, end_date, exclude_lease_id=None):
    query = Lease.query.filter(
        Lease.propertyid == property_id,
        or_(
            and_(Lease.leasetermstart <= start_date, Lease.leasetermend >= start_date),
            and_(Lease.leasetermstart <= end_date, Lease.leasetermend >= end_date),
            and_(Lease.leasetermstart >= start_date, Lease.leasetermend <= end_date)
        )
    )

    if exclude_lease_id:
        query = query.filter(Lease.leaseid != exclude_lease_id)

    return query.first() is not None

@leases_bp.route('/', methods=['GET'])
def get_leases():
    """
    Get a list of leases
    ---
    tags:
      - Leases
    responses:
      200:
        description: A list of leases
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
                  tenantId:
                    type: integer
                  tenantName:
                    type: string
                  propertyId:
                    type: integer
                  propertyAddress:
                    type: string
                  leaseStart:
                    type: string
                    format: date
                  leaseEnd:
                    type: string
                    format: date
                  paymentStatus:
                    type: string
    """
    leases = Lease.query.join(Tenant).join(Property).join(PaymentStatus).all()
    result = [
        {
            'id': l.leaseid,
            'tenantId': l.tenantid,
            'tenantName': l.tenant.name,
            'propertyId': l.propertyid,
            'propertyAddress': l.property.address,
            'leaseStart': l.leasetermstart.isoformat(),
            'leaseEnd': l.leasetermend.isoformat(),
            'paymentStatus': l.payment_status.description,
            'paymentStatusId': l.paymentstatusid
        } for l in leases
    ]
    return jsonify({'data': result})

@leases_bp.route('/<int:id>', methods=['GET'])
def get_lease_by_id(id):
    """
    Get a lease by its ID
    ---
    tags:
      - Leases
    parameters:
      - name: id
        in: path
        type: integer
        required: true
        description: The ID of the lease
    responses:
      200:
        description: A lease object
      404:
        description: Lease not found
    """
    lease = Lease.query.join(Tenant).join(Property).join(PaymentStatus).filter(Lease.leaseid == id).first()
    if not lease:
        return jsonify({'data': None, 'error': 'Lease not found'}), 404
    result = {
        'id': lease.leaseid,
        'tenantId': lease.tenantid,
        'tenantName': lease.tenant.name,
        'propertyId': lease.propertyid,
        'propertyAddress': lease.property.address,
        'leaseStart': lease.leasetermstart.isoformat(),
        'leaseEnd': lease.leasetermend.isoformat(),
        'paymentStatus': lease.payment_status.description,
        'paymentStatusId': lease.paymentstatusid
    }
    return jsonify({'data': result})

@leases_bp.route('/tenant/<int:tenant_id>', methods=['GET'])
def get_leases_by_tenant(tenant_id):
    """
    Get leases by tenant ID
    ---
    tags:
      - Leases
    parameters:
      - name: tenant_id
        in: path
        type: integer
        required: true
        description: The ID of the tenant
    responses:
      200:
        description: A list of leases for the tenant
    """
    leases = Lease.query.join(Property).join(PaymentStatus).filter(Lease.tenantid == tenant_id).all()
    result = [
        {
            'id': l.leaseid,
            'tenantId': l.tenantid,
            'propertyId': l.propertyid,
            'propertyAddress': l.property.address,
            'leaseStart': l.leasetermstart.isoformat(),
            'leaseEnd': l.leasetermend.isoformat(),
            'paymentStatus': l.payment_status.description,
            'paymentStatusId': l.paymentstatusid
        } for l in leases
    ]
    return jsonify({'data': result})

@leases_bp.route('/property/<int:property_id>', methods=['GET'])
def get_leases_by_property(property_id):
    """
    Get leases by property ID
    ---
    tags:
      - Leases
    parameters:
      - name: property_id
        in: path
        type: integer
        required: true
        description: The ID of the property
    responses:
      200:
        description: A list of leases for the property
    """
    leases = Lease.query.join(Tenant).join(PaymentStatus).filter(Lease.propertyid == property_id).all()
    result = [
        {
            'id': l.leaseid,
            'tenantId': l.tenantid,
            'tenantName': l.tenant.name,
            'propertyId': l.propertyid,
            'leaseStart': l.leasetermstart.isoformat(),
            'leaseEnd': l.leasetermend.isoformat(),
            'paymentStatus': l.payment_status.description,
            'paymentStatusId': l.paymentstatusid
        } for l in leases
    ]
    return jsonify({'data': result})

@leases_bp.route('/', methods=['POST'])
def create_lease():
    """
    Create a new lease
    ---
    tags:
      - Leases
    parameters:
      - name: body
        in: body
        required: true
        schema:
          type: object
          required:
            - tenantid
            - propertyid
            - leasetermstart
            - leasetermend
            - paymentstatusid
          properties:
            tenantid:
              type: integer
              example: 1
            propertyid:
              type: integer
              example: 1
            leasetermstart:
              type: string
              format: date
              example: "2024-01-01"
            leasetermend:
              type: string
              format: date
              example: "2025-01-01"
            paymentstatusid:
              type: integer
              example: 1
    responses:
      201:
        description: Lease created successfully
      400:
        description: Invalid input
    """
    data = request.json

    if not data:
        return jsonify({'data': None, 'error': 'No data provided'}), 400

    required_fields = ['tenantid', 'propertyid', 'leasetermstart', 'leasetermend', 'paymentstatusid']
    missing_fields = [field for field in required_fields if field not in data]
    if missing_fields:
        return jsonify({'data': None, 'error': f'Missing required fields: {", ".join(missing_fields)}'}), 400

    if check_lease_overlap(data['propertyid'], data['leasetermstart'], data['leasetermend']):
        return jsonify({
            'data': None,
            'error': 'Cannot create lease: property has overlapping lease for the specified dates'
        }), 409

    try:
        new_lease = Lease(
            tenantid=data['tenantid'],
            propertyid=data['propertyid'],
            leasetermstart=data['leasetermstart'],
            leasetermend=data['leasetermend'],
            paymentstatusid=data['paymentstatusid']
        )
        db.session.add(new_lease)
        db.session.commit()
        return jsonify({'data': {'id': new_lease.leaseid, 'message': 'Lease created successfully'}}), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({'data': None, 'error': f'Failed to create lease: {str(e)}'}), 400

@leases_bp.route('/<int:id>', methods=['PUT'])
def update_lease(id):
    """
    Update a lease
    ---
    tags:
      - Leases
    parameters:
      - name: id
        in: path
        type: integer
        required: true
        description: The ID of the lease
    requestBody:
      required: true
      content:
        application/json:
          schema:
            type: object
            properties:
              tenantid:
                type: integer
              propertyid:
                type: integer
              leasetermstart:
                type: string
                format: date
              leasetermend:
                type: string
                format: date
              paymentstatusid:
                type: integer
    responses:
      200:
        description: Lease updated successfully
      404:
        description: Lease not found
    """
    data = request.json
    lease = Lease.query.get(id)
    if not lease:
        return jsonify({'data': None, 'error': 'Lease not found'}), 404

    new_property_id = data.get('propertyid', lease.propertyid)
    new_start = data.get('leasetermstart', lease.leasetermstart)
    new_end = data.get('leasetermend', lease.leasetermend)

    if check_lease_overlap(new_property_id, new_start, new_end, exclude_lease_id=id):
        return jsonify({
            'data': None,
            'error': 'Cannot update lease: property has overlapping lease for the specified dates'
        }), 409

    lease.tenantid = data.get('tenantid', lease.tenantid)
    lease.propertyid = new_property_id
    lease.leasetermstart = new_start
    lease.leasetermend = new_end
    lease.paymentstatusid = data.get('paymentstatusid', lease.paymentstatusid)
    db.session.commit()
    return jsonify({'data': {'message': 'Lease updated successfully'}})

@leases_bp.route('/<int:id>', methods=['DELETE'])
def delete_lease(id):
    """
    Delete a lease
    ---
    tags:
      - Leases
    parameters:
      - name: id
        in: path
        type: integer
        required: true
        description: The ID of the lease
    responses:
      200:
        description: Lease deleted successfully
      404:
        description: Lease not found
    """
    lease = Lease.query.get(id)
    if not lease:
        return jsonify({'data': None, 'error': 'Lease not found'}), 404
    db.session.delete(lease)
    db.session.commit()
    return jsonify({'data': {'message': 'Lease deleted successfully'}})
