export interface Usuario {
  id: number;
  nombre: string;
  correo: string;
  rol: 'admin' | 'tecnico';
  activo: boolean;
  fecha_creacion: string;
}

export interface Token {
  access_token: string;
  token_type: string;
  usuario: Usuario;
}
