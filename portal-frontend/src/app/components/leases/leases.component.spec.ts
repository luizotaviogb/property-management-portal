import { ComponentFixture, TestBed } from '@angular/core/testing';
import { LeasesComponent } from './leases.component';
import { LeasesService } from '../../services/leases.service';
import { TenantsService } from '../../services/tenants.service';
import { PropertiesService } from '../../services/properties.service';
import { PaymentStatusService } from '../../services/payment-status.service';
import { MatDialog } from '@angular/material/dialog';
import { MatSnackBar } from '@angular/material/snack-bar';
import { of, throwError } from 'rxjs';
import { NoopAnimationsModule } from '@angular/platform-browser/animations';

describe('LeasesComponent', () => {
  let component: LeasesComponent;
  let fixture: ComponentFixture<LeasesComponent>;
  let leasesService: jasmine.SpyObj<LeasesService>;
  let tenantsService: jasmine.SpyObj<TenantsService>;
  let propertiesService: jasmine.SpyObj<PropertiesService>;
  let paymentStatusService: jasmine.SpyObj<PaymentStatusService>;
  let dialog: jasmine.SpyObj<MatDialog>;
  let snackBar: jasmine.SpyObj<MatSnackBar>;

  const mockLeases = [
    {
      id: 1,
      tenantId: 1,
      tenantName: 'John Doe',
      propertyId: 1,
      propertyAddress: '123 Test St',
      leaseStart: '2024-01-01',
      leaseEnd: '2025-01-01',
      paymentStatus: 'Paid',
      paymentStatusId: 1
    }
  ];

  const mockTenants = [{ id: 1, name: 'John Doe', contactInfo: '+33123456789' }];
  const mockProperties = [{ id: 1, address: '123 Test St', type: 'Residential', status: 'Occupied', typeId: 1, statusId: 1, purchaseDate: '2024-01-15', price: 500000 }];
  const mockPaymentStatuses = [{ id: 1, description: 'Paid' }];

  beforeEach(async () => {
    const leasesServiceSpy = jasmine.createSpyObj('LeasesService', ['get', 'create', 'update', 'delete']);
    const tenantsServiceSpy = jasmine.createSpyObj('TenantsService', ['get']);
    const propertiesServiceSpy = jasmine.createSpyObj('PropertiesService', ['get']);
    const paymentStatusServiceSpy = jasmine.createSpyObj('PaymentStatusService', ['get']);
    const dialogSpy = jasmine.createSpyObj('MatDialog', ['open']);
    const snackBarSpy = jasmine.createSpyObj('MatSnackBar', ['open']);

    await TestBed.configureTestingModule({
      imports: [LeasesComponent, NoopAnimationsModule],
      providers: [
        { provide: LeasesService, useValue: leasesServiceSpy },
        { provide: TenantsService, useValue: tenantsServiceSpy },
        { provide: PropertiesService, useValue: propertiesServiceSpy },
        { provide: PaymentStatusService, useValue: paymentStatusServiceSpy },
        { provide: MatDialog, useValue: dialogSpy },
        { provide: MatSnackBar, useValue: snackBarSpy }
      ]
    }).compileComponents();

    leasesService = TestBed.inject(LeasesService) as jasmine.SpyObj<LeasesService>;
    tenantsService = TestBed.inject(TenantsService) as jasmine.SpyObj<TenantsService>;
    propertiesService = TestBed.inject(PropertiesService) as jasmine.SpyObj<PropertiesService>;
    paymentStatusService = TestBed.inject(PaymentStatusService) as jasmine.SpyObj<PaymentStatusService>;
    dialog = TestBed.inject(MatDialog) as jasmine.SpyObj<MatDialog>;
    snackBar = TestBed.inject(MatSnackBar) as jasmine.SpyObj<MatSnackBar>;

    leasesService.get.and.returnValue(of(mockLeases));
    tenantsService.get.and.returnValue(of(mockTenants));
    propertiesService.get.and.returnValue(of(mockProperties));
    paymentStatusService.get.and.returnValue(of(mockPaymentStatuses));

    fixture = TestBed.createComponent(LeasesComponent);
    component = fixture.componentInstance;
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });

  it('should load leases on init', () => {
    fixture.detectChanges();
    expect(leasesService.get).toHaveBeenCalled();
    expect(component.dataSource.data).toEqual(mockLeases);
    expect(component.loading).toBe(false);
  });

  it('should load tenants on init', () => {
    fixture.detectChanges();
    expect(tenantsService.get).toHaveBeenCalled();
    expect(component.tenants).toEqual(mockTenants);
  });

  it('should load properties on init', () => {
    fixture.detectChanges();
    expect(propertiesService.get).toHaveBeenCalled();
    expect(component.properties).toEqual(mockProperties);
  });

  it('should load payment statuses on init', () => {
    fixture.detectChanges();
    expect(paymentStatusService.get).toHaveBeenCalled();
    expect(component.paymentStatuses).toEqual(mockPaymentStatuses);
  });

  it('should handle error when loading leases', () => {
    leasesService.get.and.returnValue(throwError(() => new Error('Load error')));
    fixture.detectChanges();
    expect(component.loading).toBe(false);
    expect(snackBar.open).toHaveBeenCalledWith('Error loading leases', 'Close', { duration: 3000 });
  });

  it('should create lease successfully', () => {
    const newLease = { ...mockLeases[0], id: 2 };
    leasesService.create.and.returnValue(of(newLease));

    component.createLease(newLease);

    expect(leasesService.create).toHaveBeenCalledWith(newLease);
    expect(snackBar.open).toHaveBeenCalledWith('Lease created successfully', 'Close', { duration: 3000 });
  });

  it('should update lease successfully', () => {
    leasesService.update.and.returnValue(of({}));

    component.updateLease(1, mockLeases[0]);

    expect(leasesService.update).toHaveBeenCalledWith(1, mockLeases[0]);
    expect(snackBar.open).toHaveBeenCalledWith('Lease updated successfully', 'Close', { duration: 3000 });
  });
});
