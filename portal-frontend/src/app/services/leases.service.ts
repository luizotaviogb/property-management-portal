import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable } from 'rxjs';
import { ILease } from '../interfaces/lease';
import { environment } from '../../environments/environment';
import { map } from 'rxjs/operators';

@Injectable({
  providedIn: 'root',
})
export class LeasesService {
  private baseUrl = `${environment.apiUrl}/leases`;

  constructor(private http: HttpClient) {}

  get(): Observable<ILease[]> {
    return this.http.get<{ data: ILease[] }>(this.baseUrl).pipe(
      map(response => response.data)
    );
  }

  getById(id: number): Observable<ILease> {
    return this.http.get<{ data: ILease }>(`${this.baseUrl}/${id}`).pipe(
      map(response => response.data)
    );
  }

  getByTenant(tenantId: number): Observable<ILease[]> {
    return this.http.get<{ data: ILease[] }>(`${this.baseUrl}/tenant/${tenantId}`).pipe(
      map(response => response.data)
    );
  }

  getByProperty(propertyId: number): Observable<ILease[]> {
    return this.http.get<{ data: ILease[] }>(`${this.baseUrl}/property/${propertyId}`).pipe(
      map(response => response.data)
    );
  }

  create(lease: ILease): Observable<ILease> {
    return this.http.post<{ data: ILease }>(this.baseUrl, lease).pipe(
      map(response => response.data)
    );
  }

  update(id: number, lease: ILease): Observable<ILease> {
    return this.http.put<{ data: ILease }>(`${this.baseUrl}/${id}`, lease).pipe(
      map(response => response.data)
    );
  }

  delete(id: number): Observable<void> {
    return this.http.delete<{ data: void }>(`${this.baseUrl}/${id}`).pipe(
      map(response => response.data)
    );
  }
}
