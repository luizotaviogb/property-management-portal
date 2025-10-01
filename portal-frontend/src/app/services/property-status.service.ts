import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable } from 'rxjs';
import { map } from 'rxjs/operators';
import { IPropertyStatus } from '../interfaces/propertyStatus';
import { environment } from '../../environments/environment';

@Injectable({
  providedIn: 'root',
})
export class PropertyStatusService {
  private baseUrl = `${environment.apiUrl}/property-status`;

  constructor(private http: HttpClient) {}

  get(): Observable<IPropertyStatus[]> {
    return this.http.get<{ data: any[] }>(this.baseUrl).pipe(
      map(response => response.data.map(item => ({
        id: item.propertystatusid,
        description: item.description
      })))
    );
  }
}