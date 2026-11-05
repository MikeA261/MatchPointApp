#Importaciones de librerias
from jinja2 import Template
import json

#Importaciones de archivos locales
from main import my_funtion
from reserve import (court_list, cancel_reservation, user_reservations)
from reader import read_courts

def view_one_court(option: int, data: list[dict], user: dict):
    choosed_court = data[option - 1]
    plantilla_cancha = """
    ------------------------------------------------------
{{ data | join(',') | upper }}
DIRECCION: {{ street | join(',') | upper }}
HORARIOS: {{ hs | join(',') }}
TELEFONO: {{ phone | join(',') | upper }}
PAREDES: {{ walls | upper }}
CANTIDAD DE CANCHAS: {{ courts }}
TIENDA: {{ "DISCPONIBLE" if shop else "NO POSEE" }}
ENTRENADOR: {{ "DISPONIBLE" if trainer else "NO DISPONIBLE" }}
DESCRIPCION: {{ info | upper }}
{{ "DISPONIBLE PARA RESERVAR" if available else ""}}
----------------------------------------------------------
0 <- ATRAS
    
                    """
    mi_plantilla_cancha = Template(plantilla_cancha)
    print(mi_plantilla_cancha.render(choosed_court))
    while True:
        try:
            back = int(input(""))
            if back == 0:
                return all_courts(user)
            else:
                print("X - OPCION INVALIDA - X")
        except ValueError:
            print("X - USE SOLO NÚMEROS - X")

def cancel_court(user: dict):
    try:
        reservas = user_reservations(user)
    except (OSError, json.JSONDecodeError, ValueError) as error:
        print(f"No se pudieron cargar tus reservas: {error}")
        return

    if not reservas:
        print("No tenés reservas activas.")
        while input("Ingresa 0 para regresar al menú: ").strip() == "0":
            return menu(user)
        

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
            return menu(user)
        cancel_reservation(user, numero)
    except ValueError as error:
        print(f"No se pudo cancelar la reserva: {error}")
        return
    except (OSError, json.JSONDecodeError) as error:
        print(f"No se pudo guardar la cancelación: {error}")
        return

    print("RESERVA CANCELADA. EL TURNO VOLVIÓ A ESTAR DISPONIBLE.")
    while input("Ingresa 0 para regresar al menú: ").strip() == "0":
        return menu(user)

def my_acount(user: dict):
    return print("ok")

def all_courts(user: dict):
    try:
        data = read_courts()
        plantilla = """
----------------------------------------------------
{% for info in courts -%}
{{ loop.index }} {{ info.data | join(',') | upper }}
DIRECCIÓN: {{ info.street | join(',') | upper }}
HORARIOS: {{ info.hs | join(',') | upper }}
Tel: {{ info.phone | join(',') | upper }}
----------------------------------------------------
{% endfor %}   
PARA MÁS INFORMACION SELECCIONE UNA CON SU NÚMERO CORRECTO

0 <- ATRAS

    """
        mi_plantilla = Template(plantilla)
        print(mi_plantilla.render(courts = data))
        while True:
            option = int(input("-> "))
            if 1 <= option <= len(data):
                view_one_court(option, data,user)
            elif option == 0:
                menu(user)
            else:
                print("X - OPCION INVALIDA - X")
    except ValueError:
        print("X - ERROR - SOLO USE NÚMEROS - X")
        
def menu(user: dict):
    plantilla = """
===================================================================
         MATCH POINT   ---------   JUGÁ SEGURO - JUGÁ SANO
===================================================================
{{ name | upper }} ¿QUE NECESITAS?
------------------------------------------------------------------- 
1 RESERVAR UN TURNO
2 VER / CANCELAR RESERVA/S
3 VER TODAS LAS CANCHAS
4 MI CUENTA
5 CERRAR SESIÓN
------------------------------------------------------------------- 
    """
    mi_plantilla = Template(plantilla)
    print(mi_plantilla.render(user))
    while True:
        try:
            opcion= int(input(""))
            match opcion:
                case 1:
                    court_list(user)
                    break
                case 2:
                    cancel_court(user)
                    break
                case 3:
                    all_courts(user)
                    break
                case 4: 
                    my_acount(user)
                    break
                case 5:
                    plantilla_exit= """
-----------------------------------------------------------------
            CERRANDO SESIÓN - HASTA LUEGO {{ name | upper}}
-----------------------------------------------------------------                    
                    """
                    mostrar_exit= Template(plantilla_exit)
                    print(mostrar_exit.render(user))
                    my_funtion()
                    break
                case _ :
                    print("         x - OPCIÓN NO FUERA DE RANGO - X            ")
        except ValueError:
            print("        X - ERROR - INGRESE SOLO NÚMEROS - X         ") 