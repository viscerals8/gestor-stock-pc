# Gestor Stock PC

Sistema de gestión de inventario TI (PCs y celulares corporativos) y seguimiento de
tareas de soporte técnico.

## Stack

- **Backend**: FastAPI + SQLAlchemy, conectado a SQL Server. Auth con JWT, roles
  `admin` / `tecnico`.
- **Frontend**: Ionic + Angular (standalone components), con Capacitor para poder
  empaquetarse como app móvil.

## Estructura

```
backend/    API REST (FastAPI)
ti-app/     Aplicación Ionic/Angular
```

## Funcionalidades

- Login con JWT y control de acceso por rol.
- Inventario de PCs: alta, edición, baja, filtros por estado/texto.
- Inventario de celulares corporativos: alta, edición, baja.
- Registro de PCs con foto real (subida al backend) o captura por cámara (Capacitor).
- Tablero de tareas técnicas (kanban) con checklist de programas instalados.
- Historial de intervenciones por equipo.
- Reportes descargables en CSV con datos reales (inventario, historial, tareas, usuarios).
- Feed de actividad reciente.

## Cómo correrlo

### Backend

Ver [backend/README.md](backend/README.md) para el detalle completo (variables de
entorno, inicialización de la base de datos, etc.). Resumen:

```
cd backend
python -m scripts.init_db     # crea la base y el usuario admin (una sola vez)
uvicorn app.main:app --reload --port 8000
```

### Frontend

```
cd ti-app
npm install
npx ng serve
```

La app queda disponible en `http://localhost:4200` y espera al backend en
`http://localhost:8000` (configurable en `ti-app/src/environments/`).
