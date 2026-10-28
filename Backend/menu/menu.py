from jinja2 import Template
from main import my_funcion
from reserve import court_list

def cancel_court():
    return print("ok")

def my_acount():
    return print("ok")

def menu(user: list):
    plantilla = """
    ===================================================================
                MATCH POINT   ---------   JUEGA SEGURO Y SANO
    ===================================================================
    {{ name | upper }} ¿Que necesitas?
    ---------------------------------- 
    1 Reservar una cancha
    2 Cancelar un turno
    3 Mi cuenta
    4 CERRAR SESIÓN
    ------------------------------------------------------------------- 
    """
    mi_plantilla = Template(plantilla)
    print(mi_plantilla.render(user[0]))
    
    try:
        opcion= int(input("    "))
        match opcion:
            case 1:
                court_list()
            case 2:
                cancel_court()
            case 3:
                my_acount()
            case 4:
                my_funcion()
    except ValueError():
        print("OPCIÓN NO VÁLIDA")
                
    return