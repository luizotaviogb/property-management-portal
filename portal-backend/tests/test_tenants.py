import pytest
import json
from app.models import Tenant, Property, PropertyType, PropertyStatus, PaymentStatus

class TestTenantsAPI:
    """Test suite for Tenants API endpoints"""

    @pytest.fixture(autouse=True)
    def setup(self, db):
        """Set up test data before each test"""
        # Create dependencies
        property_type = PropertyType(description='Residential')
        property_status = PropertyStatus(description='Occupied')
        payment_status = PaymentStatus(description='Paid')
        db.session.add_all([property_type, property_status, payment_status])
        db.session.commit()

        # Create test property
        test_property = Property(
            address='123 Test St',
            propertytypeid=1,
            propertystatusid=1,
            purchasedate='2024-01-15',
            price=500000.00
        )
        db.session.add(test_property)
        db.session.commit()

        # Create test tenant
        test_tenant = Tenant(
            name='John Doe',
            contactinfo='+33123456789',
            leasetermstart='2024-01-01',
            leasetermend='2025-01-01',
            paymentstatusid=1,
            propertyid=1
        )
        db.session.add(test_tenant)
        db.session.commit()

    def test_get_all_tenants(self, client):
        """Test GET /tenants/ returns all tenants"""
        response = client.get('/tenants/')
        assert response.status_code == 200
        data = json.loads(response.data)
        assert 'data' in data
        assert len(data['data']) >= 1
        assert data['data'][0]['name'] == 'John Doe'

    def test_get_tenant_by_id(self, client):
        """Test GET /tenants/<id> returns specific tenant"""
        response = client.get('/tenants/1')
        assert response.status_code == 200
        data = json.loads(response.data)
        assert 'data' in data
        assert data['data']['id'] == 1
        assert data['data']['name'] == 'John Doe'

    def test_get_tenant_by_id_not_found(self, client):
        """Test GET /tenants/<id> with non-existent ID"""
        response = client.get('/tenants/9999')
        assert response.status_code == 404

    def test_create_tenant(self, client):
        """Test POST /tenants/ creates new tenant"""
        new_tenant = {
            'name': 'Jane Smith',
            'contactinfo': '+33987654321',
            'leasetermstart': '2024-03-01',
            'leasetermend': '2025-03-01',
            'paymentstatusid': 1,
            'propertyid': 1
        }
        response = client.post('/tenants/',
                               data=json.dumps(new_tenant),
                               content_type='application/json')
        assert response.status_code == 201
        data = json.loads(response.data)
        assert 'data' in data
        assert 'id' in data['data']

    def test_create_tenant_missing_fields(self, client):
        """Test POST /tenants/ with missing required fields"""
        incomplete_tenant = {'name': 'Incomplete Tenant'}
        response = client.post('/tenants/',
                               data=json.dumps(incomplete_tenant),
                               content_type='application/json')
        assert response.status_code == 400
        data = json.loads(response.data)
        assert 'error' in data

    def test_update_tenant(self, client):
        """Test PUT /tenants/<id> updates tenant"""
        updated_data = {'name': 'John Updated'}
        response = client.put('/tenants/1',
                             data=json.dumps(updated_data),
                             content_type='application/json')
        assert response.status_code == 200
        data = json.loads(response.data)
        assert 'message' in data['data']

    def test_delete_tenant(self, client):
        """Test DELETE /tenants/<id> removes tenant"""
        response = client.delete('/tenants/1')
        assert response.status_code == 200

        # Verify it's deleted
        get_response = client.get('/tenants/1')
        assert get_response.status_code == 404
