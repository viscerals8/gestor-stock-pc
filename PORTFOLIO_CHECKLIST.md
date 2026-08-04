# Checklist camino a portfolio

## Funcionalidad pendiente
- [ ] Feed de actividad reciente (pantalla — la API ya existe: `GET /actividad`)
- [ ] Gestión de usuarios desde la UI (la API ya existe: `GET/POST /usuarios`)
- [ ] Detalle de PC con foto e historial de intervenciones del equipo

## Calidad / profesionalismo del repo
- [x] Tests backend (pytest: auth, CRUD de PCs, permisos de usuarios — 18 tests, corren contra SQLite, no dependen del SQL Server real)
- [ ] Migraciones con Alembic (reemplaza `Base.metadata.create_all`)
- [ ] Capturas de pantalla en el README
- [ ] Video/demo corto embebido en el README
- [ ] Deploy público con base de datos separada y datos ficticios (demo real, sin depender de tu SQL Server interno)
- [ ] LICENSE (MIT)
- [ ] CI en GitHub Actions (corre los tests en cada push)
- [ ] De acá en adelante: commits más chicos y frecuentes, en vez de volcados grandes

Marcá los que ya resolvimos y avisame qué seguimos.
