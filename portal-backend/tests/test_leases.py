import pytest
import json
from app.models import Lease, Tenant, Property, PropertyType, PropertyStatus, PaymentStatus

class TestLeasesAPI:
    """Test suite for Leases API endpoints"""

    @pytest.fixture(autouse=True)
    def setup(self, db):
        """Set up test data before each test"""
        property_type = PropertyType(description='Residential')
        property_status = PropertyStatus(description='Occupied')
        payment_status_paid = PaymentStatus(description='Paid')
        payment_status_pending = PaymentStatus(description='Pending')
        db.session.add_all([property_type, property_status, payment_status_paid, payment_status_pending])
        db.session.commit()

        test_property = Property(
            address='123 Test St, Paris, 75001',
            propertytypeid=1,
            propertystatusid=1,
            purchasedate='2024-01-15',
            price=500000.00
        )
        db.session.add(test_property)
        db.session.commit()

        test_tenant = Tenant(
            name='John Doe',
            contactinfo='+33123456789'
        )
        db.session.add(test_tenant)
        db.session.commit()

        test_lease = Lease(
            tenantid=1,
            propertyid=1,
            leasetermstart='2024-01-01',
            leasetermend='2025-01-01',
            paymentstatusid=1
        )
        db.session.add(test_lease)
        db.session.commit()

    def test_get_all_leases(self, client):
        """Test GET /leases/ returns all leases"""
        response = client.get('/leases/')
        assert response.status_code == 200
        data = json.loads(response.data)
        assert 'data' in data
        assert len(data['data']) >= 1
        assert data['data'][0]['tenantName'] == 'John Doe'
        assert data['data'][0]['propertyAddress'] == '123 Test St, Paris, 75001'

    def test_get_lease_by_id(self, client):
        """Test GET /leases/<id> returns specific lease"""
        response = client.get('/leases/1')
        assert response.status_code == 200
        data = json.loads(response.data)
        assert 'data' in data
        assert data['data']['id'] == 1
        assert data['data']['tenantName'] == 'John Doe'
        assert data['data']['propertyAddress'] == '123 Test St, Paris, 75001'

    def test_get_lease_by_id_not_found(self, client):
        """Test GET /leases/<id> with non-existent ID"""
        response = client.get('/leases/9999')
        assert response.status_code == 404
        data = json.loads(response.data)
        assert 'error' in data

    def test_get_leases_by_tenant(self, client):
        """Test GET /leases/tenant/<tenant_id> returns leases for specific tenant"""
        response = client.get('/leases/tenant/1')
        assert response.status_code == 200
        data = json.loads(response.data)
        assert 'data' in data
        assert len(data['data']) >= 1
        assert data['data'][0]['tenantId'] == 1

    def test_get_leases_by_property(self, client):
        """Test GET /leases/property/<property_id> returns leases for specific property"""
        response = client.get('/leases/property/1')
        assert response.status_code == 200
        data = json.loads(response.data)
        assert 'data' in data
        assert len(data['data']) >= 1
        assert data['data'][0]['propertyId'] == 1

    def test_create_lease(self, client):
        """Test POST /leases/ creates new lease"""
        new_lease = {
            'tenantid': 1,
            'propertyid': 1,
            'leasetermstart': '2025-01-01',
            'leasetermend': '2026-01-01',
            'paymentstatusid': 2
        }
        response = client.post('/leases/',
                               data=json.dumps(new_lease),
                               content_type='application/json')
        assert response.status_code == 201
        data = json.loads(response.data)
        assert 'data' in data
        assert 'id' in data['data']
        assert data['data']['message'] == 'Lease created successfully'

    def test_create_lease_missing_fields(self, client):
        """Test POST /leases/ with missing required fields"""
        incomplete_lease = {
            'tenantid': 1,
            'propertyid': 1
        }
        response = client.post('/leases/',
                               data=json.dumps(incomplete_lease),
                               content_type='application/json')
        assert response.status_code == 400
        data = json.loads(response.data)
        assert 'error' in data
        assert 'Missing required fields' in data['error']

    def test_create_lease_no_data(self, client):
        """Test POST /leases/ with no data"""
        response = client.post('/leases/',
                               data=json.dumps({}),
                               content_type='application/json')
        assert response.status_code == 400

    def test_update_lease(self, client):
        """Test PUT /leases/<id> updates lease"""
        updated_data = {
            'leasetermend': '2025-06-01',
            'paymentstatusid': 2
        }
        response = client.put('/leases/1',
                             data=json.dumps(updated_data),
                             content_type='application/json')
        assert response.status_code == 200
        data = json.loads(response.data)
        assert 'data' in data
        assert 'message' in data['data']

    def test_update_lease_not_found(self, client):
        """Test PUT /leases/<id> with non-existent ID"""
        response = client.put('/leases/9999',
                             data=json.dumps({'paymentstatusid': 2}),
                             content_type='application/json')
        assert response.status_code == 404

    def test_delete_lease(self, client):
        """Test DELETE /leases/<id> removes lease"""
        response = client.delete('/leases/1')
        assert response.status_code == 200
        data = json.loads(response.data)
        assert 'message' in data['data']

        get_response = client.get('/leases/1')
        assert get_response.status_code == 404

    def test_delete_lease_not_found(self, client):
        """Test DELETE /leases/<id> with non-existent ID"""
        response = client.delete('/leases/9999')
        assert response.status_code == 404
