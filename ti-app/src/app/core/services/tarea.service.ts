import { HttpClient } from '@angular/common/http';
import { Injectable, inject } from '@angular/core';
import { Observable } from 'rxjs';
import { environment } from '../../../environments/environment';
import { Tarea, TareaCreate, TareaUpdate } from '../models/tarea.model';

@Injectable({ providedIn: 'root' })
export class TareaService {
  private http = inject(HttpClient);

  private readonly url = `${environment.apiUrl}/tareas`;

  listar(filtros?: { estado?: string; pc_id?: number; tecnico_id?: number }): Observable<Tarea[]> {
    const params: Record<string, string> = {};
    if (filtros?.estado) params['estado'] = filtros.estado;
    if (filtros?.pc_id) params['pc_id'] = String(filtros.pc_id);
    if (filtros?.tecnico_id) params['tecnico_id'] = String(filtros.tecnico_id);
    return this.http.get<Tarea[]>(this.url, { params });
  }

  crear(data: TareaCreate): Observable<Tarea> {
    return this.http.post<Tarea>(this.url, data);
  }

  actualizar(id: number, data: TareaUpdate): Observable<Tarea> {
    return this.http.put<Tarea>(`${this.url}/${id}`, data);
  }

  eliminar(id: number): Observable<void> {
    return this.http.delete<void>(`${this.url}/${id}`);
  }
}
