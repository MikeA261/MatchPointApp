from jinja2 import Template
from main import my_funcion
from courts import read_courts
from reserve import choose_court


def court_reservation():
    court = []
    court = read_courts(court)
    
    plantilla = """
    -----------------------------------------------------------------
                         
    Listado de canchas 
    {% set acumulador = namespace(contador=0) %}
    {% for info in cancha -%}
        {% set acumulador.contador = acumulador.contador + 1 %}
    {{ acumulador.contador }} {{ info.data | join(',') | upper  }}
    HORARIOS: {{ info.hs | join(',') | upper }}
    ESTADO: {{ 'DISPONIBLE' if info.available else 'NO DISPONIBLE' }}
    {% endfor %}
    -----------------------------------------------------------------
    INGRESE EL NUMERO DE LA CANCHA QUE DESEA ELEGIR:
    """
    mi_plantilla = Template(plantilla)
    print(mi_plantilla.render(cancha = court))
    choose_court(court)
    return 

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
                court_reservation()
            case 2:
                cancel_court()
            case 3:
                my_acount()
            case 4:
                my_funcion()
    except ValueError():
        print("OPCIÓN NO VÁLIDA")
                
    return