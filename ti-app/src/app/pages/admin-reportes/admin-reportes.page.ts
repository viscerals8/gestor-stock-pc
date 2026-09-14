import { Component, inject } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';
import {
  IonContent, IonHeader, IonTitle, IonToolbar, IonItem, IonList, IonLabel,
  IonIcon, IonButtons, IonMenuButton,
} from '@ionic/angular/standalone';
import { addIcons } from 'ionicons';
import { hardwareChipOutline, timeOutline, listOutline, peopleOutline } from 'ionicons/icons';
import { ReporteService } from '../../core/services/reporte.service';

@Component({
  selector: 'app-admin-reportes',
  templateUrl: './admin-reportes.page.html',
  styleUrls: ['./admin-reportes.page.scss'],
  standalone: true,
  imports: [
    IonContent, IonHeader, IonTitle, IonToolbar, CommonModule, FormsModule,
    IonItem, IonList, IonLabel, IonIcon, IonButtons, IonMenuButton,
  ]
})
export class AdminReportesPage {
  private reporteService = inject(ReporteService);

  constructor() {
    addIcons({ hardwareChipOutline, timeOutline, listOutline, peopleOutline });
  }

  descargar(tipo: string) {
    this.reporteService.descargar(tipo);
  }
}
