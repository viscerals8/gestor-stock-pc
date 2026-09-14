import { Injectable, inject } from '@angular/core';
import { ToastController } from '@ionic/angular';
import { PcService } from './pc.service';
import { TareaService } from './tarea.service';
import { IntervencionService } from './intervencion.service';
import { UsuarioService } from './usuario.service';

const csvEscape = (valor: unknown) => `"${String(valor ?? '').replace(/"/g, '""')}"`;

@Injectable({ providedIn: 'root' })
export class ReporteService {
  private pcService = inject(PcService);
  private tareaService = inject(TareaService);
  private intervencionService = inject(IntervencionService);
  private usuarioService = inject(UsuarioService);
  private toastCtrl = inject(ToastController);


  descargar(tipo: string) {
    switch (tipo) {
      case 'Inventario':
        this.pcService.listar().subscribe((pcs) => {
          const filas = pcs.map((p) =>
            [p.id, p.nro_serie, p.marca, p.modelo, p.estado, p.usuario_asignado].map(csvEscape).join(',')
          );
          this.exportar(tipo, ['ID,Serie,Marca,Modelo,Estado,Usuario asignado', ...filas]);
        });
        break;

      case 'Historial de PCs':
        this.intervencionService.listar().subscribe((items) => {
          const filas = items.map((i) =>
            [i.id, i.pc_serie, i.tecnico_nombre, i.estado, i.fecha, i.observacion].map(csvEscape).join(',')
          );
          this.exportar(tipo, ['ID,PC,Técnico,Estado,Fecha,Observación', ...filas]);
        });
        break;

      case 'Tareas Técnicas':
        this.tareaService.listar().subscribe((tareas) => {
          const filas = tareas.map((t) =>
            [t.id, t.titulo, t.pc_serie, t.tecnico_nombre, t.estado, t.fecha_creacion].map(csvEscape).join(',')
          );
          this.exportar(tipo, ['ID,Título,PC,Técnico,Estado,Fecha creación', ...filas]);
        });
        break;

      case 'Usuarios':
        this.usuarioService.listar().subscribe({
          next: (usuarios) => {
            const filas = usuarios.map((u) =>
              [u.id, u.nombre, u.correo, u.rol, u.activo ? 'Sí' : 'No'].map(csvEscape).join(',')
            );
            this.exportar(tipo, ['ID,Nombre,Correo,Rol,Activo', ...filas]);
          },
          error: async () => {
            const toast = await this.toastCtrl.create({
              message: 'Solo un administrador puede descargar el reporte de usuarios.',
              duration: 2000,
              color: 'warning',
            });
            toast.present();
          },
        });
        break;
    }
  }

  private exportar(tipo: string, lineas: string[]) {
    const blob = new Blob([lineas.join('\n')], { type: 'text/csv;charset=utf-8;' });
    const url = window.URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = `reporte_${tipo.replace(/\s/g, '_')}.csv`;
    a.click();
    window.URL.revokeObjectURL(url);
  }
}
