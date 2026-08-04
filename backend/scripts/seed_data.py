"""
Carga datos de ejemplo realistas (los mismos que el frontend tenía hardcodeados
antes de conectarse a la base real), para poder ver la app con contenido.

Es seguro correrlo varias veces: si ya hay PCs cargados, no vuelve a insertar.

Ejecutar desde la carpeta backend/ con:
    python -m scripts.seed_data
"""
import sys
from datetime import datetime
from pathlib import Path

sys.path.append(str(Path(__file__).resolve().parent.parent))

from app.config import settings
from app.database import SessionLocal
from app.models import Celular, Intervencion, Pc, Tarea, Usuario
from app.security import hash_password

MODELOS_POR_MARCA = {
    "HP": "ProBook 440",
    "Dell": "Latitude 5420",
    "Lenovo": "ThinkPad E14",
    "Asus": "VivoBook 15",
    "Acer": "Aspire 5",
}

PCS_SEED = [
    {"marca": "HP", "serie": "SN001", "usuario": "Carlos", "estado": "disponible"},
    {"marca": "Dell", "serie": "SN002", "usuario": "Ana", "estado": "obsoleto"},
    {"marca": "Lenovo", "serie": "SN003", "usuario": "Pedro", "estado": "asignado"},
    {"marca": "Asus", "serie": "SN004", "usuario": "Lucía", "estado": "en juicio"},
    {"marca": "Acer", "serie": "SN005", "usuario": "Mario", "estado": "disponible"},
    {"marca": "HP", "serie": "SN006", "usuario": "Claudia", "estado": "obsoleto"},
    {"marca": "Dell", "serie": "SN007", "usuario": "Sofía", "estado": "asignado"},
    {"marca": "Lenovo", "serie": "SN008", "usuario": "Luis", "estado": "en juicio"},
    {"marca": "Asus", "serie": "SN009", "usuario": "José", "estado": "disponible"},
    {"marca": "Acer", "serie": "SN010", "usuario": "Marta", "estado": "disponible"},
    {"marca": "HP", "serie": "SN011", "usuario": "Elena", "estado": "asignado"},
    {"marca": "Dell", "serie": "SN012", "usuario": "Tomás", "estado": "en juicio"},
    {"marca": "Lenovo", "serie": "SN013", "usuario": "Sebastián", "estado": "obsoleto"},
    {"marca": "Asus", "serie": "SN014", "usuario": "Fernanda", "estado": "disponible"},
    {"marca": "Acer", "serie": "SN015", "usuario": "Ignacio", "estado": "obsoleto"},
    {"marca": "HP", "serie": "SN016", "usuario": "Valentina", "estado": "asignado"},
    {"marca": "Dell", "serie": "SN017", "usuario": "Camila", "estado": "en juicio"},
    {"marca": "Lenovo", "serie": "SN018", "usuario": "Rodrigo", "estado": "disponible"},
    {"marca": "Asus", "serie": "SN019", "usuario": "Pablo", "estado": "asignado"},
    {"marca": "Acer", "serie": "SN020", "usuario": "Carla", "estado": "disponible"},
    {"marca": "HP", "serie": "SN021", "usuario": "Andrés", "estado": "obsoleto"},
    {"marca": "Dell", "serie": "SN022", "usuario": "Florencia", "estado": "asignado"},
    {"marca": "Lenovo", "serie": "SN023", "usuario": "Gabriel", "estado": "disponible"},
    {"marca": "Asus", "serie": "SN024", "usuario": "Emilia", "estado": "en juicio"},
    {"marca": "Acer", "serie": "SN025", "usuario": "Mateo", "estado": "disponible"},
    {"marca": "HP", "serie": "SN026", "usuario": "Antonia", "estado": "asignado"},
    {"marca": "Dell", "serie": "SN027", "usuario": "Vicente", "estado": "disponible"},
    {"marca": "Lenovo", "serie": "SN028", "usuario": "Martina", "estado": "obsoleto"},
    {"marca": "Asus", "serie": "SN029", "usuario": "Benjamín", "estado": "en juicio"},
    {"marca": "Acer", "serie": "SN030", "usuario": "Trinidad", "estado": "asignado"},
]

TECNICOS_SEED = [
    {"nombre": "Juan Pérez", "correo": "juan.perez@empresa.com"},
    {"nombre": "Ana Gómez", "correo": "ana.gomez@empresa.com"},
    {"nombre": "Carlos Rivas", "correo": "carlos.rivas@empresa.com"},
    {"nombre": "Marcela Díaz", "correo": "marcela.diaz@empresa.com"},
    {"nombre": "Luis Fernández", "correo": "luis.fernandez@empresa.com"},
]
TECNICO_PASSWORD_DEFAULT = settings.seed_tecnico_password

TAREAS_SEED = [
    {"titulo": "PC Juan Pérez", "estado": "Recibido"},
    {"titulo": "PC María López", "estado": "Diagnóstico"},
    {"titulo": "PC Roberto Díaz", "estado": "Reparación"},
    {"titulo": "PC Ana Castillo", "estado": "Listo"},
    {"titulo": "PC Diego Muñoz", "estado": "Preparación"},
    {"titulo": "PC Fernanda Ruiz", "estado": "Recibido"},
    {"titulo": "PC Tomás Herrera", "estado": "Diagnóstico"},
    {"titulo": "PC Valentina Gómez", "estado": "Reparación"},
    {"titulo": "PC Martín Soto", "estado": "Listo"},
    {"titulo": "PC Camila Araya", "estado": "Preparación"},
    {"titulo": "PC Luciano Herrera", "estado": "Recibido"},
    {"titulo": "PC Daniela Paredes", "estado": "Diagnóstico"},
    {"titulo": "PC Javier Palma", "estado": "Reparación"},
    {"titulo": "PC Andrea Salinas", "estado": "Listo"},
    {"titulo": "PC Ignacio Morales", "estado": "Preparación"},
]

PROGRAMAS_VACIO = {
    "chrome": False, "winrar": False, "teamviewer": False,
    "office2019": False, "office365": False, "office2016": False, "office2021": False,
    "cytomic_cl": False, "cytomic_pe": False, "cytomic_mx": False, "cytomic_co": False,
    "cytomic_ar": False, "cytomic_br": False, "cytomic_uy": False, "cytomic_ec": False,
}

# índice de la PC (0-based, sobre PCS_SEED) que recibe cada intervención
INTERVENCIONES_SEED = [
    {"pc_index": 0, "fecha": "2025-07-20T10:30", "tecnico": "Juan Pérez", "estado": "Reparado",
     "observacion": "Se reemplazó la fuente de poder y se limpió el ventilador.",
     "acciones": ["Reemplazo de fuente de poder", "Limpieza de ventilador"], "usuarios": ["Usuario A", "Usuario B"]},
    {"pc_index": 1, "fecha": "2025-07-18T15:00", "tecnico": "Ana Gómez", "estado": "Diagnóstico",
     "observacion": "Equipo con sobrecalentamiento y apagones frecuentes.",
     "acciones": ["Prueba de temperatura", "Revisión de ventilación"], "usuarios": ["Usuario A"]},
    {"pc_index": 2, "fecha": "2025-07-10T09:15", "tecnico": "Carlos Rivas", "estado": "En reparación",
     "observacion": "Problemas con el disco duro, se requiere reemplazo.",
     "acciones": ["Diagnóstico de disco", "Solicitud de nuevo disco"], "usuarios": ["Usuario C"]},
    {"pc_index": 3, "fecha": "2025-06-30T13:45", "tecnico": "Marcela Díaz", "estado": "Listo",
     "observacion": "Reinstalación completa del sistema operativo y drivers.",
     "acciones": ["Formateo", "Instalación de Windows", "Drivers actualizados"], "usuarios": ["Usuario D"]},
    {"pc_index": 4, "fecha": "2025-06-25T16:20", "tecnico": "Luis Fernández", "estado": "Pendiente",
     "observacion": "Falla intermitente en la pantalla, pendiente revisión de cableado.",
     "acciones": ["Revisión inicial", "Pendiente evaluación en laboratorio"], "usuarios": ["Usuario E"]},
    {"pc_index": 5, "fecha": "2025-06-18T11:00", "tecnico": "Ana Gómez", "estado": "Reparado",
     "observacion": "Cambio de batería y limpieza interna.",
     "acciones": ["Reemplazo batería", "Limpieza de componentes"], "usuarios": ["Usuario F"]},
    {"pc_index": 6, "fecha": "2025-06-10T08:30", "tecnico": "Carlos Rivas", "estado": "Listo",
     "observacion": "Configuración de red e instalación de software institucional.",
     "acciones": ["Configuración IP", "Instalación Office", "Antivirus corporativo"], "usuarios": ["Usuario G", "Usuario H"]},
    {"pc_index": 7, "fecha": "2025-05-28T14:10", "tecnico": "Juan Pérez", "estado": "Diagnóstico",
     "observacion": "Reporta lentitud extrema. Se sospecha malware.",
     "acciones": ["Pruebas de rendimiento", "Escaneo de virus"], "usuarios": ["Usuario I"]},
    {"pc_index": 8, "fecha": "2025-05-15T17:50", "tecnico": "Marcela Díaz", "estado": "En reparación",
     "observacion": "No detecta señal de red. Se cambiará tarjeta de red.",
     "acciones": ["Diagnóstico de red", "Solicitud de repuesto"], "usuarios": ["Usuario J"]},
    {"pc_index": 9, "fecha": "2025-04-30T10:00", "tecnico": "Luis Fernández", "estado": "Listo",
     "observacion": "Actualización de BIOS completada con éxito.",
     "acciones": ["Respaldo previo", "Actualización BIOS"], "usuarios": ["Usuario K"]},
]

CELULARES_SEED = [
    {"codigo": "CEL-001", "numero": "+56 9 1234 5678", "marca": "Samsung", "modelo": "A32",
     "estado": "Activo", "usuario_asignado": "Juan Pérez", "imei": "352099001761481",
     "codigo_proyecto": "2025/INFRA/0001/"},
    {"codigo": "CEL-002", "numero": "+56 9 8765 4321", "marca": "Xiaomi", "modelo": "Redmi Note 10",
     "estado": "Reparación", "usuario_asignado": None, "imei": None,
     "codigo_proyecto": "2025/BODEGA/0002/"},
    {"codigo": "CEL-003", "numero": "+56 9 5522 3311", "marca": "Motorola", "modelo": "Moto G30",
     "estado": "Activo", "usuario_asignado": "María López", "imei": "358965101122334",
     "codigo_proyecto": "2025/OPERACIONES/0003/"},
    {"codigo": "CEL-004", "numero": "+56 9 9988 7766", "marca": "Apple", "modelo": "iPhone 11",
     "estado": "Baja", "usuario_asignado": None, "imei": None,
     "codigo_proyecto": "2025/VENTAS/0004/"},
    {"codigo": "CEL-005", "numero": "+56 9 6677 8899", "marca": "Samsung", "modelo": "S21",
     "estado": "Activo", "usuario_asignado": "Pedro Muñoz", "imei": "353412098765432",
     "codigo_proyecto": "2025/FINANZAS/0005/"},
]


def seed():
    db = SessionLocal()
    try:
        if db.query(Pc).count() > 0:
            print("Ya hay PCs cargados, no se vuelve a hacer seed. Borrá las tablas si querés recargar desde cero.")
            return

        admin = db.query(Usuario).filter(Usuario.rol == "admin").first()

        tecnicos_por_nombre = {}
        for t in TECNICOS_SEED:
            usuario = db.query(Usuario).filter(Usuario.correo == t["correo"]).first()
            if not usuario:
                usuario = Usuario(
                    nombre=t["nombre"],
                    correo=t["correo"],
                    password_hash=hash_password(TECNICO_PASSWORD_DEFAULT),
                    rol="tecnico",
                    activo=True,
                )
                db.add(usuario)
                db.flush()
            tecnicos_por_nombre[t["nombre"]] = usuario
        print(f"{len(tecnicos_por_nombre)} usuarios técnicos listos (contraseña por defecto: '{TECNICO_PASSWORD_DEFAULT}').")

        pcs_creadas = []
        for item in PCS_SEED:
            pc = Pc(
                nro_serie=item["serie"],
                marca=item["marca"],
                modelo=MODELOS_POR_MARCA[item["marca"]],
                estado=item["estado"],
                usuario_asignado=item["usuario"],
            )
            db.add(pc)
            pcs_creadas.append(pc)
        db.flush()
        print(f"{len(pcs_creadas)} PCs cargadas.")

        for item in TAREAS_SEED:
            tarea = Tarea(
                titulo=item["titulo"],
                estado=item["estado"],
                observacion="",
                imagen=None,
                programas=dict(PROGRAMAS_VACIO),
                tecnico_id=admin.id if admin else None,
            )
            db.add(tarea)
        print(f"{len(TAREAS_SEED)} tareas cargadas.")

        for item in INTERVENCIONES_SEED:
            tecnico = tecnicos_por_nombre.get(item["tecnico"])
            intervencion = Intervencion(
                pc_id=pcs_creadas[item["pc_index"]].id,
                tecnico_id=tecnico.id if tecnico else None,
                fecha=datetime.fromisoformat(item["fecha"]),
                estado=item["estado"],
                observacion=item["observacion"],
                acciones=item["acciones"],
                usuarios=item["usuarios"],
                fotos=[],
            )
            db.add(intervencion)
        print(f"{len(INTERVENCIONES_SEED)} intervenciones cargadas.")

        for item in CELULARES_SEED:
            celular = Celular(**item)
            db.add(celular)
        print(f"{len(CELULARES_SEED)} celulares cargados.")

        db.commit()
        print("Seed completo.")
    finally:
        db.close()


if __name__ == "__main__":
    seed()
