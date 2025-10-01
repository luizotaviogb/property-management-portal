import pytest
import json
from app.models import Maintenance, Property, PropertyType, PropertyStatus, MaintenanceStatus

class TestMaintenanceAPI:
    """Test suite for Maintenance API endpoints"""

    @pytest.fixture(autouse=True)
    def setup(self, db):
        """Set up test data before each test"""
        # Create dependencies
        property_type = PropertyType(description='Residential')
        property_status = PropertyStatus(description='Occupied')
        maintenance_status = MaintenanceStatus(description='Pending')
        db.session.add_all([property_type, property_status, maintenance_status])
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

        # Create test maintenance task
        test_maintenance = Maintenance(
            description='Fix broken window',
            maintenancestatusid=1,
            scheduleddate='2024-03-15',
            propertyid=1
        )
        db.session.add(test_maintenance)
        db.session.commit()

    def test_get_all_maintenance(self, client):
        """Test GET /maintenance/ returns all maintenance tasks"""
        response = client.get('/maintenance/')
        assert response.status_code == 200
        data = json.loads(response.data)
        assert 'data' in data
        assert len(data['data']) >= 1
        assert data['data'][0]['description'] == 'Fix broken window'

    def test_get_maintenance_by_id(self, client):
        """Test GET /maintenance/<id> returns specific task"""
        response = client.get('/maintenance/1')
        assert response.status_code == 200
        data = json.loads(response.data)
        assert 'data' in data
        assert data['data']['id'] == 1
        assert data['data']['description'] == 'Fix broken window'

    def test_get_maintenance_by_id_not_found(self, client):
        """Test GET /maintenance/<id> with non-existent ID"""
        response = client.get('/maintenance/9999')
        assert response.status_code == 404

    def test_create_maintenance(self, client):
        """Test POST /maintenance/ creates new task"""
        new_task = {
            'description': 'Replace air filter',
            'maintenancestatusid': 1,
            'scheduleddate': '2024-04-20',
            'propertyid': 1
        }
        response = client.post('/maintenance/',
                               data=json.dumps(new_task),
                               content_type='application/json')
        assert response.status_code == 201
        data = json.loads(response.data)
        assert 'data' in data
        assert 'id' in data['data']

    def test_create_maintenance_missing_fields(self, client):
        """Test POST /maintenance/ with missing required fields"""
        incomplete_task = {'description': 'Incomplete task'}
        response = client.post('/maintenance/',
                               data=json.dumps(incomplete_task),
                               content_type='application/json')
        assert response.status_code == 400
        data = json.loads(response.data)
        assert 'error' in data

    def test_update_maintenance(self, client):
        """Test PUT /maintenance/<id> updates task"""
        updated_data = {'description': 'Fix broken window - URGENT'}
        response = client.put('/maintenance/1',
                             data=json.dumps(updated_data),
                             content_type='application/json')
        assert response.status_code == 200
        data = json.loads(response.data)
        assert 'message' in data['data']

    def test_delete_maintenance(self, client):
        """Test DELETE /maintenance/<id> removes task"""
        response = client.delete('/maintenance/1')
        assert response.status_code == 200

        # Verify it's deleted
        get_response = client.get('/maintenance/1')
        assert get_response.status_code == 404
