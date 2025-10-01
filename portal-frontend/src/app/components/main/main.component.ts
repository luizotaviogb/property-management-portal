import { CommonModule } from '@angular/common';
import { Component } from '@angular/core';
import { TenantsComponent } from '../tenants/tenants.component';
import { PropertiesComponent } from '../properties/properties.component';
import { MaintenanceComponent } from '../maintenance/maintenance.component';

@Component({
  selector: 'app-main',
  standalone: true,
  imports: [CommonModule, TenantsComponent, PropertiesComponent, MaintenanceComponent],
  templateUrl: './main.component.html',
  styleUrls: ['./main.component.scss']
})
export class MainComponent {
  activeTab: string = 'tenants';

  setActiveTab(tab: string): void {
    this.activeTab = tab;
  }
}