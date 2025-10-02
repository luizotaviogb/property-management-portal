from flask import Blueprint, jsonify, request
from sqlalchemy.exc import IntegrityError
from ...models import Tenant, Lease
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
                  contactInfo:
                    type: string
    """
    tenants = Tenant.query.all()
    result = [
        {
            'id': t.tenantid,
            'name': t.name,
            'contactInfo': t.contactinfo
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
    tenant = Tenant.query.filter(Tenant.tenantid == id).first()
    if not tenant:
        return jsonify({'data': None, 'error': 'Tenant not found'}), 404
    result = {
        'id': tenant.tenantid,
        'name': tenant.name,
        'contactInfo': tenant.contactinfo
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
          properties:
            name:
              type: string
              example: "John Doe"
            contactinfo:
              type: string
              example: "+33123456789"
    responses:
      201:
        description: Tenant created successfully
      400:
        description: Invalid input
    """
    data = request.json

    if not data:
        return jsonify({'data': None, 'error': 'No data provided'}), 400

    required_fields = ['name', 'contactinfo']
    missing_fields = [field for field in required_fields if field not in data]
    if missing_fields:
        return jsonify({'data': None, 'error': f'Missing required fields: {", ".join(missing_fields)}'}), 400

    try:
        new_tenant = Tenant(
            name=data['name'],
            contactinfo=data['contactinfo']
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
      409:
        description: Cannot delete tenant due to active leases
    """
    tenant = Tenant.query.get(id)
    if not tenant:
        return jsonify({'data': None, 'error': 'Tenant not found'}), 404

    active_leases = Lease.query.filter(Lease.tenantid == id).count()
    if active_leases > 0:
        return jsonify({
            'data': None,
            'error': f'Cannot delete tenant because they have {active_leases} active lease(s). Please delete or reassign the leases first.'
        }), 409

    try:
        db.session.delete(tenant)
        db.session.commit()
        return jsonify({'data': {'message': 'Tenant deleted successfully'}})
    except IntegrityError:
        db.session.rollback()
        return jsonify({
            'data': None,
            'error': 'Cannot delete tenant due to database constraints'
        }), 409