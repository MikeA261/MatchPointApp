#Importaciones de librerias 
# este se da cuando ya has iniciado sesion !!
# Ajuste reciente: la opción de reservas muestra las del usuario y permite
# cancelar una propia.
import json

from jinja2 import Template

#Importaciones de archivos locales
from main import my_funtion
from reserve import (
    cancel_reservation,
    court_list,
    show_all_courts,
    user_reservations,
)


# Muestra las reservas del usuario y permite cancelar una; 0 vuelve sin cambios.
def cancel_court(user: dict) -> None:
    try:
        reservas = user_reservations(user)
    except (OSError, json.JSONDecodeError, ValueError) as error:
        print(f"No se pudieron cargar tus reservas: {error}")
        return

    if not reservas:
        print("No tenés reservas activas.")
        return

    plantilla_reservas = """
TUS RESERVAS ACTIVAS
{% for reserva in reservas %}
{{ loop.index }} - {{ reserva.court_name }} | {{ reserva.date }} | {{ reserva.time }}
{% endfor %}
"""
    print(Template(plantilla_reservas).render(reservas=reservas))
    try:
        numero = int(input("Número de reserva a cancelar (0 para volver): "))
        if numero == 0:
            return
        cancel_reservation(user, numero)
    except ValueError as error:
        print(f"No se pudo cancelar la reserva: {error}")
        return
    except (OSError, json.JSONDecodeError) as error:
        print(f"No se pudo guardar la cancelación: {error}")
        return

    print("RESERVA CANCELADA. EL TURNO VOLVIÓ A ESTAR DISPONIBLE.")
    while input("Ingresa 0 para regresar al menú: ").strip() != "0":
        print("Opción inválida. Ingresa 0 para regresar.")

def my_acount():
    return print("ok")

def menu(user: list):
    plantilla = """
===================================================================
         MATCH POINT   ---------   JUGÁ SEGURO - JUGÁ SANO
===================================================================
{{ name | upper }} ¿QUE NECESITAS?
------------------------------------------------------------------- 
1 RESERVAR UN TURNO
2 VER / CANCELAR MIS RESERVAS
3 VER TODAS LAS CANCHAS
4 MI CUENTA
5 CERRAR SESIÓN
------------------------------------------------------------------- 
    """
    mi_plantilla = Template(plantilla)
    while True:
        print(mi_plantilla.render(user[0]))
        try:
            opcion= int(input(""))
            match opcion:
                case 1:
                    court_list(user[0])
                case 2:
                    cancel_court(user[0])
                case 3:
                    show_all_courts()
                case 4: 
                    my_acount
                case 5:
                    print("-----------------------------------------------------")
                    print("         CERRANDO SESIÓN ------ HASTA LUEGO          ")
                    print("-----------------------------------------------------")
                    my_funtion()
                    break
                case _ :
                    print("-----------------------------------------------------")
                    print("         x - OPCIÓN NO FUERA DE RANGO - X            ")
                    print("-----------------------------------------------------")
        except ValueError:
            print("-----------------------------------------------------")
            print("        X - ERROR - INGRESE SOLO NÚMEROS - X         ")
            print("-----------------------------------------------------")    
    return