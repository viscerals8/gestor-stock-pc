export interface Intervencion {
  id: number;
  pc_id: number;
  tecnico_id: number | null;
  fecha: string;
  estado: string;
  observacion: string | null;
  acciones: string[];
  usuarios: string[];
  fotos: string[];
  pc_serie: string | null;
  tecnico_nombre: string | null;
}

export type IntervencionCreate = Pick<Intervencion, 'pc_id' | 'tecnico_id' | 'estado' | 'observacion' | 'acciones' | 'usuarios' | 'fotos'>;
