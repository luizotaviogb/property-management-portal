import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable } from 'rxjs';
import { IMaintenance } from '../interfaces/maintenance';
import { environment } from '../../environments/environment';
import { map } from 'rxjs/operators';

@Injectable({
  providedIn: 'root',
})
export class MaintenanceService {
  private baseUrl = `${environment.apiUrl}/maintenance`;

  constructor(private http: HttpClient) {}

  get(): Observable<IMaintenance[]> {
    return this.http.get<{ data: IMaintenance[] }>(this.baseUrl).pipe(
      map(response => response.data)
    );
  }

  getById(id: number): Observable<IMaintenance> {
    return this.http.get<{ data: IMaintenance }>(`${this.baseUrl}/${id}`).pipe(
      map(response => response.data)
    );
  }

  create(maintenance: IMaintenance): Observable<IMaintenance> {
    return this.http.post<{ data: IMaintenance }>(this.baseUrl, maintenance).pipe(
      map(response => response.data)
    );
  }

  update(id: number, maintenance: IMaintenance): Observable<IMaintenance> {
    return this.http.put<{ data: IMaintenance }>(`${this.baseUrl}/${id}`, maintenance).pipe(
      map(response => response.data)
    );
  }

  delete(id: number): Observable<void> {
    return this.http.delete<{ data: void }>(`${this.baseUrl}/${id}`).pipe(
      map(response => response.data)
    );
  }
}