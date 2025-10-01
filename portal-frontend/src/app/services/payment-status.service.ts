import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable } from 'rxjs';
import { map } from 'rxjs/operators';
import { IPaymentStatus } from '../interfaces/paymentStatus';
import { environment } from '../../environments/environment';

@Injectable({
  providedIn: 'root',
})
export class PaymentStatusService {
  private baseUrl = `${environment.apiUrl}/payment-status`;

  constructor(private http: HttpClient) {}

  get(): Observable<IPaymentStatus[]> {
    return this.http.get<{ data: any[] }>(this.baseUrl).pipe(
      map(response => response.data.map(item => ({
        id: item.paymentstatusid,
        description: item.description
      })))
    );
  }
}