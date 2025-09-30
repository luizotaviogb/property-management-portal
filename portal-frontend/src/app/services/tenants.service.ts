import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable } from 'rxjs';
import { ITenant } from '../interfaces/tenants';
import { environment } from '../../environments/environment';

@Injectable({
  providedIn: 'root',
})
export class TenantsService {
  private baseUrl = `${environment.apiUrl}/tenants`;

  constructor(private http: HttpClient) {}

  get(): Observable<ITenant[]> {
    return this.http.get<ITenant[]>(this.baseUrl);
  }

  getById(id: number): Observable<ITenant> {
    return this.http.get<ITenant>(`${this.baseUrl}/${id}`);
  }

  create(tenant: ITenant): Observable<ITenant> {
    return this.http.post<ITenant>(this.baseUrl, tenant);
  }

  update(id: number, tenant: ITenant): Observable<ITenant> {
    return this.http.put<ITenant>(`${this.baseUrl}/${id}`, tenant);
  }

  delete(id: number): Observable<void> {
    return this.http.delete<void>(`${this.baseUrl}/${id}`);
  }
}