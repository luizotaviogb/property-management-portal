import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable } from 'rxjs';
import { IMaintenance } from '../interfaces/maintenance';
import { environment } from '../../environments/environment';

@Injectable({
  providedIn: 'root',
})
export class MaintenanceService {
  private baseUrl = `${environment.apiUrl}/maintenance`;

  constructor(private http: HttpClient) {}

  get(): Observable<IMaintenance[]> {
    return this.http.get<IMaintenance[]>(this.baseUrl);
  }

  getById(id: number): Observable<IMaintenance> {
    return this.http.get<IMaintenance>(`${this.baseUrl}/${id}`);
  }

  create(maintenance: IMaintenance): Observable<IMaintenance> {
    return this.http.post<IMaintenance>(this.baseUrl, maintenance);
  }

  update(id: number, maintenance: IMaintenance): Observable<IMaintenance> {
    return this.http.put<IMaintenance>(`${this.baseUrl}/${id}`, maintenance);
  }

  delete(id: number): Observable<void> {
    return this.http.delete<void>(`${this.baseUrl}/${id}`);
  }
}