export interface ProgramasChecklist {
  [key: string]: boolean;
}

export interface Tarea {
  id: number;
  titulo: string;
  estado: string;
  observacion: string | null;
  imagen: string | null;
  programas: ProgramasChecklist;
  pc_id: number | null;
  tecnico_id: number | null;
  fecha_creacion: string;
  fecha_actualizacion: string;
  pc_serie?: string | null;
  tecnico_nombre?: string | null;

  // Solo UI (no persisten en backend): controlan despliegue de sub-listas del checklist.
  showOfficeVersions?: boolean;
  showCytomicVersions?: boolean;
}

export type TareaCreate = Pick<Tarea, 'titulo' | 'estado' | 'observacion' | 'imagen' | 'programas' | 'pc_id' | 'tecnico_id'>;
export type TareaUpdate = Partial<TareaCreate>;
