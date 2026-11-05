import json
from datetime import datetime
from pathlib import Path

from jinja2 import Template


# Guarda el historial junto al backend y limita cada vista para evitar listas largas.
NOTIFICATIONS_FILE = Path(__file__).resolve().parent / "notifications.json"
NOTIFICATIONS_PER_PAGE = 5


def _read_notifications() -> list[dict]:
    # La ausencia del archivo equivale a un historial vacío; el primer aviso lo crea.
    if not NOTIFICATIONS_FILE.exists():
        return []

    with NOTIFICATIONS_FILE.open("r", encoding="utf-8-sig") as file:
        notifications = json.load(file)
    # Se valida la estructura antes de usar los registros o sobrescribir el archivo.
    if not isinstance(notifications, list) or not all(
        isinstance(notification, dict) for notification in notifications
    ):
        raise ValueError("El archivo de notificaciones debe contener una lista de objetos.")
    return notifications


def add_notification(event: str, reservation: dict) -> None:
    # Conserva los avisos previos y agrega los datos relevantes de la reserva.
    notifications = _read_notifications()
    notifications.append(
        {
            "event": event,
            "username": reservation.get("username", "Usuario desconocido"),
            "court_name": reservation.get("court_name", "Cancha desconocida"),
            "date": reservation.get("date", ""),
            "time": reservation.get("time", ""),
            "created_at": datetime.now().isoformat(timespec="seconds"),
        }
    )
    # Se guarda el historial completo para no descartar eventos anteriores.
    with NOTIFICATIONS_FILE.open("w", encoding="utf-8") as file:
        json.dump(notifications, file, ensure_ascii=False, indent=4)
        file.write("\n")


def show_admin_notifications() -> None:
    try:
        notifications = _read_notifications()
    except (OSError, json.JSONDecodeError, ValueError) as error:
        # Informa el problema y vuelve al menú sin interrumpir el flujo administrativo.
        print(f"No se pudieron cargar las notificaciones: {error}")
        return

    if not notifications:
        print("No hay notificaciones nuevas por ahora.")
        return

    # Las páginas se cuentan desde las más recientes hacia las más antiguas.
    pagina = 0
    total_paginas = (
        len(notifications) + NOTIFICATIONS_PER_PAGE - 1
    ) // NOTIFICATIONS_PER_PAGE
    # La plantilla muestra solo los controles válidos para la página actual.
    plantilla = """
===================================================================
                      NOTIFICACIONES
===================================================================
{% for notificacion in notificaciones %}
{{ loop.index }} - {{ notificacion.event | upper }}
Usuario: {{ notificacion.username }}
Cancha: {{ notificacion.court_name }}
Fecha: {{ notificacion.date }}    Horario: {{ notificacion.time }}
Registrada: {{ notificacion.created_at }}
-------------------------------------------------------------------
{% endfor %}
Página {{ pagina }} de {{ total_paginas }}
{% if pagina < total_paginas %}1 - Ver notificaciones anteriores{% endif %}
{% if pagina > 1 %}2 - Volver a las más recientes{% endif %}
0 - Regresar al menú
"""

    while True:
        # Calcula el segmento de cinco avisos y lo invierte para mostrar el más nuevo primero.
        fin = len(notifications) - pagina * NOTIFICATIONS_PER_PAGE
        inicio = max(0, fin - NOTIFICATIONS_PER_PAGE)
        pagina_actual = list(reversed(notifications[inicio:fin]))
        print(
            Template(plantilla).render(
                notificaciones=pagina_actual,
                pagina=pagina + 1,
                total_paginas=total_paginas,
            )
        )
        # Navega al historial sin cargar de nuevo el archivo ni alterar sus registros.
        opcion = input("Seleccione una opción: ").strip()
        if opcion == "0":
            return
        if opcion == "1" and pagina + 1 < total_paginas:
            pagina += 1
        elif opcion == "2" and pagina > 0:
            pagina -= 1
        else:
            print("Opción fuera de rango.")
