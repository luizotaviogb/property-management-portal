import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable } from 'rxjs';
import { IProperty } from '../interfaces/properties';
import { environment } from '../../environments/environment';
import { map } from 'rxjs/operators';

@Injectable({
  providedIn: 'root',
})
export class PropertiesService {
  private baseUrl = `${environment.apiUrl}/properties`;

  constructor(private http: HttpClient) {}

  get(): Observable<IProperty[]> {
    return this.http.get<{ data: IProperty[] }>(`${this.baseUrl}/`).pipe(
      map(response => response.data)
    );
  }

  getById(id: number): Observable<IProperty> {
    return this.http.get<{ data: IProperty }>(`${this.baseUrl}/${id}`).pipe(
      map(response => response.data)
    );
  }

  create(property: IProperty): Observable<IProperty> {
    return this.http.post<{ data: IProperty }>(`${this.baseUrl}/`, property).pipe(
      map(response => response.data)
    );
  }

  update(id: number, property: IProperty): Observable<IProperty> {
    return this.http.put<{ data: IProperty }>(`${this.baseUrl}/${id}`, property).pipe(
      map(response => response.data)
    );
  }

  delete(id: number): Observable<void> {
    return this.http.delete<{ data: void }>(`${this.baseUrl}/${id}`).pipe(
      map(response => response.data)
    );
  }
}
