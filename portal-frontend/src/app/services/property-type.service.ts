import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable } from 'rxjs';
import { map } from 'rxjs/operators';
import { IPropertyType } from '../interfaces/propertyType';
import { environment } from '../../environments/environment';

@Injectable({
  providedIn: 'root',
})
export class PropertyTypeService {
  private baseUrl = `${environment.apiUrl}/property-type`;

  constructor(private http: HttpClient) {}

  get(): Observable<IPropertyType[]> {
    return this.http.get<{ data: any[] }>(this.baseUrl).pipe(
      map(response => response.data.map(item => ({
        id: item.propertytypeid,
        description: item.description
      })))
    );
  }
}