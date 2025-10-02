import { ComponentFixture, TestBed } from '@angular/core/testing';
import { MaintenanceComponent } from './maintenance.component';
import { MaintenanceService } from '../../services/maintenance.service';
import { PropertiesService } from '../../services/properties.service';
import { MaintenanceStatusService } from '../../services/maintenance-status.service';
import { MatDialog } from '@angular/material/dialog';
import { MatSnackBar } from '@angular/material/snack-bar';
import { of, throwError } from 'rxjs';
import { NoopAnimationsModule } from '@angular/platform-browser/animations';

describe('MaintenanceComponent', () => {
  let component: MaintenanceComponent;
  let fixture: ComponentFixture<MaintenanceComponent>;
  let maintenanceService: jasmine.SpyObj<MaintenanceService>;
  let propertiesService: jasmine.SpyObj<PropertiesService>;
  let maintenanceStatusService: jasmine.SpyObj<MaintenanceStatusService>;
  let dialog: jasmine.SpyObj<MatDialog>;
  let snackBar: jasmine.SpyObj<MatSnackBar>;

  const mockMaintenance = [
    {
      id: 1,
      description: 'Fix leaking roof',
      status: 'Completed',
      statusId: 1,
      scheduledDate: '2024-03-15',
      propertyId: 1
    }
  ];

  const mockProperties = [{ id: 1, address: '123 Test St', type: 'Residential', status: 'Occupied', typeId: 1, statusId: 1, purchaseDate: '2024-01-15', price: 500000 }];
  const mockMaintenanceStatuses = [{ id: 1, description: 'Completed' }];

  beforeEach(async () => {
    const maintenanceServiceSpy = jasmine.createSpyObj('MaintenanceService', ['get', 'create', 'update', 'delete']);
    const propertiesServiceSpy = jasmine.createSpyObj('PropertiesService', ['get']);
    const maintenanceStatusServiceSpy = jasmine.createSpyObj('MaintenanceStatusService', ['get']);
    const dialogSpy = jasmine.createSpyObj('MatDialog', ['open']);
    const snackBarSpy = jasmine.createSpyObj('MatSnackBar', ['open']);

    await TestBed.configureTestingModule({
      imports: [MaintenanceComponent, NoopAnimationsModule],
      providers: [
        { provide: MaintenanceService, useValue: maintenanceServiceSpy },
        { provide: PropertiesService, useValue: propertiesServiceSpy },
        { provide: MaintenanceStatusService, useValue: maintenanceStatusServiceSpy },
        { provide: MatDialog, useValue: dialogSpy },
        { provide: MatSnackBar, useValue: snackBarSpy }
      ]
    }).compileComponents();

    maintenanceService = TestBed.inject(MaintenanceService) as jasmine.SpyObj<MaintenanceService>;
    propertiesService = TestBed.inject(PropertiesService) as jasmine.SpyObj<PropertiesService>;
    maintenanceStatusService = TestBed.inject(MaintenanceStatusService) as jasmine.SpyObj<MaintenanceStatusService>;
    dialog = TestBed.inject(MatDialog) as jasmine.SpyObj<MatDialog>;
    snackBar = TestBed.inject(MatSnackBar) as jasmine.SpyObj<MatSnackBar>;

    maintenanceService.get.and.returnValue(of(mockMaintenance));
    propertiesService.get.and.returnValue(of(mockProperties));
    maintenanceStatusService.get.and.returnValue(of(mockMaintenanceStatuses));

    fixture = TestBed.createComponent(MaintenanceComponent);
    component = fixture.componentInstance;
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });

  it('should load maintenance on init', () => {
    fixture.detectChanges();
    expect(maintenanceService.get).toHaveBeenCalled();
    expect(component.dataSource.data).toEqual(mockMaintenance);
    expect(component.loading).toBe(false);
  });

  it('should load properties on init', () => {
    fixture.detectChanges();
    expect(propertiesService.get).toHaveBeenCalled();
    expect(component.properties).toEqual(mockProperties);
  });

  it('should load maintenance statuses on init', () => {
    fixture.detectChanges();
    expect(maintenanceStatusService.get).toHaveBeenCalled();
    expect(component.maintenanceStatuses).toEqual(mockMaintenanceStatuses);
  });

  it('should handle error when loading maintenance', () => {
    maintenanceService.get.and.returnValue(throwError(() => new Error('Load error')));
    fixture.detectChanges();
    expect(component.loading).toBe(false);
    expect(snackBar.open).toHaveBeenCalledWith('Error loading maintenance', 'Close', { duration: 3000 });
  });

  it('should create maintenance successfully', () => {
    const newMaintenance = { ...mockMaintenance[0], id: 2 };
    maintenanceService.create.and.returnValue(of(newMaintenance));

    component.createMaintenance(newMaintenance);

    expect(maintenanceService.create).toHaveBeenCalledWith(newMaintenance);
    expect(snackBar.open).toHaveBeenCalledWith('Maintenance created successfully', 'Close', { duration: 3000 });
  });

  it('should update maintenance successfully', () => {
    maintenanceService.update.and.returnValue(of({}));

    component.updateMaintenance(1, mockMaintenance[0]);

    expect(maintenanceService.update).toHaveBeenCalledWith(1, mockMaintenance[0]);
    expect(snackBar.open).toHaveBeenCalledWith('Maintenance updated successfully', 'Close', { duration: 3000 });
  });
});
