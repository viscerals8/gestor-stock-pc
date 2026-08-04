export interface Pc {
  id: number;
  nro_serie: string;
  marca: string;
  modelo: string;
  estado: string;
  usuario_asignado: string | null;
  motivo: string | null;
  foto_url: string | null;
  fecha_registro: string;
}

export type PcCreate = Omit<Pc, 'id' | 'fecha_registro'>;
export type PcUpdate = Partial<PcCreate>;
