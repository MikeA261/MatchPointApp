from jinja2 import Template
from main import my_funtion
from reader import read_user
from reader import read_courts

def show_reserv(court: dict):
    return

def cancel_and_active():
    return
def modify_info():
    return

def menu_a(court: dict):
    try:
        plantilla= """
--------------------------------------------------------
                MENU ADMINISTRATIVO
--------------------------------------------------------
1 VER TURNOS RESERVADOS
2 DAR DE BAJA/ALTA
3 MODIFICAR INFORMACION
4 SALIR

    """
        mi_plantilla = Template(plantilla)
        print(mi_plantilla.render())
        opcion = int(input())
        match opcion:
            case 1:
                show_reserv(court)         
            case 2:
                cancel_and_active()
            case 3:
                modify_info()
            case 4:
                my_funtion()
            case _ :
                print("-----------------------------------------------------")
                print("            x - OPCION FUERA DE RANGO - x            ")
                print("-----------------------------------------------------")  
                menu_a() 
    except ValueError:
            print("X - ERROR MENU - INGRESE SOLO NUMEROS - X")
            menu_a()
    finally:
        pass
    

    return