# Property Management Portal - Backend

A Flask REST API for managing properties, tenants, and maintenance tasks.

## Features

- **Properties Management**: CRUD operations for properties with types and statuses
- **Tenants Management**: Track tenants with lease information and payment status
- **Maintenance Tracking**: Schedule and monitor maintenance tasks
- **Lookup Tables**: Property types, property statuses, payment statuses, maintenance statuses
- **API Documentation**: Interactive Swagger/Flasgger documentation
- **Input Validation**: Comprehensive validation with error handling
- **Environment Configuration**: Secure credential management via environment variables

## Tech Stack

- **Framework**: Flask 2.3+
- **Database**: PostgreSQL 15 with SQLAlchemy ORM
- **Testing**: pytest with Flask integration
- **Documentation**: Flasgger (Swagger UI)
- **CORS**: Flask-CORS for cross-origin requests

## Quick Start

### Local Development

1. **Create and activate virtual environment**:
   ```bash
   python -m venv .venv
   source .venv/bin/activate  # On Windows: .venv\Scripts\activate
   ```

2. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

3. **Set environment variables** (optional, defaults provided):
   ```bash
   export DATABASE_URL='postgresql://user:password@localhost:5432/property_management'
   export DB_NAME='property_management'
   export DB_USER='user'
   export DB_PASSWORD='password'
   export DB_HOST='localhost'
   export DB_PORT='5432'
   export PORT='5001'
   ```

4. **Run the application**:
   ```bash
   python app.py
   ```

   The API will be available at `http://localhost:5001`

### Docker Development

```bash
# From project root directory
docker-compose up
```

The backend will be available at `http://localhost:5001`

## API Documentation

Once the application is running, visit:
- **Swagger UI**: http://localhost:5001/apidocs/

## API Endpoints

### Properties
- `GET /properties/` - List all properties
- `GET /properties/<id>` - Get property by ID
- `POST /properties/` - Create new property
- `PUT /properties/<id>` - Update property
- `DELETE /properties/<id>` - Delete property

### Tenants
- `GET /tenants/` - List all tenants
- `GET /tenants/<id>` - Get tenant by ID
- `POST /tenants/` - Create new tenant
- `PUT /tenants/<id>` - Update tenant
- `DELETE /tenants/<id>` - Delete tenant

### Maintenance
- `GET /maintenance/` - List all maintenance tasks
- `GET /maintenance/<id>` - Get task by ID
- `POST /maintenance/` - Create new task
- `PUT /maintenance/<id>` - Update task
- `DELETE /maintenance/<id>` - Delete task

### Lookup Tables
- `/property_status/` - Property statuses (Vacant, Occupied, etc.)
- `/payment_status/` - Payment statuses (Paid, Pending, Overdue)
- `/maintenance_status/` - Maintenance statuses (Completed, In Progress, Pending)
- `/property_type/` - Property types (Residential, Commercial, etc.)

All lookup endpoints support GET (list/by-id), POST, PUT, DELETE operations.

## Testing

### Run all tests:
```bash
pytest
```

### Run specific test file:
```bash
pytest tests/test_properties.py
```

### Run with coverage:
```bash
pytest --cov=app tests/
```

### Run specific test:
```bash
pytest tests/test_properties.py::TestPropertiesAPI::test_create_property
```

## Project Structure

```
portal-backend/
├── app/
│   ├── __init__.py          # Flask app factory
│   ├── config.py            # Configuration with env vars
│   ├── db.py                # Database instance
│   ├── blueprints/          # API routes organized by resource
│   │   ├── properties/
│   │   ├── tenants/
│   │   ├── maintenance/
│   │   └── status/
│   └── models/              # SQLAlchemy models
│       ├── property.py
│       ├── tenant.py
│       ├── maintenance.py
│       └── ...
├── tests/                   # pytest test suite
│   ├── conftest.py         # Test fixtures
│   ├── test_properties.py
│   ├── test_tenants.py
│   └── test_maintenance.py
├── app.py                   # Application entry point
├── requirements.txt         # Python dependencies
├── pytest.ini              # pytest configuration
└── Dockerfile              # Docker configuration
```

## Response Format

All endpoints return JSON with a consistent structure:

**Success**:
```json
{
  "data": { /* response data */ }
}
```

**Error**:
```json
{
  "data": null,
  "error": "Error message"
}
```

## Development Notes

- All model attributes use lowercase snake_case (e.g., `propertyid`, `leasetermstart`)
- Foreign key validations are handled by database constraints
- Date fields use ISO format (YYYY-MM-DD)
- All database operations are wrapped in try-except for error handling
- Database sessions are rolled back on errors

## Environment Variables

| Variable | Default | Description |
|----------|---------|-------------|
| `DATABASE_URL` | `postgresql://user:password@db:5432/property_management` | Full database connection string |
| `DB_NAME` | `property_management` | Database name |
| `DB_USER` | `user` | Database user |
| `DB_PASSWORD` | `password` | Database password |
| `DB_HOST` | `db` | Database host |
| `DB_PORT` | `5432` | Database port |
| `PORT` | `5001` | Application port |
| `FLASK_ENV` | `production` | Flask environment |

## License

This project is for evaluation purposes.
