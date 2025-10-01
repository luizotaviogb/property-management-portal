from flask import Blueprint, jsonify, request
from ...models import Tenant, PaymentStatus, Property
from ...db import db

tenants_bp = Blueprint('tenants', __name__)

@tenants_bp.route('/', methods=['GET'])
def get_tenants():
    """
    Get a list of tenants
    ---
    tags:
      - Tenants
    responses:
      200:
        description: A list of tenants
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
                  name:
                    type: string
                  info:
                    type: string
                  leaseStart:
                    type: string
                    format: date-time
                  leaseEnd:
                    type: string
                    format: date-time
                  paymentStatus:
                    type: string
                  propertyId:
                    type: integer
    """
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
    return jsonify({'data': result})

@tenants_bp.route('/<int:id>', methods=['GET'])
def get_tenant_by_id(id):
    """
    Get a tenant by its ID
    ---
    tags:
      - Tenants
    parameters:
      - name: id
        in: path
        type: integer
        required: true
        description: The ID of the tenant
    responses:
      200:
        description: A tenant object
      404:
        description: Tenant not found
    """
    tenant = Tenant.query.join(PaymentStatus).join(Property).filter(Tenant.tenantid == id).first()
    if not tenant:
        return jsonify({'data': None, 'error': 'Tenant not found'}), 404
    result = {
        'id': tenant.tenantid,
        'name': tenant.name,
        'info': tenant.contactinfo,
        'leaseStart': tenant.leasetermstart.isoformat(),
        'leaseEnd': tenant.leasetermend.isoformat(),
        'paymentStatus': tenant.payment_status.description,
        'paymentStatusId': tenant.paymentstatusid,
        'propertyId': tenant.propertyid
    }
    return jsonify({'data': result})

@tenants_bp.route('/', methods=['POST'])
def create_tenant():
    """
    Create a new tenant
    ---
    tags:
      - Tenants
    parameters:
      - name: body
        in: body
        required: true
        schema:
          type: object
          required:
            - name
            - contactinfo
            - leasetermstart
            - leasetermend
            - paymentstatusid
            - propertyid
          properties:
            name:
              type: string
              example: "John Doe"
            contactinfo:
              type: string
              example: "+33123456789"
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
            propertyid:
              type: integer
              example: 1
    responses:
      201:
        description: Tenant created successfully
      400:
        description: Invalid input
    """
    data = request.json

    if not data:
        return jsonify({'data': None, 'error': 'No data provided'}), 400

    required_fields = ['name', 'contactinfo', 'leasetermstart', 'leasetermend', 'paymentstatusid', 'propertyid']
    missing_fields = [field for field in required_fields if field not in data]
    if missing_fields:
        return jsonify({'data': None, 'error': f'Missing required fields: {", ".join(missing_fields)}'}), 400

    try:
        new_tenant = Tenant(
            name=data['name'],
            contactinfo=data['contactinfo'],
            leasetermstart=data['leasetermstart'],
            leasetermend=data['leasetermend'],
            paymentstatusid=data['paymentstatusid'],
            propertyid=data['propertyid']
        )
        db.session.add(new_tenant)
        db.session.commit()
        return jsonify({'data': {'id': new_tenant.tenantid, 'message': 'Tenant created successfully'}}), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({'data': None, 'error': f'Failed to create tenant: {str(e)}'}), 400

@tenants_bp.route('/<int:id>', methods=['PUT'])
def update_tenant(id):
    """
    Update a tenant
    ---
    tags:
      - Tenants
    parameters:
      - name: id
        in: path
        type: integer
        required: true
        description: The ID of the tenant
    requestBody:
      required: true
      content:
        application/json:
          schema:
            type: object
            properties:
              name:
                type: string
              contactinfo:
                type: string
              leasetermstart:
                type: string
                format: date
              leasetermend:
                type: string
                format: date
              paymentstatusid:
                type: integer
              propertyid:
                type: integer
    responses:
      200:
        description: Tenant updated successfully
      404:
        description: Tenant not found
    """
    data = request.json
    tenant = Tenant.query.get(id)
    if not tenant:
        return jsonify({'data': None, 'error': 'Tenant not found'}), 404
    tenant.name = data.get('name', tenant.name)
    tenant.contactinfo = data.get('contactinfo', tenant.contactinfo)
    tenant.leasetermstart = data.get('leasetermstart', tenant.leasetermstart)
    tenant.leasetermend = data.get('leasetermend', tenant.leasetermend)
    tenant.paymentstatusid = data.get('paymentstatusid', tenant.paymentstatusid)
    tenant.propertyid = data.get('propertyid', tenant.propertyid)
    db.session.commit()
    return jsonify({'data': {'message': 'Tenant updated successfully'}})

@tenants_bp.route('/<int:id>', methods=['DELETE'])
def delete_tenant(id):
    """
    Delete a tenant
    ---
    tags:
      - Tenants
    parameters:
      - name: id
        in: path
        type: integer
        required: true
        description: The ID of the tenant
    responses:
      200:
        description: Tenant deleted successfully
      404:
        description: Tenant not found
    """
    tenant = Tenant.query.get(id)
    if not tenant:
        return jsonify({'data': None, 'error': 'Tenant not found'}), 404
    db.session.delete(tenant)
    db.session.commit()
    return jsonify({'data': {'message': 'Tenant deleted successfully'}})