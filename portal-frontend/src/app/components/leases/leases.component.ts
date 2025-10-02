import { Component, OnInit, ViewChild, AfterViewInit } from '@angular/core';
import { CommonModule } from '@angular/common';
import { LeasesService } from '../../services/leases.service';
import { TenantsService } from '../../services/tenants.service';
import { PropertiesService } from '../../services/properties.service';
import { PaymentStatusService } from '../../services/payment-status.service';
import { ILease } from '../../interfaces/lease';
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
import { ConfirmationDialogComponent } from '../shared/confirmation-dialog/confirmation-dialog.component';
import { LeaseDialogComponent } from './lease-dialog/lease-dialog.component';

@Component({
  selector: 'app-leases',
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
  templateUrl: './leases.component.html',
  styleUrls: ['./leases.component.scss']
})
export class LeasesComponent implements OnInit, AfterViewInit {
  dataSource = new MatTableDataSource<ILease>([]);
  displayedColumns: string[] = ['id', 'tenantName', 'propertyAddress', 'leaseStart', 'leaseEnd', 'paymentStatus', 'actions'];
  loading = false;
  tenants: ITenant[] = [];
  properties: IProperty[] = [];
  paymentStatuses: IPaymentStatus[] = [];

  @ViewChild(MatPaginator) paginator!: MatPaginator;
  @ViewChild(MatSort) sort!: MatSort;

  constructor(
    private leasesService: LeasesService,
    private tenantsService: TenantsService,
    private propertiesService: PropertiesService,
    private paymentStatusService: PaymentStatusService,
    private dialog: MatDialog,
    private snackBar: MatSnackBar
  ) {}

  ngOnInit(): void {
    this.loadLeases();
    this.loadTenants();
    this.loadProperties();
    this.loadPaymentStatuses();
  }

  ngAfterViewInit(): void {
    this.dataSource.paginator = this.paginator;
    this.dataSource.sort = this.sort;
  }

  loadLeases(): void {
    this.loading = true;
    this.leasesService.get().subscribe({
      next: (data) => {
        this.dataSource.data = data;
        this.loading = false;
      },
      error: (error) => {
        console.error('Error loading leases:', error);
        this.snackBar.open('Error loading leases', 'Close', { duration: 3000 });
        this.loading = false;
      }
    });
  }

  loadTenants(): void {
    this.tenantsService.get().subscribe({
      next: (data) => {
        this.tenants = data;
      },
      error: (error) => {
        console.error('Error loading tenants:', error);
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
    const dialogRef = this.dialog.open(LeaseDialogComponent, {
      width: '600px',
      data: {
        lease: null,
        tenants: this.tenants,
        properties: this.properties,
        paymentStatuses: this.paymentStatuses
      }
    });

    dialogRef.afterClosed().subscribe(result => {
      if (result) {
        this.createLease(result);
      }
    });
  }

  openEditDialog(lease: ILease): void {
    const dialogRef = this.dialog.open(LeaseDialogComponent, {
      width: '600px',
      data: {
        lease: { ...lease },
        tenants: this.tenants,
        properties: this.properties,
        paymentStatuses: this.paymentStatuses
      }
    });

    dialogRef.afterClosed().subscribe(result => {
      if (result && lease.id) {
        this.updateLease(lease.id, result);
      }
    });
  }

  createLease(lease: ILease): void {
    this.leasesService.create(lease).subscribe({
      next: () => {
        this.snackBar.open('Lease created successfully', 'Close', { duration: 3000 });
        this.loadLeases();
      },
      error: (error) => {
        console.error('Error creating lease:', error);
        this.snackBar.open('Error creating lease', 'Close', { duration: 3000 });
      }
    });
  }

  updateLease(id: number, lease: ILease): void {
    this.leasesService.update(id, lease).subscribe({
      next: () => {
        this.snackBar.open('Lease updated successfully', 'Close', { duration: 3000 });
        this.loadLeases();
      },
      error: (error) => {
        console.error('Error updating lease:', error);
        this.snackBar.open('Error updating lease', 'Close', { duration: 3000 });
      }
    });
  }

  deleteLease(lease: ILease): void {
    const dialogRef = this.dialog.open(ConfirmationDialogComponent, {
      width: '400px',
      data: {
        title: 'Delete Lease',
        message: `Are you sure you want to delete this lease? This action cannot be undone.`,
        confirmText: 'Delete',
        cancelText: 'Cancel',
        type: 'danger'
      }
    });

    dialogRef.afterClosed().subscribe(result => {
      if (result && lease.id) {
        this.leasesService.delete(lease.id).subscribe({
          next: () => {
            this.snackBar.open('Lease deleted successfully', 'Close', { duration: 3000 });
            this.loadLeases();
          },
          error: (error) => {
            console.error('Error deleting lease:', error);
            this.snackBar.open('Error deleting lease', 'Close', { duration: 3000 });
          }
        });
      }
    });
  }
}
