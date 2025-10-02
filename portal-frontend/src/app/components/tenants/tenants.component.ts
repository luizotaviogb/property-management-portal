import { Component, OnInit, ViewChild, AfterViewInit } from '@angular/core';
import { CommonModule } from '@angular/common';
import { TenantsService } from '../../services/tenants.service';
import { PropertiesService } from '../../services/properties.service';
import { PaymentStatusService } from '../../services/payment-status.service';
import { ITenant } from '../../interfaces/tenants';
import { IProperty } from '../../interfaces/properties';
import { IPaymentStatus } from '../../interfaces/paymentStatus';
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
import { TenantDialogComponent } from './tenant-dialog/tenant-dialog.component';
import { ConfirmationDialogComponent } from '../shared/confirmation-dialog/confirmation-dialog.component';

@Component({
  selector: 'app-tenants',
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
  templateUrl: './tenants.component.html',
  styleUrls: ['./tenants.component.scss']
})
export class TenantsComponent implements OnInit, AfterViewInit {
  dataSource = new MatTableDataSource<ITenant>([]);
  displayedColumns: string[] = ['id', 'name', 'info', 'leaseStart', 'leaseEnd', 'paymentStatus', 'propertyId', 'actions'];
  loading = false;
  properties: IProperty[] = [];
  paymentStatuses: IPaymentStatus[] = [];

  @ViewChild(MatPaginator) paginator!: MatPaginator;
  @ViewChild(MatSort) sort!: MatSort;

  constructor(
    private tenantsService: TenantsService,
    private propertiesService: PropertiesService,
    private paymentStatusService: PaymentStatusService,
    private dialog: MatDialog,
    private snackBar: MatSnackBar
  ) {}

  ngOnInit(): void {
    this.loadTenants();
    this.loadProperties();
    this.loadPaymentStatuses();
  }

  ngAfterViewInit(): void {
    this.dataSource.paginator = this.paginator;
    this.dataSource.sort = this.sort;
  }

  loadTenants(): void {
    this.loading = true;
    this.tenantsService.get().subscribe({
      next: (data) => {
        this.dataSource.data = data;
        this.loading = false;
      },
      error: (error) => {
        console.error('Error loading tenants:', error);
        this.snackBar.open('Error loading tenants', 'Close', { duration: 3000 });
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

  loadPaymentStatuses(): void {
    this.paymentStatusService.get().subscribe({
      next: (data) => {
        this.paymentStatuses = data;
      },
      error: (error) => {
        console.error('Error loading payment statuses:', error);
      }
    });
  }

  openCreateDialog(): void {
    const dialogRef = this.dialog.open(TenantDialogComponent, {
      width: '600px',
      data: {
        tenant: null,
        properties: this.properties,
        paymentStatuses: this.paymentStatuses
      }
    });

    dialogRef.afterClosed().subscribe(result => {
      if (result) {
        this.createTenant(result);
      }
    });
  }

  openEditDialog(tenant: ITenant): void {
    const dialogRef = this.dialog.open(TenantDialogComponent, {
      width: '600px',
      data: {
        tenant: { ...tenant },
        properties: this.properties,
        paymentStatuses: this.paymentStatuses
      }
    });

    dialogRef.afterClosed().subscribe(result => {
      if (result && tenant.id) {
        this.updateTenant(tenant.id, result);
      }
    });
  }

  createTenant(tenant: ITenant): void {
    this.tenantsService.create(tenant).subscribe({
      next: () => {
        this.snackBar.open('Tenant created successfully', 'Close', { duration: 3000 });
        this.loadTenants();
      },
      error: (error) => {
        console.error('Error creating tenant:', error);
        this.snackBar.open('Error creating tenant', 'Close', { duration: 3000 });
      }
    });
  }

  updateTenant(id: number, tenant: ITenant): void {
    this.tenantsService.update(id, tenant).subscribe({
      next: () => {
        this.snackBar.open('Tenant updated successfully', 'Close', { duration: 3000 });
        this.loadTenants();
      },
      error: (error) => {
        console.error('Error updating tenant:', error);
        this.snackBar.open('Error updating tenant', 'Close', { duration: 3000 });
      }
    });
  }

  deleteTenant(tenant: ITenant): void {
    const dialogRef = this.dialog.open(ConfirmationDialogComponent, {
      width: '400px',
      data: {
        title: 'Delete Tenant',
        message: `Are you sure you want to delete tenant "${tenant.name}"? This action cannot be undone.`,
        confirmText: 'Delete',
        cancelText: 'Cancel',
        type: 'danger'
      }
    });

    dialogRef.afterClosed().subscribe(result => {
      if (result && tenant.id) {
        this.tenantsService.delete(tenant.id).subscribe({
          next: () => {
            this.snackBar.open('Tenant deleted successfully', 'Close', { duration: 3000 });
            this.loadTenants();
          },
          error: (error) => {
            console.error('Error deleting tenant:', error);
            this.snackBar.open('Error deleting tenant', 'Close', { duration: 3000 });
          }
        });
      }
    });
  }
}