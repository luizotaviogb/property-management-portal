# Property Management Portal - Frontend

Angular 18 web application for managing properties, tenants, leases, and maintenance tasks.

## Features

- **Properties Dashboard**: View, create, update, and delete properties with type and status tracking
- **Tenants Management**: Manage tenant information and contact details
- **Leases Management**: Handle lease agreements with date validation and overlap detection
- **Maintenance Tracking**: Schedule and monitor maintenance tasks for properties
- **Responsive UI**: Material Design interface with table views and form dialogs
- **Real-time Validation**: Client-side and server-side validation for data integrity

## Tech Stack

- **Framework**: Angular 18 (Standalone Components)
- **UI Library**: Angular Material
- **Package Manager**: Yarn
- **Testing**: Jasmine/Karma
- **HTTP Client**: RxJS with Angular HttpClient
- **Build Tool**: Angular CLI

## Quick Start

### Local Development

1. **Install dependencies**:
   ```bash
   yarn install
   ```

2. **Start development server**:
   ```bash
   npm run start
   # or
   ng serve
   ```

   Navigate to `http://localhost:4200/`

3. **Ensure backend is running**:
   The frontend expects the backend API at `http://localhost:5001`

### Docker Development

```bash
# From project root directory
docker-compose up
```

The frontend will be available at `http://localhost:80`

## Available Scripts

### Development
```bash
npm run start       # Start dev server on localhost:4200
ng serve           # Same as npm run start
```

### Build
```bash
npm run build      # Build for production
ng build          # Same as npm run build
```

Build artifacts will be stored in `dist/portal-frontend/browser/`

### Testing
```bash
npm run test       # Run unit tests via Karma
ng test           # Same as npm run test
```

### Code Generation
```bash
ng generate component component-name    # Generate new component
ng generate service service-name        # Generate new service
ng generate interface interface-name    # Generate new interface
```

## Project Structure

```
portal-frontend/
├── src/
│   ├── app/
│   │   ├── components/          # UI Components
│   │   │   ├── main/           # Main tabbed layout
│   │   │   ├── properties/     # Properties table & forms
│   │   │   ├── tenants/        # Tenants table & forms
│   │   │   ├── leases/         # Leases table & forms
│   │   │   └── maintenance/    # Maintenance table & forms
│   │   ├── services/           # HTTP Services
│   │   │   ├── properties.service.ts
│   │   │   ├── tenants.service.ts
│   │   │   ├── leases.service.ts
│   │   │   ├── maintenance.service.ts
│   │   │   └── *-status.service.ts
│   │   ├── interfaces/         # TypeScript Interfaces
│   │   │   ├── property.ts
│   │   │   ├── tenant.ts
│   │   │   ├── lease.ts
│   │   │   └── maintenance.ts
│   │   └── app.component.ts    # Root component
│   ├── environments/           # Environment configs
│   └── assets/                 # Static assets
├── angular.json               # Angular CLI config
├── package.json              # Dependencies
└── tsconfig.json            # TypeScript config
```

## Architecture

### Components
- **Standalone Components**: Uses Angular 18 standalone component pattern (no NgModule)
- **Material Design**: All components use Angular Material for consistent UI
- **Tab-based Layout**: Main component provides tabbed navigation

### Services
- **HTTP Communication**: Each service handles API calls for its domain
- **Observable Pattern**: Uses RxJS observables for async operations
- **Error Handling**: Centralized error handling in services

### Interfaces
TypeScript interfaces mirror backend models:
- `Property`: Address, type, status, purchase info
- `Tenant`: Name, contact information
- `Lease`: Property-tenant relationship with dates
- `Maintenance`: Task description, status, dates

## API Integration

The frontend communicates with the Flask backend API:

**API Base URL**: Configured in `src/environments/environment.ts`
```typescript
export const environment = {
  production: false,
  apiUrl: 'http://localhost:5001'
};
```

### Response Format
All API endpoints return data in this structure:
```typescript
{
  data: T | T[]  // Actual response data
}
```

Services use `.pipe(map())` to extract data from responses.

## Development Notes

- **Standalone Components**: Import CommonModule, FormsModule, and Material modules directly in component decorators
- **Reactive Forms**: Consider migrating from template-driven to reactive forms for better validation
- **State Management**: Currently uses component state; consider NgRx for complex state needs
- **Type Safety**: All API calls use TypeScript interfaces for type checking

## Environment Configuration

### Development (`src/environments/environment.ts`)
```typescript
apiUrl: 'http://localhost:5001'
```

### Production (`src/environments/environment.prod.ts`)
Update `apiUrl` to production backend URL before deployment

## Testing

### Unit Tests
- Located alongside component/service files (*.spec.ts)
- Use Jasmine for test structure
- Run via Karma test runner

### Test Coverage
```bash
ng test --code-coverage
```

Coverage report will be in `coverage/portal-frontend/`

## Build for Production

```bash
npm run build
```

Production build optimizations:
- AOT compilation
- Minification
- Tree shaking
- Bundle optimization

## License

This project is for evaluation purposes.
