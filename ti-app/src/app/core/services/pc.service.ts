import { HttpClient } from '@angular/common/http';
import { Injectable, inject } from '@angular/core';
import { Observable } from 'rxjs';
import { environment } from '../../../environments/environment';
import { Pc, PcCreate, PcUpdate } from '../models/pc.model';

@Injectable({ providedIn: 'root' })
export class PcService {
  private http = inject(HttpClient);

  private readonly url = `${environment.apiUrl}/pcs`;

  listar(filtros?: { texto?: string; estado?: string }): Observable<Pc[]> {
    const params: Record<string, string> = {};
    if (filtros?.texto) params['texto'] = filtros.texto;
    if (filtros?.estado) params['estado'] = filtros.estado;
    return this.http.get<Pc[]>(this.url, { params });
  }

  obtener(id: number): Observable<Pc> {
    return this.http.get<Pc>(`${this.url}/${id}`);
  }

  crear(data: PcCreate): Observable<Pc> {
    return this.http.post<Pc>(this.url, data);
  }

  actualizar(id: number, data: PcUpdate): Observable<Pc> {
    return this.http.put<Pc>(`${this.url}/${id}`, data);
  }

  eliminar(id: number): Observable<void> {
    return this.http.delete<void>(`${this.url}/${id}`);
  }
}
