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
import { IMaintenance } from '../../../interfaces/maintenance';
import { IProperty } from '../../../interfaces/properties';
import { IMaintenanceStatus } from '../../../interfaces/maintenanceStatus';

export interface MaintenanceDialogData {
  maintenance: IMaintenance | null;
  properties: IProperty[];
  maintenanceStatuses: IMaintenanceStatus[];
}

@Component({
  selector: 'app-maintenance-dialog',
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
  templateUrl: './maintenance-dialog.component.html',
  styleUrls: ['./maintenance-dialog.component.scss']
})
export class MaintenanceDialogComponent implements OnInit {
  maintenanceForm: FormGroup;
  isEditMode: boolean;

  constructor(
    private fb: FormBuilder,
    public dialogRef: MatDialogRef<MaintenanceDialogComponent>,
    @Inject(MAT_DIALOG_DATA) public data: MaintenanceDialogData
  ) {
    this.isEditMode = !!data.maintenance;

    const scheduledDate = data.maintenance?.scheduledDate || data.maintenance?.scheduleddate || '';
    const statusId = data.maintenance?.statusId || data.maintenance?.maintenancestatusid || '';
    const propertyId = data.maintenance?.propertyId || data.maintenance?.propertyid || '';

    this.maintenanceForm = this.fb.group({
      description: [data.maintenance?.description || '', Validators.required],
      maintenancestatusid: [statusId, Validators.required],
      scheduleddate: [scheduledDate, Validators.required],
      propertyid: [propertyId, Validators.required]
    });
  }

  ngOnInit(): void {}

  onCancel(): void {
    this.dialogRef.close();
  }

  onSubmit(): void {
    if (this.maintenanceForm.valid) {
      const formValue = this.maintenanceForm.value;

      const date = new Date(formValue.scheduleddate);
      const formattedDate = date.toISOString().split('T')[0];

      const maintenance: IMaintenance = {
        description: formValue.description,
        maintenancestatusid: formValue.maintenancestatusid,
        scheduleddate: formattedDate,
        propertyid: formValue.propertyid
      };

      this.dialogRef.close(maintenance);
    }
  }
}
