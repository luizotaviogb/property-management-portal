import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable } from 'rxjs';
import { IMaintenanceStatus } from '../interfaces/maintenanceStatus';
import { environment } from '../../environments/environment';

@Injectable({
  providedIn: 'root',
})
export class MaintenanceStatusService {
  private baseUrl = `${environment.apiUrl}/maintenance-status`;

  constructor(private http: HttpClient) {}

  get(): Observable<IMaintenanceStatus[]> {
    return this.http.get<IMaintenanceStatus[]>(this.baseUrl);
  }
}