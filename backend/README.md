# Backend - Gestor Stock PC

API en FastAPI + SQLAlchemy conectada a SQL Server, para reemplazar los datos hardcodeados
del frontend Ionic/Angular (`ti-app`).

## Configuración

1. Copiar `.env.example` a `.env` y completar los valores reales (servidor, usuario `sa`,
   contraseña, secreto JWT, credenciales del admin inicial). El archivo `.env` está en
   `.gitignore`, nunca se sube al repo.

2. Instalar dependencias (ya están instaladas globalmente en este equipo, pero para un
   entorno limpio):
   ```
   pip install -r requirements.txt
   ```

3. Inicializar la base de datos (crea la base si no existe, crea las tablas y el usuario
   admin definido en `.env`):
   ```
   python -m scripts.init_db
   ```

4. Levantar el servidor:
   ```
   uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
   ```

5. Documentación interactiva de la API: http://localhost:8000/docs

## Módulos

- `auth` — login (JWT) y usuario actual.
- `usuarios` — alta de usuarios/técnicos (solo admin).
- `pcs` — inventario de equipos.
- `celulares` — inventario de celulares corporativos.
- `tareas` — tablero de tareas técnicas (Kanban), enlazadas opcionalmente a un PC y a un técnico.
- `intervenciones` — historial de intervenciones, siempre enlazadas a un PC real.

Roles: `admin` y `tecnico`. Ambos pueden leer/crear/editar los recursos; solo `admin`
puede eliminar y gestionar usuarios.

## Tests

Los tests corren contra una base SQLite temporal (no tocan el SQL Server real).

```
pip install -r requirements-dev.txt
python -m pytest tests/ -v
```

Cubren autenticación (login válido/inválido, usuario inactivo, `/auth/me`), CRUD de
PCs (alta, duplicados, edición, permisos de borrado por rol) y permisos de gestión
de usuarios (solo `admin`).
