import { Component, OnInit, inject } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';
import {
  IonContent,
  IonHeader,
  IonTitle,
  IonToolbar,
  IonButtons,
  IonMenuButton,
  IonIcon,
  IonButton,
} from '@ionic/angular/standalone';
import { RouterLink } from '@angular/router';
import { NgChartsModule } from 'ng2-charts';
import { ChartType } from 'chart.js';
import { forkJoin } from 'rxjs';
import { addIcons } from 'ionicons';
import {
  timeOutline, listOutline, alertCircleOutline, checkmarkDoneOutline, addOutline,
} from 'ionicons/icons';
import { PcService } from '../../core/services/pc.service';
import { TareaService } from '../../core/services/tarea.service';
import { Pc } from '../../core/models/pc.model';
import { Tarea } from '../../core/models/tarea.model';

interface Kpi {
  titulo: string;
  valor: number;
  icono: string;
  color: string;
}

@Component({
  selector: 'app-dashboard-tecnico',
  standalone: true,
  imports: [
    IonContent,
    IonHeader,
    IonTitle,
    IonToolbar,
    IonButtons,
    IonMenuButton,
    IonIcon,
    IonButton,
    CommonModule,
    FormsModule,
    RouterLink,
    NgChartsModule
  ],
  templateUrl: './dashboard-tecnico.page.html',
  styleUrls: ['./dashboard-tecnico.page.scss']
})
export class DashboardTecnicoPage implements OnInit {
  private pcService = inject(PcService);
  private tareaService = inject(TareaService);


  kpis: Kpi[] = [
    { titulo: 'PCs pendientes', valor: 0, icono: 'time-outline', color: 'warning' },
    { titulo: 'Tareas activas', valor: 0, icono: 'list-outline', color: 'primary' },
    { titulo: 'Alertas de inventario', valor: 0, icono: 'alert-circle-outline', color: 'danger' },
    { titulo: 'PCs entregados', valor: 0, icono: 'checkmark-done-outline', color: 'success' },
  ];

  private pcs: Pc[] = [];
  private tareas: Tarea[] = [];

  chartType: ChartType = 'doughnut';
  chartData = {
    labels: ['Disponible', 'Asignado', 'Obsoleto', 'En juicio'],
    datasets: [
      {
        data: [0, 0, 0, 0],
        backgroundColor: ['#16a34a', '#5b5bd6', '#6b7280', '#dc2626'],
        hoverOffset: 4,
      }
    ]
  };

  constructor() {
    addIcons({ timeOutline, listOutline, alertCircleOutline, checkmarkDoneOutline, addOutline });
  }

  ngOnInit() {
    forkJoin({
      pcs: this.pcService.listar(),
      tareas: this.tareaService.listar(),
    }).subscribe(({ pcs, tareas }) => {
      this.pcs = pcs;
      this.tareas = tareas;
      this.calcularKpis();
    });
  }

  private calcularKpis() {
    const tareasActivas = this.tareas.filter(t => t.estado !== 'Listo').length;
    const pcsPendientes = this.tareas.filter(t => t.estado === 'Recibido' || t.estado === 'Diagnóstico').length;
    const alertasInventario = this.pcs.filter(p => p.estado === 'obsoleto').length;
    const pcsEntregados = this.pcs.filter(p => p.estado === 'asignado').length;

    this.kpis = [
      { ...this.kpis[0], valor: pcsPendientes },
      { ...this.kpis[1], valor: tareasActivas },
      { ...this.kpis[2], valor: alertasInventario },
      { ...this.kpis[3], valor: pcsEntregados },
    ];

    this.chartData = {
      ...this.chartData,
      datasets: [{
        ...this.chartData.datasets[0],
        data: [
          this.pcs.filter(p => p.estado === 'disponible').length,
          this.pcs.filter(p => p.estado === 'asignado').length,
          this.pcs.filter(p => p.estado === 'obsoleto').length,
          this.pcs.filter(p => p.estado === 'en juicio').length,
        ]
      }]
    };
  }
}
