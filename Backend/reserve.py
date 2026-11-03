#IMPORTACION DE LIBRERIÁS
# Ajuste reciente: permite consultar y cancelar reservas propias sin borrar
# el historial; los turnos cancelados vuelven a quedar disponibles.
import json
import re
import unicodedata
from datetime import date, time, timedelta
from pathlib import Path

from jinja2 import Template

#IMPORTACION DE ARCHIVOS LOCALES
from reader import read_courts

RESERVATIONS_FILE = Path(__file__).resolve().parent / "reservations.json"
DURACION_TURNO = timedelta(hours=1)


class TurnoOcupadoError(ValueError):
    # Permite manejar un choque de horario distinto de otros datos inválidos.
    pass


def _validate_date(value: str) -> str:
    # Primero valida el formato y luego que la fecha exista en el calendario.
    if not re.fullmatch(r"\d{4}-\d{2}-\d{2}", value):
        raise ValueError("La fecha debe tener el formato AAAA-MM-DD.")
    try:
        return date.fromisoformat(value).isoformat()
    except ValueError as error:
        raise ValueError("La fecha ingresada no es válida.") from error


def _validate_time(value: str) -> str:
    # Devuelve la hora en formato uniforme HH:MM para compararla y guardarla.
    if not re.fullmatch(r"\d{2}:\d{2}", value):
        raise ValueError("El horario debe tener el formato HH:MM.")
    try:
        return time.fromisoformat(value).isoformat(timespec="minutes")
    except ValueError as error:
        raise ValueError("El horario ingresado no es válido.") from error


def _read_reservations(path: Path) -> list[dict]:
    # Las reservas se manejan como una lista de diccionarios, uno por turno.
    if not path.exists():
        return []

    with path.open("r", encoding="utf-8-sig") as file:
        reservations = json.load(file)

    if not isinstance(reservations, list) or not all(
        isinstance(reservation, dict) for reservation in reservations
    ):
        raise ValueError("El archivo de reservas debe contener una lista de objetos.")
    return reservations


def _hora_a_minutos(hora: str) -> int:
    # Convierte el horario a minutos desde medianoche para simplificar cálculos.
    coincidencia = re.fullmatch(
        r"\s*(\d{1,2})(?::(\d{2}))?\s*(am|pm)?\s*",
        hora.lower(),
    ) # hice quick para esta parte de horarios 
    if coincidencia is None:
        raise ValueError("El horario de atención de la cancha no tiene un formato válido.")

    horas = int(coincidencia.group(1))
    minutos = int(coincidencia.group(2) or 0)
    sufijo = coincidencia.group(3)
    if minutos > 59 or horas > 24:
        raise ValueError("El horario de atención de la cancha no es válido.")
    # Algunos datos usan "20pm"; las horas mayores a 12 ya están en formato 24 h.
    if sufijo and horas <= 12:
        horas = horas % 12 + (12 if sufijo == "pm" else 0)
    if horas == 24 and minutos:
        raise ValueError("El horario de atención de la cancha no es válido.")
    return horas * 60 + minutos


def _horario_atencion(court: dict) -> tuple[int, int]:
    # Busca en los textos de atención el primer rango de apertura y cierre.
    horarios = court.get("hs", [])
    for detalle in horarios:
        coincidencia = re.search(
            r"(\d{1,2}(?::\d{2})?\s*(?:am|pm)?)\s+a\s+"
            r"(\d{1,2}(?::\d{2})?\s*(?:am|pm)?)",
            detalle.lower(),
        )
        if coincidencia:
            apertura = _hora_a_minutos(coincidencia.group(1))
            cierre = _hora_a_minutos(coincidencia.group(2))
            if cierre <= apertura:
                raise ValueError("El horario de cierre debe ser posterior a la apertura.")
            return apertura, cierre
    raise ValueError("No se pudo interpretar el horario de atención de la cancha.")


def _dias_atencion(court: dict) -> set[int] | None:
    # El mapa permite convertir los nombres de días a weekday() (lunes=0).
    dias = {
        "lunes": 0,
        "martes": 1,
        "miercoles": 2,
        "jueves": 3,
        "viernes": 4,
        "sabado": 5,
        "domingo": 6,
    }
    # Un conjunto guarda los días abiertos sin repetirlos.
    dias_configurados: set[int] = set()
    tiene_dias = False

    for detalle in court.get("hs", []):
        # Se quitan tildes para comparar nombres como "miércoles" con el mapa.
        normalizado = unicodedata.normalize("NFD", detalle.lower())
        normalizado = "".join(
            letra for letra in normalizado if unicodedata.category(letra) != "Mn"
        )
        coincidencia = re.search(
            r"\b(lunes|martes|miercoles|jueves|viernes|sabados?|domingos?)"
            r"\s+a\s+"
            r"(lunes|martes|miercoles|jueves|viernes|sabados?|domingos?)\b",
            normalizado,
        )
        if coincidencia:
            tiene_dias = True
            primer_dia = coincidencia.group(1)
            ultimo_dia = coincidencia.group(2)
            # Solo "sábados" y "domingos" aparecen en plural en estos rangos.
            if primer_dia in ("sabados", "domingos"):
                primer_dia = primer_dia[:-1]
            if ultimo_dia in ("sabados", "domingos"):
                ultimo_dia = ultimo_dia[:-1]
            inicio = dias[primer_dia]
            fin = dias[ultimo_dia]
            # Avanza por la semana y admite rangos que cruzan el domingo.
            dia = inicio
            while True:
                dias_configurados.add(dia)
                if dia == fin:
                    break
                dia = (dia + 1) % 7

    return dias_configurados if tiene_dias else None


def _horarios_de_una_hora(court: dict, booking_date: str) -> list[str]:
    # Genera los inicios permitidos antes de quitar los que ya están ocupados.
    fecha = date.fromisoformat(_validate_date(booking_date))
    dias_atencion = _dias_atencion(court)
    if dias_atencion is not None and fecha.weekday() not in dias_atencion:
        return []

    apertura, cierre = _horario_atencion(court)
    # Cada inicio debe dejar una hora completa antes del cierre.
    primer_inicio = (apertura + 59) // 60
    ultimo_inicio = (cierre - int(DURACION_TURNO.total_seconds() // 60)) // 60
    return [
        f"{hora:02d}:00"
        for hora in range(primer_inicio, ultimo_inicio + 1)
    ]


def _reserva_ocupa_horario(
    reserva: dict,
    court_id: int,
    booking_date: str,
    booking_time: str,
) -> bool:
    # Solo compiten reservas activas de la misma cancha y fecha.
    if (
        reserva.get("court_id") != court_id
        or reserva.get("date") != booking_date
        or reserva.get("status", "active") != "active"
    ):
        return False

    hora_reservada = time.fromisoformat(_validate_time(str(reserva.get("time", ""))))
    hora_solicitada = time.fromisoformat(booking_time)
    inicio_reserva = hora_reservada.hour * 60 + hora_reservada.minute
    inicio_solicitado = hora_solicitada.hour * 60 + hora_solicitada.minute
    duracion = int(DURACION_TURNO.total_seconds() // 60)
    # Dos intervalos se solapan si cada uno empieza antes de que termine el otro.
    return (
        inicio_solicitado < inicio_reserva + duracion
        and inicio_reserva < inicio_solicitado + duracion
    )


def available_times(
    court: dict,
    booking_date: str,
    *,
    reservations_file: Path = RESERVATIONS_FILE,
) -> list[str]:
    # Filtra los horarios de atención usando las reservas guardadas.
    horarios = _horarios_de_una_hora(court, booking_date)
    reservas = _read_reservations(reservations_file)
    return [
        horario
        for horario in horarios
        if not any(
            _reserva_ocupa_horario(
                reserva,
                court["id"],
                _validate_date(booking_date),
                horario,
            )
            for reserva in reservas
        )
    ]


# Devuelve solo las reservas activas del usuario identificado en la sesión.
def user_reservations(
    user: dict,
    *,
    reservations_file: Path = RESERVATIONS_FILE,
) -> list[dict]:
    # El ID de sesión limita la consulta a las reservas de este usuario.
    user_id = user.get("id")
    if not isinstance(user_id, int) or isinstance(user_id, bool):
        raise ValueError("No se pudo identificar al usuario de la sesión.")

    reservations = _read_reservations(reservations_file)
    return [
        reservation
        for reservation in reservations
        if reservation.get("user_id") == user_id
        and reservation.get("status", "active") == "active"
    ]


# Marca como cancelada una reserva propia para conservar el historial y liberar el turno.
def cancel_reservation(
    user: dict,
    reservation_number: int,
    *,
    reservations_file: Path = RESERVATIONS_FILE,
) -> dict:
    # El número elegido corresponde a la posición en la lista de reservas activas.
    user_id = user.get("id")
    if not isinstance(user_id, int) or isinstance(user_id, bool):
        raise ValueError("No se pudo identificar al usuario de la sesión.")
    if not isinstance(reservation_number, int) or isinstance(reservation_number, bool):
        raise ValueError("El número de reserva no es válido.")

    reservations = _read_reservations(reservations_file)
    reservas_usuario = [
        reservation
        for reservation in reservations
        if reservation.get("user_id") == user_id
        and reservation.get("status", "active") == "active"
    ]
    if not 1 <= reservation_number <= len(reservas_usuario):
        raise ValueError("No existe una reserva activa con ese número.")

    reserva_elegida = reservas_usuario[reservation_number - 1]
    # Se conserva el registro y se libera el turno cambiando solo su estado.
    reserva_elegida["status"] = "cancelled"
    with reservations_file.open("w", encoding="utf-8") as file:
        json.dump(reservations, file, ensure_ascii=False, indent=4)
        file.write("\n")
    return reserva_elegida


def create_reservation(
    user: dict,
    court_id: int,
    booking_date: str,
    booking_time: str,
    *,
    reservations_file: Path = RESERVATIONS_FILE,
) -> dict:
    # Valida primero la identidad y los datos para no guardar reservas incompletas.
    user_id = user.get("id")
    username = user.get("username")
    if (
        not isinstance(user_id, int)
        or isinstance(user_id, bool)
        or not isinstance(username, str)
        or not username.strip()
    ):
        raise ValueError("No se pudo identificar al usuario de la sesión.")
    if not isinstance(court_id, int) or isinstance(court_id, bool):
        raise ValueError("El identificador de la cancha no es válido.")

    normalized_date = _validate_date(booking_date)
    normalized_time = _validate_time(booking_time)

    courts = read_courts()
    court = next((item for item in courts if item.get("id") == court_id), None)
    if court is None:
        raise ValueError("No existe una cancha con ese identificador.")
    if court.get("available") is not True:
        raise ValueError("La cancha no está habilitada para reservar.")

    horarios = _horarios_de_una_hora(court, normalized_date)
    if normalized_time not in horarios:
        raise ValueError(
            "Elegí un turno de una hora disponible dentro del horario de atención."
        )

    # Comprueba conflictos antes de agregar la nueva reserva a la lista.
    reservations = _read_reservations(reservations_file)
    if any(
        _reserva_ocupa_horario(
            reservation,
            court_id,
            normalized_date,
            normalized_time,
        )
        for reservation in reservations
    ):
        raise TurnoOcupadoError(
            "Ese turno ya está reservado para la cancha seleccionada."
        )

    court_data = court.get("data", [])
    court_name = court_data[0] if court_data else f"Cancha {court_id}"
    reservation = {
        "user_id": user_id,
        "username": username.strip(),
        "court_id": court_id,
        "court_name": court_name,
        "date": normalized_date,
        "time": normalized_time,
        "status": "active",
    }
    reservations.append(reservation)
    with reservations_file.open("w", encoding="utf-8") as file:
        json.dump(reservations, file, ensure_ascii=False, indent=4)
        file.write("\n")
    return reservation


def confirm_court(court: dict, user: dict) -> bool:
    # Repite la solicitud de fecha si el formato es incorrecto o no hay horarios.
    while True:
        booking_date = input("Ingrese la fecha (AAAA-MM-DD): ").strip()
        try:
            _validate_date(booking_date)
        except ValueError as error:
            print(error)
            continue

        try:
            horarios_disponibles = available_times(court, booking_date)
        except (OSError, json.JSONDecodeError, ValueError) as error:
            print(f"No se pudieron consultar los horarios: {error}")
            return False
        if not horarios_disponibles:
            print("No hay turnos disponibles para esa fecha.")
            continue

        plantilla_horarios = """
TURNOS DISPONIBLES (1 HORA)
{% for horario in horarios %}
{{ loop.index }} - {{ horario }}
{% endfor %}
        """
        print(Template(plantilla_horarios).render(horarios=horarios_disponibles))
        # La persona elige el índice mostrado; se traduce al horario real.
        while True:
            try:
                numero_horario = int(input("Elija el número de horario: "))
                if 1 <= numero_horario <= len(horarios_disponibles):
                    booking_time = horarios_disponibles[numero_horario - 1]
                    break
                print("X - OPCIÓN FUERA DE RANGO - X")
            except ValueError:
                print("X - INGRESE SOLO NÚMEROS - X")

        plantilla = """
* CONFIRMACION DE RESERVA *
    
PARA CONFIRMAR SU RESERVA DEBE INGRESAR SI/NO
    """
        mi_plantilla= Template(plantilla)
        print(mi_plantilla.render())
        answer = str(input("").strip().lower())
        match answer:
            case "si":
                try:
                    reservation = create_reservation(
                        user,
                        court["id"],
                        booking_date,
                        booking_time,
                    )
                except TurnoOcupadoError as error:
                    print(error)
                    continue
                except (OSError, json.JSONDecodeError, ValueError) as error:
                    print(f"No se pudo completar la reserva: {error}")
                    return False

                plantilla = """ 
* RESERVA CONFIRMADA *
SU RESERVA HA SIDO CONFIRMADA CON EXITO
            """
                mi_plantilla = Template(plantilla)
                print(mi_plantilla.render())
                detalles_reserva = """
CANCHA: {{ court_name | upper }}
FECHA: {{ date }}    HORARIO: {{ time }}
                """
                print(Template(detalles_reserva).render(reservation))
                return True
            case "no":
                print("-----------------------------------------------------")
                print("                  RESERVA ANULADA                    ")
                print("-----------------------------------------------------")
                return False
            case _ :
                print("-----------------------------------------------------")    
                print("        X - RESPUESTA INCORRECTA - USE SI/NO X       ")
                print("-----------------------------------------------------")


def choose_court(courts: list[dict], user: dict) -> None:
    while True:
        try:
            option = int(input(""))
            if 1 <= option <= len(courts):
                selected_court = courts[option - 1]
                break
            print("x - OPCION FUERA DE RANGO - X")
        except ValueError:
            print("ERROR - INGRESE SOLO NÚMEROS")

    plantilla ="""
* DETALLES DEL LUGAR *
    
{{ data | join(',') | upper }}
{{ info | upper }}
TEL: {{ phone | join(',') }}
CANTIDAD DE CANCHAS: {{ courts }}
PAREDES: {{ walls | upper }}
TIENDA: {{ "SI INCLUYE" if shop else "NO INCLUYE" }}
ENTRENADOR: {{ "DISPONIBLES" if trainer else "NO DISPONIBLES" }}
            """
    mi_plantilla= Template(plantilla)
    print(mi_plantilla.render(selected_court))
    confirm_court(selected_court, user)


def court_list(user: dict) -> None:
    try:
        courts = read_courts()
    except (OSError, json.JSONDecodeError, ValueError) as error:
        print(f"No se pudieron cargar las canchas: {error}")
        return

    available_courts = [
        court for court in courts if court.get("available") is True
    ]
    not_available_courts = [
        court for court in courts if court.get("available") is not True
    ]
    if not available_courts:
        print("No hay canchas habilitadas para reservar.")
        return

    plantilla = """
-----------------------------------------------------------------                  
CANCHAS DISPONIBLES PARA RESERVAR
    
{% for info in cancha -%}
{{ loop.index }} (INGRESE {{ loop.index }}) - {{ info.data | join(',') | upper }}
HORARIOS: {{ info.hs | join(',') | upper }}
Tel: {{ info.phone | join(',') | upper }}
-----------------------------------------------------------------
{% endfor %}
-----------------------------------------------------------------
CANCHAS NO DISPONIBLES
    
{% for info in not_available_courts -%}
{{ loop.index }} {{ info.data | join(',') | upper  }}
HORARIOS: {{ info.hs | join(',') | upper }}
Tel: {{ info.phone | join(',') }}
----------------------------------------------------------------
{% endfor %}
    
-------- INGRESE EL NUMERO DE LA CANCHA QUE DESEA ELEGIR -------
    """
    mi_plantilla = Template(plantilla)
    print(
        mi_plantilla.render(
            cancha=available_courts,
            not_available_courts=not_available_courts,
        )
    )
    choose_court(available_courts, user)


# Muestra todas las canchas con su estado, sin iniciar una reserva.
def show_all_courts() -> None:
    try:
        courts = read_courts()
    except (OSError, json.JSONDecodeError, ValueError) as error:
        print(f"No se pudieron cargar las canchas: {error}")
        return

    plantilla = """
TODAS LAS CANCHAS
{% for cancha in canchas %}
{{ loop.index }} - {{ cancha.data | join(',') | upper }}
HORARIOS: {{ cancha.hs | join(', ') | upper }}
ESTADO: {{ "HABILITADA" if cancha.available else "NO DISPONIBLE" }}
-----------------------------------------------------------------
{% endfor %}
"""
    print(Template(plantilla).render(canchas=courts))
    while input("Seleccione 0 para regresar al menú: ").strip() != "0":
        print("Opción inválida. Ingrese 0 para regresar.")
