# Gestor Stock PC

Sistema de gestión de inventario TI (PCs y celulares corporativos) y seguimiento de
tareas de soporte técnico, con backend propio y base de datos real.

## El problema

El proyecto arrancó como un prototipo de interfaz sin backend: todos los datos vivían
hardcodeados en el frontend, se perdían al recargar la página, el login era una
comparación de strings en el cliente, y no había ningún control de acceso — cualquiera
podía entrar a cualquier pantalla escribiendo la URL directamente. El historial de
intervenciones referenciaba equipos con números de serie inventados que no coincidían
con los del inventario real, y los reportes y el dashboard mostraban números fijos
que no reflejaban ningún dato real.

## La solución

Reescritura completa de la capa de datos y seguridad, manteniendo la interfaz Ionic
original:

- Backend propio en **FastAPI**, con modelos relacionales reales en **SQL Server**.
- Autenticación con **JWT** y control de acceso por rol (`admin` / `tecnico`), tanto en
  la API como en las rutas del frontend.
- Todas las entidades (PCs, celulares, tareas, intervenciones) están relacionadas de
  verdad — el historial de un equipo apunta al PC real, no a datos sueltos.
- Reportes y KPIs del dashboard calculados en vivo contra la base de datos.

## Estado del proyecto

| Módulo                                             | Estado                        |
|-----------------------------------------------------|--------------------------------|
| Autenticación y control de acceso por rol           | ✅ Completo                    |
| Inventario de PCs (alta, edición, baja, filtros)     | ✅ Completo                    |
| Inventario de celulares (alta, edición, baja)        | ✅ Completo                    |
| Tablero de tareas técnicas (Kanban)                  | ✅ Completo                    |
| Historial de intervenciones por equipo               | ✅ Completo                    |
| Reportes en CSV con datos reales                     | ✅ Completo                    |
| Registro de PCs con foto (subida real + cámara)      | ✅ Completo                    |
| Feed de actividad reciente                           | 🔶 API lista, falta la pantalla |
| Gestión de usuarios desde la interfaz                | 🔶 API lista, falta la pantalla |
| Detalle de PC con foto e historial del equipo        | ⬜ Pendiente                    |

## Stack

- **Backend**: FastAPI + SQLAlchemy + SQL Server. JWT para autenticación, Pydantic
  para validación.
- **Frontend**: Ionic + Angular (standalone components) + Capacitor, preparado para
  empaquetarse como app móvil nativa.

## Estructura

```
backend/    API REST (FastAPI)
ti-app/     Aplicación Ionic/Angular
```

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
