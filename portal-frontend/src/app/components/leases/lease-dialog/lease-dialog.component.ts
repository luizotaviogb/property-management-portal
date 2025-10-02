import { Component, Inject, OnInit } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormBuilder, FormGroup, Validators, ReactiveFormsModule } from '@angular/forms';
import { MatDialogRef, MAT_DIALOG_DATA, MatDialogModule } from '@angular/material/dialog';
import { MatFormFieldModule } from '@angular/material/form-field';
import { MatInputModule } from '@angular/material/input';
import { MatButtonModule } from '@angular/material/button';
import { MatSelectModule } from '@angular/material/select';
import { MatDatepickerModule } from '@angular/material/datepicker';
import { MatNativeDateModule } from '@angular/material/core';
import { ILease } from '../../../interfaces/lease';
import { ITenant } from '../../../interfaces/tenants';
import { IProperty } from '../../../interfaces/properties';
import { IPaymentStatus } from '../../../interfaces/paymentStatus';

export interface LeaseDialogData {
  lease: ILease | null;
  tenants: ITenant[];
  properties: IProperty[];
  paymentStatuses: IPaymentStatus[];
}

@Component({
  selector: 'app-lease-dialog',
  standalone: true,
  imports: [
    CommonModule,
    ReactiveFormsModule,
    MatDialogModule,
    MatFormFieldModule,
    MatInputModule,
    MatButtonModule,
    MatSelectModule,
    MatDatepickerModule,
    MatNativeDateModule
  ],
  templateUrl: './lease-dialog.component.html',
  styleUrls: ['./lease-dialog.component.scss']
})
export class LeaseDialogComponent implements OnInit {
  leaseForm: FormGroup;
  isEditMode: boolean;

  constructor(
    private fb: FormBuilder,
    public dialogRef: MatDialogRef<LeaseDialogComponent>,
    @Inject(MAT_DIALOG_DATA) public data: LeaseDialogData
  ) {
    this.isEditMode = !!data.lease;

    const leaseStart = data.lease?.leaseStart || data.lease?.leasetermstart || '';
    const leaseEnd = data.lease?.leaseEnd || data.lease?.leasetermend || '';
    const tenantId = data.lease?.tenantId || data.lease?.tenantid || '';
    const propertyId = data.lease?.propertyId || data.lease?.propertyid || '';
    const paymentStatusId = data.lease?.paymentStatusId || data.lease?.paymentstatusid || '';

    this.leaseForm = this.fb.group({
      tenantid: [tenantId, Validators.required],
      propertyid: [propertyId, Validators.required],
      leasetermstart: [leaseStart, Validators.required],
      leasetermend: [leaseEnd, Validators.required],
      paymentstatusid: [paymentStatusId, Validators.required]
    });
  }

  ngOnInit(): void {}

  onCancel(): void {
    this.dialogRef.close();
  }

  onSubmit(): void {
    if (this.leaseForm.valid) {
      const formValue = this.leaseForm.value;

      const leaseStart = new Date(formValue.leasetermstart);
      const leaseEnd = new Date(formValue.leasetermend);

      const lease: ILease = {
        tenantid: formValue.tenantid,
        propertyid: formValue.propertyid,
        leasetermstart: leaseStart.toISOString().split('T')[0],
        leasetermend: leaseEnd.toISOString().split('T')[0],
        paymentstatusid: formValue.paymentstatusid
      };

      this.dialogRef.close(lease);
    }
  }
}
