import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable } from 'rxjs';
import { IProperty } from '../interfaces/properties';
import { environment } from '../../environments/environment';

@Injectable({
  providedIn: 'root',
})
export class PropertiesService {
  private baseUrl = `${environment.apiUrl}/properties`;

  constructor(private http: HttpClient) {}

  get(): Observable<IProperty[]> {
    return this.http.get<IProperty[]>(this.baseUrl);
  }

  getById(id: number): Observable<IProperty> {
    return this.http.get<IProperty>(`${this.baseUrl}/${id}`);
  }

  create(property: IProperty): Observable<IProperty> {
    return this.http.post<IProperty>(this.baseUrl, property);
  }

  update(id: number, property: IProperty): Observable<IProperty> {
    return this.http.put<IProperty>(`${this.baseUrl}/${id}`, property);
  }

  delete(id: number): Observable<void> {
    return this.http.delete<void>(`${this.baseUrl}/${id}`);
  }
}
