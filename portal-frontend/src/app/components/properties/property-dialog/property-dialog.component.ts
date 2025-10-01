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
import { IProperty } from '../../../interfaces/properties';
import { IPropertyType } from '../../../interfaces/propertyType';
import { IPropertyStatus } from '../../../interfaces/propertyStatus';

export interface PropertyDialogData {
  property: IProperty | null;
  propertyTypes: IPropertyType[];
  propertyStatuses: IPropertyStatus[];
}

@Component({
  selector: 'app-property-dialog',
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
  templateUrl: './property-dialog.component.html',
  styleUrls: ['./property-dialog.component.scss']
})
export class PropertyDialogComponent implements OnInit {
  propertyForm: FormGroup;
  isEditMode: boolean;

  constructor(
    private fb: FormBuilder,
    public dialogRef: MatDialogRef<PropertyDialogComponent>,
    @Inject(MAT_DIALOG_DATA) public data: PropertyDialogData
  ) {
    this.isEditMode = !!data.property;
    this.propertyForm = this.fb.group({
      address: [data.property?.address || '', Validators.required],
      typeId: [data.property?.typeId || '', Validators.required],
      statusId: [data.property?.statusId || '', Validators.required],
      purchaseDate: [data.property?.purchaseDate || '', Validators.required],
      price: [data.property?.price || '', [Validators.required, Validators.min(0)]]
    });
  }

  ngOnInit(): void {}

  onCancel(): void {
    this.dialogRef.close();
  }

  onSubmit(): void {
    if (this.propertyForm.valid) {
      const formValue = this.propertyForm.value;

      const date = new Date(formValue.purchaseDate);
      const formattedDate = date.toISOString().split('T')[0];

      const property: IProperty = {
        address: formValue.address,
        typeId: formValue.typeId,
        statusId: formValue.statusId,
        purchaseDate: formattedDate,
        price: formValue.price
      };

      this.dialogRef.close(property);
    }
  }
}
