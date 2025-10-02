import { ComponentFixture, TestBed } from '@angular/core/testing';
import { TenantsComponent } from './tenants.component';
import { TenantsService } from '../../services/tenants.service';
import { MatDialog } from '@angular/material/dialog';
import { MatSnackBar } from '@angular/material/snack-bar';
import { of, throwError } from 'rxjs';
import { NoopAnimationsModule } from '@angular/platform-browser/animations';

describe('TenantsComponent', () => {
  let component: TenantsComponent;
  let fixture: ComponentFixture<TenantsComponent>;
  let tenantsService: jasmine.SpyObj<TenantsService>;
  let dialog: jasmine.SpyObj<MatDialog>;
  let snackBar: jasmine.SpyObj<MatSnackBar>;

  const mockTenants = [
    {
      id: 1,
      name: 'John Doe',
      contactInfo: '+33123456789'
    }
  ];

  beforeEach(async () => {
    const tenantsServiceSpy = jasmine.createSpyObj('TenantsService', ['get', 'create', 'update', 'delete']);
    const dialogSpy = jasmine.createSpyObj('MatDialog', ['open']);
    const snackBarSpy = jasmine.createSpyObj('MatSnackBar', ['open']);

    await TestBed.configureTestingModule({
      imports: [TenantsComponent, NoopAnimationsModule],
      providers: [
        { provide: TenantsService, useValue: tenantsServiceSpy },
        { provide: MatDialog, useValue: dialogSpy },
        { provide: MatSnackBar, useValue: snackBarSpy }
      ]
    }).compileComponents();

    tenantsService = TestBed.inject(TenantsService) as jasmine.SpyObj<TenantsService>;
    dialog = TestBed.inject(MatDialog) as jasmine.SpyObj<MatDialog>;
    snackBar = TestBed.inject(MatSnackBar) as jasmine.SpyObj<MatSnackBar>;

    tenantsService.get.and.returnValue(of(mockTenants));

    fixture = TestBed.createComponent(TenantsComponent);
    component = fixture.componentInstance;
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });

  it('should load tenants on init', () => {
    fixture.detectChanges();
    expect(tenantsService.get).toHaveBeenCalled();
    expect(component.dataSource.data).toEqual(mockTenants);
    expect(component.loading).toBe(false);
  });

  it('should handle error when loading tenants', () => {
    tenantsService.get.and.returnValue(throwError(() => new Error('Load error')));
    fixture.detectChanges();
    expect(component.loading).toBe(false);
    expect(snackBar.open).toHaveBeenCalledWith('Error loading tenants', 'Close', { duration: 3000 });
  });

  it('should create tenant successfully', () => {
    const newTenant = { ...mockTenants[0], id: 2 };
    tenantsService.create.and.returnValue(of(newTenant));

    component.createTenant(newTenant);

    expect(tenantsService.create).toHaveBeenCalledWith(newTenant);
    expect(snackBar.open).toHaveBeenCalledWith('Tenant created successfully', 'Close', { duration: 3000 });
  });

  it('should handle error when creating tenant', () => {
    const newTenant = { ...mockTenants[0], id: 2 };
    tenantsService.create.and.returnValue(throwError(() => new Error('Create error')));

    component.createTenant(newTenant);

    expect(snackBar.open).toHaveBeenCalledWith('Error creating tenant', 'Close', { duration: 3000 });
  });

  it('should update tenant successfully', () => {
    tenantsService.update.and.returnValue(of({}));

    component.updateTenant(1, mockTenants[0]);

    expect(tenantsService.update).toHaveBeenCalledWith(1, mockTenants[0]);
    expect(snackBar.open).toHaveBeenCalledWith('Tenant updated successfully', 'Close', { duration: 3000 });
  });

  it('should handle error when updating tenant', () => {
    tenantsService.update.and.returnValue(throwError(() => new Error('Update error')));

    component.updateTenant(1, mockTenants[0]);

    expect(snackBar.open).toHaveBeenCalledWith('Error updating tenant', 'Close', { duration: 3000 });
  });

  it('should open create dialog', () => {
    const dialogRefMock = { afterClosed: () => of(null) };
    dialog.open.and.returnValue(dialogRefMock as any);

    component.openCreateDialog();

    expect(dialog.open).toHaveBeenCalled();
  });

  it('should open edit dialog', () => {
    const dialogRefMock = { afterClosed: () => of(null) };
    dialog.open.and.returnValue(dialogRefMock as any);

    component.openEditDialog(mockTenants[0]);

    expect(dialog.open).toHaveBeenCalled();
  });
});
