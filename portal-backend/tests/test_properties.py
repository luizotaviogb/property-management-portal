import pytest
import json
from app.models import Property, PropertyType, PropertyStatus

class TestPropertiesAPI:
    """Test suite for Properties API endpoints"""

    @pytest.fixture(autouse=True)
    def setup(self, db):
        """Set up test data before each test"""
        # Create property types
        residential = PropertyType(description='Residential')
        commercial = PropertyType(description='Commercial')
        db.session.add_all([residential, commercial])

        # Create property statuses
        vacant = PropertyStatus(description='Vacant')
        occupied = PropertyStatus(description='Occupied')
        db.session.add_all([vacant, occupied])

        db.session.commit()

        # Create test property
        test_property = Property(
            address='123 Test St, Paris, 75001',
            propertytypeid=1,
            propertystatusid=1,
            purchasedate='2024-01-15',
            price=500000.00
        )
        db.session.add(test_property)
        db.session.commit()

    def test_get_all_properties(self, client):
        """Test GET /properties/ returns all properties"""
        response = client.get('/properties/')
        assert response.status_code == 200
        data = json.loads(response.data)
        assert 'data' in data
        assert len(data['data']) >= 1
        assert data['data'][0]['address'] == '123 Test St, Paris, 75001'

    def test_get_property_by_id(self, client):
        """Test GET /properties/<id> returns specific property"""
        response = client.get('/properties/1')
        assert response.status_code == 200
        data = json.loads(response.data)
        assert 'data' in data
        assert data['data']['id'] == 1
        assert data['data']['address'] == '123 Test St, Paris, 75001'

    def test_get_property_by_id_not_found(self, client):
        """Test GET /properties/<id> with non-existent ID"""
        response = client.get('/properties/9999')
        assert response.status_code == 404
        data = json.loads(response.data)
        assert 'error' in data

    def test_create_property(self, client):
        """Test POST /properties/ creates new property"""
        new_property = {
            'address': '456 New Ave, Lyon, 69001',
            'typeId': 2,
            'statusId': 2,
            'purchaseDate': '2024-02-20',
            'price': 750000.00
        }
        response = client.post('/properties/',
                               data=json.dumps(new_property),
                               content_type='application/json')
        assert response.status_code == 201
        data = json.loads(response.data)
        assert 'data' in data
        assert 'id' in data['data']
        assert data['data']['message'] == 'Property created successfully'

    def test_create_property_missing_fields(self, client):
        """Test POST /properties/ with missing required fields"""
        incomplete_property = {
            'address': '789 Incomplete St'
        }
        response = client.post('/properties/',
                               data=json.dumps(incomplete_property),
                               content_type='application/json')
        assert response.status_code == 400
        data = json.loads(response.data)
        assert 'error' in data
        assert 'Missing required fields' in data['error']

    def test_update_property(self, client):
        """Test PUT /properties/<id> updates property"""
        updated_data = {
            'address': '123 Updated St, Paris, 75001',
            'price': 550000.00
        }
        response = client.put('/properties/1',
                             data=json.dumps(updated_data),
                             content_type='application/json')
        assert response.status_code == 200
        data = json.loads(response.data)
        assert 'data' in data
        assert 'message' in data['data']

    def test_update_property_not_found(self, client):
        """Test PUT /properties/<id> with non-existent ID"""
        response = client.put('/properties/9999',
                             data=json.dumps({'price': 100000}),
                             content_type='application/json')
        assert response.status_code == 404

    def test_delete_property(self, client):
        """Test DELETE /properties/<id> removes property"""
        response = client.delete('/properties/1')
        assert response.status_code == 200
        data = json.loads(response.data)
        assert 'message' in data['data']

        # Verify it's deleted
        get_response = client.get('/properties/1')
        assert get_response.status_code == 404

    def test_delete_property_not_found(self, client):
        """Test DELETE /properties/<id> with non-existent ID"""
        response = client.delete('/properties/9999')
        assert response.status_code == 404
