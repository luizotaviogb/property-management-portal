import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable } from 'rxjs';
import { ITenant } from '../interfaces/tenants';
import { environment } from '../../environments/environment';
import { map } from 'rxjs/operators';

@Injectable({
  providedIn: 'root',
})
export class TenantsService {
  private baseUrl = `${environment.apiUrl}/tenants`;

  constructor(private http: HttpClient) {}

  get(): Observable<ITenant[]> {
    return this.http.get<{ data: ITenant[] }>(`${this.baseUrl}/`).pipe(
      map(response => response.data)
    );
  }

  getById(id: number): Observable<ITenant> {
    return this.http.get<{ data: ITenant }>(`${this.baseUrl}/${id}`).pipe(
      map(response => response.data)
    );
  }

  create(tenant: ITenant): Observable<ITenant> {
    return this.http.post<{ data: ITenant }>(`${this.baseUrl}/`, tenant).pipe(
      map(response => response.data)
    );
  }

  update(id: number, tenant: ITenant): Observable<ITenant> {
    return this.http.put<{ data: ITenant }>(`${this.baseUrl}/${id}`, tenant).pipe(
      map(response => response.data)
    );
  }

  delete(id: number): Observable<void> {
    return this.http.delete<{ data: void }>(`${this.baseUrl}/${id}`).pipe(
      map(response => response.data)
    );
  }
}