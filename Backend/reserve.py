from jinja2 import Template

def choose_court(court: list[dict]):
    try:
        opcion= int(input("    "))
        information = court[opcion - 1 ]
        plantilla ="""
    {{ info | upper }}
    ESTADO: {{ 'DISPONIBLE PARA RESERVAR' if available else 'NO DISPONIBLE - ELIJA OTRA OPCION' }}
    """
        mi_plantilla= Template(plantilla)
        print(mi_plantilla.render(information))
    except(ValueError):
        print("OPCION FUERA DE RANGO")
    except(TypeError):
        print("OPCION NO VALIDA")
    finally:
        pass
    return