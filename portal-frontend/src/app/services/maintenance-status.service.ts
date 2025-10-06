import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable } from 'rxjs';
import { map } from 'rxjs/operators';
import { IMaintenanceStatus } from '../interfaces/maintenanceStatus';
import { environment } from '../../environments/environment';

@Injectable({
  providedIn: 'root',
})
export class MaintenanceStatusService {
  private baseUrl = `${environment.apiUrl}/maintenance-status`;

  constructor(private http: HttpClient) {}

  get(): Observable<IMaintenanceStatus[]> {
    return this.http.get<{ data: any[] }>(`${this.baseUrl}/`).pipe(
      map(response => response.data.map(item => ({
        id: item.maintenancestatusid,
        description: item.description
      })))
    );
  }
}