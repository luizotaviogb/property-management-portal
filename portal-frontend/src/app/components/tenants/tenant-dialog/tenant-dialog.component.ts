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
import { ITenant } from '../../../interfaces/tenants';
import { IProperty } from '../../../interfaces/properties';
import { IPaymentStatus } from '../../../interfaces/paymentStatus';

export interface TenantDialogData {
  tenant: ITenant | null;
  properties: IProperty[];
  paymentStatuses: IPaymentStatus[];
}

@Component({
  selector: 'app-tenant-dialog',
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
  templateUrl: './tenant-dialog.component.html',
  styleUrls: ['./tenant-dialog.component.scss']
})
export class TenantDialogComponent implements OnInit {
  tenantForm: FormGroup;
  isEditMode: boolean;

  constructor(
    private fb: FormBuilder,
    public dialogRef: MatDialogRef<TenantDialogComponent>,
    @Inject(MAT_DIALOG_DATA) public data: TenantDialogData
  ) {
    this.isEditMode = !!data.tenant;

    const leaseStart = data.tenant?.leaseStart || data.tenant?.leasetermstart || '';
    const leaseEnd = data.tenant?.leaseEnd || data.tenant?.leasetermend || '';
    const contactInfo = data.tenant?.info || data.tenant?.contactinfo || '';
    const paymentStatusId = data.tenant?.paymentstatusid || '';
    const propertyId = data.tenant?.propertyId || data.tenant?.propertyid || '';

    this.tenantForm = this.fb.group({
      name: [data.tenant?.name || '', Validators.required],
      contactinfo: [contactInfo, Validators.required],
      leasetermstart: [leaseStart, Validators.required],
      leasetermend: [leaseEnd, Validators.required],
      paymentstatusid: [paymentStatusId, Validators.required],
      propertyid: [propertyId, Validators.required]
    });
  }

  ngOnInit(): void {}

  onCancel(): void {
    this.dialogRef.close();
  }

  onSubmit(): void {
    if (this.tenantForm.valid) {
      const formValue = this.tenantForm.value;

      const leaseStart = new Date(formValue.leasetermstart);
      const leaseEnd = new Date(formValue.leasetermend);

      const tenant: ITenant = {
        name: formValue.name,
        contactinfo: formValue.contactinfo,
        leasetermstart: leaseStart.toISOString().split('T')[0],
        leasetermend: leaseEnd.toISOString().split('T')[0],
        paymentstatusid: formValue.paymentstatusid,
        propertyid: formValue.propertyid
      };

      this.dialogRef.close(tenant);
    }
  }
}
