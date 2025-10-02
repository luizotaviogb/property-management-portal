import { ComponentFixture, TestBed } from '@angular/core/testing';
import { PropertiesComponent } from './properties.component';
import { PropertiesService } from '../../services/properties.service';
import { PropertyTypeService } from '../../services/property-type.service';
import { PropertyStatusService } from '../../services/property-status.service';
import { MatDialog } from '@angular/material/dialog';
import { MatSnackBar } from '@angular/material/snack-bar';
import { of, throwError } from 'rxjs';
import { NoopAnimationsModule } from '@angular/platform-browser/animations';

describe('PropertiesComponent', () => {
  let component: PropertiesComponent;
  let fixture: ComponentFixture<PropertiesComponent>;
  let propertiesService: jasmine.SpyObj<PropertiesService>;
  let propertyTypeService: jasmine.SpyObj<PropertyTypeService>;
  let propertyStatusService: jasmine.SpyObj<PropertyStatusService>;
  let dialog: jasmine.SpyObj<MatDialog>;
  let snackBar: jasmine.SpyObj<MatSnackBar>;

  const mockProperties = [
    {
      id: 1,
      address: '123 Test St',
      type: 'Residential',
      status: 'Vacant',
      typeId: 1,
      statusId: 1,
      purchaseDate: '2024-01-15',
      price: 500000
    }
  ];

  const mockPropertyTypes = [
    { id: 1, description: 'Residential' },
    { id: 2, description: 'Commercial' }
  ];

  const mockPropertyStatuses = [
    { id: 1, description: 'Vacant' },
    { id: 2, description: 'Occupied' }
  ];

  beforeEach(async () => {
    const propertiesServiceSpy = jasmine.createSpyObj('PropertiesService', ['get', 'create', 'update', 'delete']);
    const propertyTypeServiceSpy = jasmine.createSpyObj('PropertyTypeService', ['get']);
    const propertyStatusServiceSpy = jasmine.createSpyObj('PropertyStatusService', ['get']);
    const dialogSpy = jasmine.createSpyObj('MatDialog', ['open']);
    const snackBarSpy = jasmine.createSpyObj('MatSnackBar', ['open']);

    await TestBed.configureTestingModule({
      imports: [PropertiesComponent, NoopAnimationsModule],
      providers: [
        { provide: PropertiesService, useValue: propertiesServiceSpy },
        { provide: PropertyTypeService, useValue: propertyTypeServiceSpy },
        { provide: PropertyStatusService, useValue: propertyStatusServiceSpy },
        { provide: MatDialog, useValue: dialogSpy },
        { provide: MatSnackBar, useValue: snackBarSpy }
      ]
    }).compileComponents();

    propertiesService = TestBed.inject(PropertiesService) as jasmine.SpyObj<PropertiesService>;
    propertyTypeService = TestBed.inject(PropertyTypeService) as jasmine.SpyObj<PropertyTypeService>;
    propertyStatusService = TestBed.inject(PropertyStatusService) as jasmine.SpyObj<PropertyStatusService>;
    dialog = TestBed.inject(MatDialog) as jasmine.SpyObj<MatDialog>;
    snackBar = TestBed.inject(MatSnackBar) as jasmine.SpyObj<MatSnackBar>;

    propertiesService.get.and.returnValue(of(mockProperties));
    propertyTypeService.get.and.returnValue(of(mockPropertyTypes));
    propertyStatusService.get.and.returnValue(of(mockPropertyStatuses));

    fixture = TestBed.createComponent(PropertiesComponent);
    component = fixture.componentInstance;
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });

  it('should load properties on init', () => {
    fixture.detectChanges();
    expect(propertiesService.get).toHaveBeenCalled();
    expect(component.dataSource.data).toEqual(mockProperties);
    expect(component.loading).toBe(false);
  });

  it('should load property types on init', () => {
    fixture.detectChanges();
    expect(propertyTypeService.get).toHaveBeenCalled();
    expect(component.propertyTypes).toEqual(mockPropertyTypes);
  });

  it('should load property statuses on init', () => {
    fixture.detectChanges();
    expect(propertyStatusService.get).toHaveBeenCalled();
    expect(component.propertyStatuses).toEqual(mockPropertyStatuses);
  });

  it('should handle error when loading properties', () => {
    propertiesService.get.and.returnValue(throwError(() => new Error('Load error')));
    fixture.detectChanges();
    expect(component.loading).toBe(false);
    expect(snackBar.open).toHaveBeenCalledWith('Error loading properties', 'Close', { duration: 3000 });
  });

  it('should create property successfully', () => {
    const newProperty = { ...mockProperties[0], id: 2 };
    propertiesService.create.and.returnValue(of(newProperty));

    component.createProperty(newProperty);

    expect(propertiesService.create).toHaveBeenCalledWith(newProperty);
    expect(snackBar.open).toHaveBeenCalledWith('Property created successfully', 'Close', { duration: 3000 });
  });

  it('should handle error when creating property', () => {
    const newProperty = { ...mockProperties[0], id: 2 };
    propertiesService.create.and.returnValue(throwError(() => new Error('Create error')));

    component.createProperty(newProperty);

    expect(snackBar.open).toHaveBeenCalledWith('Error creating property', 'Close', { duration: 3000 });
  });

  it('should update property successfully', () => {
    propertiesService.update.and.returnValue(of({}));

    component.updateProperty(1, mockProperties[0]);

    expect(propertiesService.update).toHaveBeenCalledWith(1, mockProperties[0]);
    expect(snackBar.open).toHaveBeenCalledWith('Property updated successfully', 'Close', { duration: 3000 });
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

    component.openEditDialog(mockProperties[0]);

    expect(dialog.open).toHaveBeenCalled();
  });
});
