import { Component, OnInit } from '@angular/core';
import { CommonModule } from '@angular/common';
import { TenantsService } from '../../services/tenants.service';
import { ITenant } from '../../interfaces/tenants';

@Component({
  selector: 'app-tenants',
  standalone: true,
  imports: [CommonModule],
  templateUrl: './tenants.component.html',
  styleUrls: ['./tenants.component.scss']
})
export class TenantsComponent implements OnInit {
  tenants: ITenant[] = [];

  constructor(private tenantsService: TenantsService) {}

  ngOnInit(): void {
    this.tenantsService.get().subscribe((data) => {
      this.tenants = data;
    });
  }
}