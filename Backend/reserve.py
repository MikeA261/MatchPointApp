#IMPORTACION DE LIBRERIÁS
from jinja2 import Template

#IMPORTACION DE ARCHIVOS LOCALES
from reader import read_courts
from modify_court import change_availible
def back_menu():
    from menu.menu import menu

def confirm_court(court: dict):
    entry = True
    while entry:
        plantilla = """
* CONFIRMACION DE RESERVA *
    
PARA CONFIRMAR SU RESERVA DEBE INGRESAR SI/NO
    """
        mi_plantilla= Template(plantilla)
        print(mi_plantilla.render())
        answer = str(input("").strip().lower())
        match answer:
            case "si":
                plantilla = """ 
* RESERVA CONFIRMADA *
SU RESERVA HA SIDO CONFIRMADA CON EXITO
            """
                mi_plantilla = Template(plantilla)
                print(mi_plantilla.render())
                change_availible(court,answer)
                break
            case "no":
                print("-----------------------------------------------------")
                print("                  RESERVA ANULADA                    ")
                print("-----------------------------------------------------")
                back_menu()
                break
            case _ :
                print("-----------------------------------------------------")    
                print("        X - RESPUESTA INCORRECTA - USE SI/NO X       ")
                print("-----------------------------------------------------")
                    
def choose_court(court: list[dict]):
    while True:
        try:
            option= int(input(""))
            if 1 <= option <= len(court):
                availible_court = court[option - 1] 
                break
            else:
                print("x - OPCION FUERA DE RANGO - X")
        except(ValueError, IndexError):
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
    print(mi_plantilla.render(availible_court))
    confirm_court(availible_court)
    return 

def court_list():
    court = read_courts()
    avalible_courts = [info for info in court if info['available']]
    not_availible_courts = [info for info in court if not info.get('available')]    
    plantilla = """
-----------------------------------------------------------------                  
CANCHAS DISPONIBLES PARA RESERVAR
    
{% for info in cancha -%}
{{ loop.index }} {{ info.data | join(',') | upper  }}
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
    
------- INGRESE EL NUMERO DE LA CANCHA QUE DESEA ELEGIR -------
    """
    mi_plantilla = Template(plantilla)
    print(mi_plantilla.render(cancha = avalible_courts, not_available_courts = not_availible_courts))
    choose_court(avalible_courts)
    return 