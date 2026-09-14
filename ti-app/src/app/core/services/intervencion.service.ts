import { HttpClient } from '@angular/common/http';
import { Injectable, inject } from '@angular/core';
import { Observable } from 'rxjs';
import { environment } from '../../../environments/environment';
import { Intervencion, IntervencionCreate } from '../models/intervencion.model';

@Injectable({ providedIn: 'root' })
export class IntervencionService {
  private http = inject(HttpClient);

  private readonly url = `${environment.apiUrl}/intervenciones`;

  listar(filtros?: { pc_id?: number; texto?: string }): Observable<Intervencion[]> {
    const params: Record<string, string> = {};
    if (filtros?.pc_id) params['pc_id'] = String(filtros.pc_id);
    if (filtros?.texto) params['texto'] = filtros.texto;
    return this.http.get<Intervencion[]>(this.url, { params });
  }

  crear(data: IntervencionCreate): Observable<Intervencion> {
    return this.http.post<Intervencion>(this.url, data);
  }
}
