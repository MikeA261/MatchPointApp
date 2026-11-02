#Importaciones de librerias
from jinja2 import Template

#Importaciones de archivos locales
from main import my_funtion
from reserve import court_list

def cancel_court():
    return print("ok")

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
2 CANCELAR UNA RESERVA
3 VER TODAS LAS CANCHAS
4 MI CUENTA
5 CERRAR SESIÓN
------------------------------------------------------------------- 
    """
    mi_plantilla = Template(plantilla)
    print(mi_plantilla.render(user[0]))
    while True:
        try:
            opcion= int(input(""))
            match opcion:
                case 1:
                    court_list()
                    break
                case 2:
                    cancel_court()
                    break
                case 3:
                    pass
                case 4: 
                    my_acount
                    break
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
        except ValueError():
            print("-----------------------------------------------------")
            print("        X - ERROR - INGRESE SOLO NÚMEROS - X         ")
            print("-----------------------------------------------------")    
    return