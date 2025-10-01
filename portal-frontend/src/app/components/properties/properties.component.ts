import { Component, OnInit, ViewChild, AfterViewInit } from '@angular/core';
import { CommonModule } from '@angular/common';
import { PropertiesService } from '../../services/properties.service';
import { PropertyTypeService } from '../../services/property-type.service';
import { PropertyStatusService } from '../../services/property-status.service';
import { IProperty } from '../../interfaces/properties';
import { IPropertyType } from '../../interfaces/propertyType';
import { IPropertyStatus } from '../../interfaces/propertyStatus';
import { MatTableModule, MatTableDataSource } from '@angular/material/table';
import { MatButtonModule } from '@angular/material/button';
import { MatIconModule } from '@angular/material/icon';
import { MatDialog, MatDialogModule } from '@angular/material/dialog';
import { MatSnackBar, MatSnackBarModule } from '@angular/material/snack-bar';
import { MatProgressSpinnerModule } from '@angular/material/progress-spinner';
import { MatPaginator, MatPaginatorModule } from '@angular/material/paginator';
import { MatSort, MatSortModule } from '@angular/material/sort';
import { MatChipsModule } from '@angular/material/chips';
import { MatTooltipModule } from '@angular/material/tooltip';
import { MatCardModule } from '@angular/material/card';
import { PropertyDialogComponent } from './property-dialog/property-dialog.component';

@Component({
  selector: 'app-properties',
  standalone: true,
  imports: [
    CommonModule,
    MatTableModule,
    MatButtonModule,
    MatIconModule,
    MatDialogModule,
    MatSnackBarModule,
    MatProgressSpinnerModule,
    MatPaginatorModule,
    MatSortModule,
    MatChipsModule,
    MatTooltipModule,
    MatCardModule
  ],
  templateUrl: './properties.component.html',
  styleUrls: ['./properties.component.scss']
})
export class PropertiesComponent implements OnInit, AfterViewInit {
  dataSource = new MatTableDataSource<IProperty>([]);
  displayedColumns: string[] = ['id', 'address', 'type', 'status', 'purchaseDate', 'price', 'actions'];
  loading = false;
  propertyTypes: IPropertyType[] = [];
  propertyStatuses: IPropertyStatus[] = [];

  @ViewChild(MatPaginator) paginator!: MatPaginator;
  @ViewChild(MatSort) sort!: MatSort;

  constructor(
    private propertiesService: PropertiesService,
    private propertyTypeService: PropertyTypeService,
    private propertyStatusService: PropertyStatusService,
    private dialog: MatDialog,
    private snackBar: MatSnackBar
  ) {}

  ngOnInit(): void {
    this.loadProperties();
    this.loadPropertyTypes();
    this.loadPropertyStatuses();
  }

  ngAfterViewInit(): void {
    this.dataSource.paginator = this.paginator;
    this.dataSource.sort = this.sort;
  }

  loadProperties(): void {
    this.loading = true;
    this.propertiesService.get().subscribe({
      next: (data) => {
        this.dataSource.data = data;
        this.loading = false;
      },
      error: (error) => {
        console.error('Error loading properties:', error);
        this.snackBar.open('Error loading properties', 'Close', { duration: 3000 });
        this.loading = false;
      }
    });
  }

  loadPropertyTypes(): void {
    this.propertyTypeService.get().subscribe({
      next: (data) => {
        this.propertyTypes = data;
      },
      error: (error) => {
        console.error('Error loading property types:', error);
      }
    });
  }

  loadPropertyStatuses(): void {
    this.propertyStatusService.get().subscribe({
      next: (data) => {
        this.propertyStatuses = data;
      },
      error: (error) => {
        console.error('Error loading property statuses:', error);
      }
    });
  }

  openCreateDialog(): void {
    const dialogRef = this.dialog.open(PropertyDialogComponent, {
      width: '600px',
      data: {
        property: null,
        propertyTypes: this.propertyTypes,
        propertyStatuses: this.propertyStatuses
      }
    });

    dialogRef.afterClosed().subscribe(result => {
      if (result) {
        this.createProperty(result);
      }
    });
  }

  openEditDialog(property: IProperty): void {
    const dialogRef = this.dialog.open(PropertyDialogComponent, {
      width: '600px',
      data: {
        property: { ...property },
        propertyTypes: this.propertyTypes,
        propertyStatuses: this.propertyStatuses
      }
    });

    dialogRef.afterClosed().subscribe(result => {
      if (result && property.id) {
        this.updateProperty(property.id, result);
      }
    });
  }

  createProperty(property: IProperty): void {
    this.propertiesService.create(property).subscribe({
      next: () => {
        this.snackBar.open('Property created successfully', 'Close', { duration: 3000 });
        this.loadProperties();
      },
      error: (error) => {
        console.error('Error creating property:', error);
        this.snackBar.open('Error creating property', 'Close', { duration: 3000 });
      }
    });
  }

  updateProperty(id: number, property: IProperty): void {
    this.propertiesService.update(id, property).subscribe({
      next: () => {
        this.snackBar.open('Property updated successfully', 'Close', { duration: 3000 });
        this.loadProperties();
      },
      error: (error) => {
        console.error('Error updating property:', error);
        this.snackBar.open('Error updating property', 'Close', { duration: 3000 });
      }
    });
  }

  deleteProperty(property: IProperty): void {
    if (confirm(`Are you sure you want to delete property at ${property.address}?`)) {
      if (property.id) {
        this.propertiesService.delete(property.id).subscribe({
          next: () => {
            this.snackBar.open('Property deleted successfully', 'Close', { duration: 3000 });
            this.loadProperties();
          },
          error: (error) => {
            console.error('Error deleting property:', error);
            this.snackBar.open('Error deleting property', 'Close', { duration: 3000 });
          }
        });
      }
    }
  }
}