import { Component, OnInit } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';
import { IonicModule } from '@ionic/angular';
import {
  IonContent, IonHeader, IonTitle, IonToolbar, IonButtons, IonMenuButton,
  IonTextarea, IonSelect, IonSelectOption, IonCheckbox, IonItem, IonLabel
} from '@ionic/angular/standalone';
import { TareaService } from '../../core/services/tarea.service';
import { Tarea } from '../../core/models/tarea.model';

@Component({
  selector: 'app-gestion-tareas',
  templateUrl: './gestion-tareas.page.html',
  styleUrls: ['./gestion-tareas.page.scss'],
  standalone: true,
  imports: [
    IonContent, IonHeader, IonTitle, IonToolbar, IonButtons, IonMenuButton,
    CommonModule, FormsModule,
    IonTextarea, IonSelect, IonSelectOption, IonCheckbox, IonItem, IonLabel
  ]
})
export class GestionTareasPage implements OnInit {
  columnas = ['Recibido', 'Diagnóstico', 'Reparación', 'Preparación', 'Listo'];

  programasDisponibles = [
    { key: 'chrome', nombre: 'Google Chrome' },
    { key: 'winrar', nombre: 'WinRAR' },
    { key: 'teamviewer', nombre: 'TeamViewer' },
  ];

  officeVersions = [
    { key: 'office2016', nombre: 'Office 2016' },
    { key: 'office2021', nombre: 'Office 2021' },
    { key: 'office2019', nombre: 'Office 2019' },
    { key: 'office365', nombre: 'Office 365' }
  ];

  cytomicVersions = [
    { key: 'cytomic_i', nombre: 'Cytomic Zona I' },
    { key: 'cytomic_ii', nombre: 'Cytomic Zona II' },
    { key: 'cytomic_iii', nombre: 'Cytomic Zona III' },
    { key: 'cytomic_iv', nombre: 'Cytomic Zona IV' },
    { key: 'cytomic_v', nombre: 'Cytomic Zona V' },
    { key: 'cytomic_vi', nombre: 'Cytomic Zona VI' }
  ];

  tareas: Tarea[] = [];
  cargando = false;

  constructor(private tareaService: TareaService) {}

  ngOnInit() {
    this.cargar();
  }

  cargar() {
    this.cargando = true;
    this.tareaService.listar().subscribe({
      next: (tareas) => {
        this.tareas = tareas.map(t => ({ ...t, programas: { ...this.inicializarProgramas(), ...t.programas } }));
        this.cargando = false;
      },
      error: () => {
        this.cargando = false;
      }
    });
  }

  inicializarProgramas() {
    return {
      chrome: false,
      winrar: false,
      teamviewer: false,
      office2019: false,
      office365: false,
      office2016: false,
      office2021: false,
      cytomic_i: false,
      cytomic_ii: false,
      cytomic_iii: false,
      cytomic_iv: false,
      cytomic_v: false,
      cytomic_vi: false
    };
  }

  cambiarEstado(tareaId: number, nuevoEstado: string) {
    const tarea = this.tareas.find(t => t.id === tareaId);
    if (!tarea) return;

    tarea.estado = nuevoEstado;
    this.persistir(tarea);
  }

  onImageneSelected(event: any, tarea: Tarea) {
    const file = event.target.files[0];
    if (file) {
      tarea.imagen = file.name;
      this.persistir(tarea);
    }
  }

  guardarObservacion(tarea: Tarea) {
    this.persistir(tarea);
  }

  guardarProgramas(tarea: Tarea) {
    this.persistir(tarea);
  }

  toggleOffice(tarea: Tarea) {
    tarea.showOfficeVersions = !tarea.showOfficeVersions;
  }

  toggleCytomic(tarea: Tarea) {
    tarea.showCytomicVersions = !tarea.showCytomicVersions;
  }

  filtradoPorEstado(estado: string): Tarea[] {
    return this.tareas.filter(t => t.estado === estado);
  }

  private persistir(tarea: Tarea) {
    this.tareaService.actualizar(tarea.id, {
      estado: tarea.estado,
      observacion: tarea.observacion,
      imagen: tarea.imagen,
      programas: tarea.programas,
    }).subscribe();
  }
}
