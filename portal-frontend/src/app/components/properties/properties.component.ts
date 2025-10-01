import { Component, OnInit } from '@angular/core';
import { CommonModule } from '@angular/common';
import { PropertiesService } from '../../services/properties.service';
import { IProperty } from '../../interfaces/properties';

@Component({
  selector: 'app-properties',
  standalone: true,
  imports: [CommonModule],
  templateUrl: './properties.component.html',
  styleUrls: ['./properties.component.scss']
})
export class PropertiesComponent implements OnInit {
  properties: IProperty[] = [];

  constructor(private propertiesService: PropertiesService) {}

  ngOnInit(): void {
    this.propertiesService.get().subscribe((data) => {
        console.log(data)
      this.properties = data;
    });
  }
}