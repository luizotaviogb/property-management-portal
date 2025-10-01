import { CommonModule } from '@angular/common';
import { Component } from '@angular/core';
import { TenantsComponent } from '../tenants/tenants.component';
import { PropertiesComponent } from '../properties/properties.component';
import { MaintenanceComponent } from '../maintenance/maintenance.component';
import { MatTabsModule } from '@angular/material/tabs';
import { MatCardModule } from '@angular/material/card';
import { MatToolbarModule } from '@angular/material/toolbar';
import { MatIconModule } from '@angular/material/icon';
import { MatButtonModule } from '@angular/material/button';

@Component({
  selector: 'app-main',
  standalone: true,
  imports: [
    CommonModule,
    TenantsComponent,
    PropertiesComponent,
    MaintenanceComponent,
    MatTabsModule,
    MatCardModule,
    MatToolbarModule,
    MatIconModule,
    MatButtonModule,
  ],
  templateUrl: './main.component.html',
  styleUrls: ['./main.component.scss'],
})
export class MainComponent {
  selectedTabIndex: number = 0;
  currentYear = new Date().getFullYear();
}
