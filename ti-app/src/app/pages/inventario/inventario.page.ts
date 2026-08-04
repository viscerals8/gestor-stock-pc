import { Component, OnInit } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';
import {
  IonContent, IonHeader, IonTitle, IonToolbar, IonItem,
  IonLabel, IonInput, IonList, IonSelect, IonSelectOption,
  IonButtons, IonMenuButton
} from '@ionic/angular/standalone';
import { PcService } from '../../core/services/pc.service';
import { Pc } from '../../core/models/pc.model';
import { filtrarPorTexto } from '../../core/utils/filtro.util';

@Component({
  selector: 'app-inventario',
  templateUrl: './inventario.page.html',
  styleUrls: ['./inventario.page.scss'],
  standalone: true,
  imports: [
    IonList, IonInput, IonLabel, IonItem,
    IonContent, IonHeader, IonTitle, IonToolbar,
    IonSelect, IonSelectOption, CommonModule, FormsModule,
    IonButtons, IonMenuButton
  ]
})
export class InventarioPage implements OnInit {
  filtroTexto = '';
  filtroEstado = '';
  pcs: Pc[] = [];
  cargando = false;

  constructor(private pcService: PcService) {}

  ngOnInit() {
    this.cargar();
  }

  cargar() {
    this.cargando = true;
    this.pcService.listar().subscribe({
      next: (pcs) => {
        this.pcs = pcs;
        this.cargando = false;
      },
      error: () => {
        this.cargando = false;
      }
    });
  }

  get filtrados() {
    const porEstado = this.filtroEstado
      ? this.pcs.filter(pc => pc.estado === this.filtroEstado)
      : this.pcs;
    return filtrarPorTexto(porEstado, this.filtroTexto, ['marca', 'nro_serie', 'usuario_asignado']);
  }
}
