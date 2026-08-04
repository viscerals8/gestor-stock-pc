// historial-pcs.page.ts

import { Component, OnInit } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';
import {
  IonContent,
  IonHeader,
  IonTitle,
  IonToolbar,
  IonCard,
  IonCardHeader,
  IonCardTitle,
  IonCardSubtitle,
  IonCardContent,
  IonSearchbar,
  IonButton,
  IonButtons,
  IonMenuButton,
} from '@ionic/angular/standalone';
import { IonicModule } from '@ionic/angular';
import { IntervencionService } from '../../core/services/intervencion.service';
import { Intervencion } from '../../core/models/intervencion.model';
import { filtrarPorTexto } from '../../core/utils/filtro.util';

@Component({
  selector: 'app-historial-pcs',
  templateUrl: './historial-pcs.page.html',
  styleUrls: ['./historial-pcs.page.scss'],
  standalone: true,
  imports: [
    CommonModule,
    FormsModule,

    IonContent,
    IonHeader,
    IonTitle,
    IonToolbar,
    IonCard,
    IonCardHeader,
    IonCardTitle,
    IonCardSubtitle,
    IonCardContent,
    IonSearchbar,
    IonButton,
    IonButtons,
    IonMenuButton,
  ],
})
export class HistorialPcsPage implements OnInit {
  filtrosBusqueda: string = '';
  intervencionSeleccionada: Intervencion | null = null;
  intervenciones: Intervencion[] = [];
  cargando = false;

  constructor(private intervencionService: IntervencionService) {}

  ngOnInit() {
    this.cargar();
  }

  cargar() {
    this.cargando = true;
    this.intervencionService.listar().subscribe({
      next: (intervenciones) => {
        this.intervenciones = intervenciones;
        this.cargando = false;
      },
      error: () => {
        this.cargando = false;
      }
    });
  }

  filtarIntervenciones() {
    return filtrarPorTexto(this.intervenciones, this.filtrosBusqueda,
      ['tecnico_nombre', 'estado', 'observacion', 'pc_serie']);
  }

  mostrarDetalle(intervencion: Intervencion) {
    if (this.intervencionSeleccionada === intervencion) {
      this.intervencionSeleccionada = null;
    } else {
      this.intervencionSeleccionada = intervencion;
    }
  }

  cerrarDetalle() {
    this.intervencionSeleccionada = null;
  }
}
