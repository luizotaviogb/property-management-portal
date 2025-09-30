import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable } from 'rxjs';
import { IPropertyType } from '../interfaces/propertyType';
import { environment } from '../../environments/environment';

@Injectable({
  providedIn: 'root',
})
export class PropertyTypeService {
  private baseUrl = `${environment.apiUrl}/property-type`;

  constructor(private http: HttpClient) {}

  get(): Observable<IPropertyType[]> {
    return this.http.get<IPropertyType[]>(this.baseUrl);
  }
}