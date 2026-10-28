from jinja2 import Template
from courts import read_courts


def choose_court(court: list[dict]):
    try:
        option= int(input("    "))
        if option >= 1 and option <= len(court):
            availible_court = court[option - 1]
            information = availible_court
            plantilla ="""
            DETALLE DEL LUGAR
            """
            mi_plantilla= Template(plantilla)
            print(mi_plantilla.render(information))
    except(ValueError):
        print("OPCION FUERA DE RANGO")
    except(TypeError):
        print("OPCION NO VALIDA")
    finally:
        pass
    return print(availible_court)

def court_list():
    court = []
    court = read_courts(court)
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