import { Component, OnInit, ViewChild, AfterViewInit } from '@angular/core';
import { CommonModule } from '@angular/common';
import { MaintenanceService } from '../../services/maintenance.service';
import { PropertiesService } from '../../services/properties.service';
import { MaintenanceStatusService } from '../../services/maintenance-status.service';
import { IMaintenance } from '../../interfaces/maintenance';
import { IProperty } from '../../interfaces/properties';
import { IMaintenanceStatus } from '../../interfaces/maintenanceStatus';
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
import { MaintenanceDialogComponent } from './maintenance-dialog/maintenance-dialog.component';
import { ConfirmationDialogComponent } from '../shared/confirmation-dialog/confirmation-dialog.component';

@Component({
  selector: 'app-maintenance',
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
  templateUrl: './maintenance.component.html',
  styleUrls: ['./maintenance.component.scss']
})
export class MaintenanceComponent implements OnInit, AfterViewInit {
  dataSource = new MatTableDataSource<IMaintenance>([]);
  displayedColumns: string[] = ['id', 'description', 'status', 'scheduledDate', 'propertyId', 'actions'];
  loading = false;
  properties: IProperty[] = [];
  maintenanceStatuses: IMaintenanceStatus[] = [];

  @ViewChild(MatPaginator) paginator!: MatPaginator;
  @ViewChild(MatSort) sort!: MatSort;

  constructor(
    private maintenanceService: MaintenanceService,
    private propertiesService: PropertiesService,
    private maintenanceStatusService: MaintenanceStatusService,
    private dialog: MatDialog,
    private snackBar: MatSnackBar
  ) {}

  ngOnInit(): void {
    this.loadMaintenance();
    this.loadProperties();
    this.loadMaintenanceStatuses();
  }

  ngAfterViewInit(): void {
    this.dataSource.paginator = this.paginator;
    this.dataSource.sort = this.sort;
  }

  loadMaintenance(): void {
    this.loading = true;
    this.maintenanceService.get().subscribe({
      next: (data) => {
        this.dataSource.data = data;
        if (this.paginator) {
          this.dataSource.paginator = this.paginator;
        }
        this.loading = false;
      },
      error: (error) => {
        console.error('Error loading maintenance:', error);
        this.snackBar.open('Error loading maintenance', 'Close', { duration: 3000 });
        this.loading = false;
      }
    });
  }

  loadProperties(): void {
    this.propertiesService.get().subscribe({
      next: (data) => {
        this.properties = data;
      },
      error: (error) => {
        console.error('Error loading properties:', error);
      }
    });
  }

  loadMaintenanceStatuses(): void {
    this.maintenanceStatusService.get().subscribe({
      next: (data) => {
        this.maintenanceStatuses = data;
      },
      error: (error) => {
        console.error('Error loading maintenance statuses:', error);
      }
    });
  }

  openCreateDialog(): void {
    const dialogRef = this.dialog.open(MaintenanceDialogComponent, {
      width: '600px',
      data: {
        maintenance: null,
        properties: this.properties,
        maintenanceStatuses: this.maintenanceStatuses
      }
    });

    dialogRef.afterClosed().subscribe(result => {
      if (result) {
        this.createMaintenance(result);
      }
    });
  }

  openEditDialog(maintenance: IMaintenance): void {
    const dialogRef = this.dialog.open(MaintenanceDialogComponent, {
      width: '600px',
      data: {
        maintenance: { ...maintenance },
        properties: this.properties,
        maintenanceStatuses: this.maintenanceStatuses
      }
    });

    dialogRef.afterClosed().subscribe(result => {
      if (result && maintenance.id) {
        this.updateMaintenance(maintenance.id, result);
      }
    });
  }

  createMaintenance(maintenance: IMaintenance): void {
    this.maintenanceService.create(maintenance).subscribe({
      next: () => {
        this.snackBar.open('Maintenance created successfully', 'Close', { duration: 3000 });
        this.loadMaintenance();
      },
      error: (error) => {
        console.error('Error creating maintenance:', error);
        this.snackBar.open('Error creating maintenance', 'Close', { duration: 3000 });
      }
    });
  }

  updateMaintenance(id: number, maintenance: IMaintenance): void {
    this.maintenanceService.update(id, maintenance).subscribe({
      next: () => {
        this.snackBar.open('Maintenance updated successfully', 'Close', { duration: 3000 });
        this.loadMaintenance();
      },
      error: (error) => {
        console.error('Error updating maintenance:', error);
        this.snackBar.open('Error updating maintenance', 'Close', { duration: 3000 });
      }
    });
  }

  deleteMaintenance(maintenance: IMaintenance): void {
    const dialogRef = this.dialog.open(ConfirmationDialogComponent, {
      width: '400px',
      data: {
        title: 'Delete Maintenance',
        message: 'Are you sure you want to delete this maintenance task? This action cannot be undone.',
        confirmText: 'Delete',
        cancelText: 'Cancel',
        type: 'danger'
      }
    });

    dialogRef.afterClosed().subscribe(result => {
      if (result && maintenance.id) {
        this.maintenanceService.delete(maintenance.id).subscribe({
          next: () => {
            this.snackBar.open('Maintenance deleted successfully', 'Close', { duration: 3000 });
            this.loadMaintenance();
          },
          error: (error) => {
            console.error('Error deleting maintenance:', error);
            this.snackBar.open('Error deleting maintenance', 'Close', { duration: 3000 });
          }
        });
      }
    });
  }
}