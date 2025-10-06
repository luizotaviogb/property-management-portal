# Property Management Portal

A full-stack web application for monitoring and managing property portfolios, built with Flask (Python) and Angular 18.

## Prerequisites

- Docker
- Docker Compose

## How to Run

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
- **Frontend**: http://localhost:80
- **Backend API**: http://localhost:5001
- **API Documentation**: http://localhost:5001/apidocs
- **Database**: localhost:5432

## Stopping the Application

```bash
docker-compose down
```

To stop and remove all volumes (database data):
```bash
docker-compose down -v
```
