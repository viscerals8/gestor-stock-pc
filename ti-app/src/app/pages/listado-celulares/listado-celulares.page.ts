import { Component, OnInit, inject } from '@angular/core';
import { CommonModule } from '@angular/common';
import { IonicModule } from '@ionic/angular';
import { FormsModule } from '@angular/forms';
import { RouterLink } from '@angular/router';
import { CelularService } from '../../core/services/celular.service';
import { Celular } from '../../core/models/celular.model';
import { filtrarPorTexto } from '../../core/utils/filtro.util';

@Component({
  selector: 'app-listado-celulares',
  standalone: true,
  templateUrl: './listado-celulares.page.html',
  styleUrls: ['./listado-celulares.page.scss'],
  imports: [
    CommonModule,
    IonicModule,
    FormsModule,
    RouterLink
  ]
})
export class ListadoCelularesPage implements OnInit {
  private celularService = inject(CelularService);


  busqueda = '';
  filtroUsuario = '';
  filtroCodigoProyecto = '';
  celulares: Celular[] = [];
  cargando = false;

  ngOnInit() {
    this.cargar();
  }

  cargar() {
    this.cargando = true;
    this.celularService.listar().subscribe({
      next: (celulares) => {
        this.celulares = celulares;
        this.cargando = false;
      },
      error: () => {
        this.cargando = false;
      }
    });
  }

  get celularesFiltrados() {
    const porFiltrosExactos = this.celulares.filter(c =>
      (!this.filtroUsuario || c.usuario_asignado === this.filtroUsuario) &&
      (!this.filtroCodigoProyecto || c.codigo_proyecto === this.filtroCodigoProyecto)
    );
    return filtrarPorTexto(porFiltrosExactos, this.busqueda, ['usuario_asignado', 'codigo_proyecto']);
  }
}
