import { HttpClient } from '@angular/common/http';
import { Injectable } from '@angular/core';
import { Observable, map } from 'rxjs';
import { environment } from '../../../environments/environment';

@Injectable({ providedIn: 'root' })
export class UploadService {
  private readonly url = `${environment.apiUrl}/uploads/foto`;

  constructor(private http: HttpClient) {}

  subirFoto(archivo: Blob, nombreArchivo: string): Observable<string> {
    const formData = new FormData();
    formData.append('file', archivo, nombreArchivo);

    return this.http
      .post<{ url: string }>(this.url, formData)
      .pipe(map((res) => `${environment.apiUrl}${res.url}`));
  }
}
