import { Component } from '@angular/core';
import { RouterOutlet } from '@angular/router';
import { MainComponent } from './components/main/main.component';
import { TenantsComponent } from './components/tenants/tenants.component';
import { PropertiesComponent } from './components/properties/properties.component';
import { MaintenanceComponent } from './components/maintenance/maintenance.component';

@Component({
  selector: 'app-root',
  standalone: true,
  imports: [RouterOutlet, MainComponent, TenantsComponent, PropertiesComponent, MaintenanceComponent],
  templateUrl: './app.component.html',
  styleUrl: './app.component.scss'
})
export class AppComponent {
  title = 'portal-frontend';
}
