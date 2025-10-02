# Property Management Portal

A full-stack web application for monitoring and managing property portfolios, built with Flask (Python) and Angular 18.

## Features

- **Property Management**: Track properties with details like address, type, status, purchase date, and price
- **Tenant Management**: Manage tenant information and contact details
- **Lease Management**: Handle lease agreements with automatic overlap detection
- **Maintenance Tracking**: Schedule and track maintenance tasks for properties
- **Real-time Validation**: Business logic ensures data integrity (no overlapping leases, proper date validation, etc.)

## Tech Stack

### Backend
- **Framework**: Flask (Python)
- **Database**: PostgreSQL 15
- **ORM**: SQLAlchemy
- **API Documentation**: Swagger/Flasgger
- **Testing**: Pytest

### Frontend
- **Framework**: Angular 18 (Standalone Components)
- **UI Library**: Angular Material
- **Package Manager**: Yarn
- **Testing**: Jasmine/Karma

### Infrastructure
- **Containerization**: Docker & Docker Compose
- **Database Initialization**: SQL scripts

## Architecture

### Database Schema
- **Lookup Tables**: property_types, property_statuses, maintenance_statuses, payment_statuses
- **Main Tables**: properties, tenants, leases, maintenance
- **Relationships**: Properties have many leases and maintenance tasks; Tenants have many leases

### API Endpoints

#### Properties
- `GET /properties/` - List all properties
- `GET /properties/{id}` - Get property by ID
- `POST /properties/` - Create new property
- `PUT /properties/{id}` - Update property
- `DELETE /properties/{id}` - Delete property

#### Tenants
- `GET /tenants/` - List all tenants
- `GET /tenants/{id}` - Get tenant by ID
- `POST /tenants/` - Create new tenant
- `PUT /tenants/{id}` - Update tenant
- `DELETE /tenants/{id}` - Delete tenant

#### Leases
- `GET /leases/` - List all leases
- `GET /leases/{id}` - Get lease by ID
- `GET /leases/tenant/{tenant_id}` - Get leases by tenant
- `GET /leases/property/{property_id}` - Get leases by property
- `POST /leases/` - Create new lease (validates no overlaps)
- `PUT /leases/{id}` - Update lease (validates no overlaps)
- `DELETE /leases/{id}` - Delete lease

#### Maintenance
- `GET /maintenance/` - List all maintenance tasks
- `GET /maintenance/{id}` - Get maintenance task by ID
- `POST /maintenance/` - Create new maintenance task
- `PUT /maintenance/{id}` - Update maintenance task
- `DELETE /maintenance/{id}` - Delete maintenance task

#### Status Endpoints
- `GET /property-status/` - List property statuses
- `GET /property-type/` - List property types
- `GET /payment-status/` - List payment statuses
- `GET /maintenance-status/` - List maintenance statuses

## Getting Started

### Prerequisites
- Docker & Docker Compose
- OR: Python 3.12+, Node.js 18+, PostgreSQL 15+

### Running with Docker (Recommended)

1. Clone the repository:
```bash
git clone <repository-url>
cd property-management-portal
```

2. Start all services:
```bash
docker-compose up --build
```

3. Access the application:
- Frontend: http://localhost:80
- Backend API: http://localhost:5001
- Swagger Documentation: http://localhost:5001/apidocs
- PostgreSQL: localhost:5432

### Running Locally

#### Backend Setup

1. Create and activate virtual environment:
```bash
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate
```

2. Install dependencies:
```bash
pip install -r portal-backend/requirements.txt
```

3. Set up PostgreSQL database and run initialization script:
```bash
psql -U user -d property_management -f init-db.sql
```

4. Run the backend:
```bash
cd portal-backend && python app.py
```

#### Frontend Setup

1. Install dependencies:
```bash
cd portal-frontend
yarn install
```

2. Start development server:
```bash
npm run start
```

3. Access at http://localhost:4200

## Testing

### Backend Tests
```bash
cd portal-backend
source ../.venv/bin/activate
pytest tests/ -v
```

### Frontend Tests
```bash
cd portal-frontend
npm run test
```

## Business Logic Validations

### Lease Validation
- Lease end date must be after start date
- No overlapping leases for the same property
- Cannot create lease with invalid dates

### Tenant Integrity
- Cannot delete tenant with active leases
- Contact info must be valid email or phone number

### Property Integrity
- Cannot delete property with associated leases or maintenance records
- Price must be non-negative
- Address must be non-empty

### Maintenance Validation
- Description must be non-empty
- Scheduled date must be valid

## Project Structure

```
property-management-portal/
├── portal-backend/
│   ├── app/
│   │   ├── blueprints/      # API route handlers
│   │   ├── models/          # SQLAlchemy models
│   │   ├── __init__.py      # App factory
│   │   └── db.py            # Database instance
│   ├── tests/               # Pytest test suites
│   ├── requirements.txt
│   └── Dockerfile
├── portal-frontend/
│   ├── src/
│   │   └── app/
│   │       ├── components/  # Angular components
│   │       ├── services/    # HTTP services
│   │       └── interfaces/  # TypeScript interfaces
│   ├── package.json
│   └── Dockerfile
├── init-db.sql              # Database schema
├── docker-compose.yml
└── README.md
```

## Environment Variables

Backend environment variables (set in docker-compose.yml or .env):
- `FLASK_ENV`: Environment (development/production)
- Database connection configured in `portal-backend/app/config.py`

## Contributing

1. Follow existing code structure and patterns
2. Add tests for new features
3. Ensure all tests pass before committing
4. Use meaningful commit messages

## Troubleshooting

### Database Connection Issues
- Ensure PostgreSQL is running
- Check credentials in `portal-backend/app/config.py`
- Verify database has been initialized with `init-db.sql`

### CORS Issues
- Backend has CORS enabled for all origins in development
- Configure appropriately for production

### Port Conflicts
- Backend: 5001
- Frontend: 80 (Docker) or 4200 (local)
- Database: 5432

Change ports in `docker-compose.yml` if conflicts occur.

## License

This project is for educational purposes.
