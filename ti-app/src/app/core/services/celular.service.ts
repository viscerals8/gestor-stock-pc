import { HttpClient } from '@angular/common/http';
import { Injectable } from '@angular/core';
import { Observable } from 'rxjs';
import { environment } from '../../../environments/environment';
import { Celular, CelularCreate, CelularUpdate } from '../models/celular.model';

@Injectable({ providedIn: 'root' })
export class CelularService {
  private readonly url = `${environment.apiUrl}/celulares`;

  constructor(private http: HttpClient) {}

  listar(filtros?: { texto?: string; usuario_asignado?: string; codigo_proyecto?: string }): Observable<Celular[]> {
    const params: Record<string, string> = {};
    if (filtros?.texto) params['texto'] = filtros.texto;
    if (filtros?.usuario_asignado) params['usuario_asignado'] = filtros.usuario_asignado;
    if (filtros?.codigo_proyecto) params['codigo_proyecto'] = filtros.codigo_proyecto;
    return this.http.get<Celular[]>(this.url, { params });
  }

  obtener(id: number): Observable<Celular> {
    return this.http.get<Celular>(`${this.url}/${id}`);
  }

  crear(data: CelularCreate): Observable<Celular> {
    return this.http.post<Celular>(this.url, data);
  }

  actualizar(id: number, data: CelularUpdate): Observable<Celular> {
    return this.http.put<Celular>(`${this.url}/${id}`, data);
  }

  eliminar(id: number): Observable<void> {
    return this.http.delete<void>(`${this.url}/${id}`);
  }
}
