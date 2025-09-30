import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable } from 'rxjs';
import { IPropertyStatus } from '../interfaces/propertyStatus';
import { environment } from '../../environments/environment';

@Injectable({
  providedIn: 'root',
})
export class PropertyStatusService {
  private baseUrl = `${environment.apiUrl}/property-status`;

  constructor(private http: HttpClient) {}

  get(): Observable<IPropertyStatus[]> {
    return this.http.get<IPropertyStatus[]>(this.baseUrl);
  }
}