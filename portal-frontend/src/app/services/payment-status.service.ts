import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable } from 'rxjs';
import { IPaymentStatus } from '../interfaces/paymentStatus';
import { environment } from '../../environments/environment';

@Injectable({
  providedIn: 'root',
})
export class PaymentStatusService {
  private baseUrl = `${environment.apiUrl}/payment-status`;

  constructor(private http: HttpClient) {}

  get(): Observable<IPaymentStatus[]> {
    return this.http.get<IPaymentStatus[]>(this.baseUrl);
  }
}