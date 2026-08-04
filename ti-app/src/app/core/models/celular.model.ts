export interface Celular {
  id: number;
  codigo: string;
  numero: string | null;
  marca: string;
  modelo: string;
  estado: string;
  usuario_asignado: string | null;
  imei: string | null;
  codigo_proyecto: string | null;
  fecha_asignacion: string | null;
}

export type CelularCreate = Omit<Celular, 'id'>;
export type CelularUpdate = Partial<CelularCreate>;
