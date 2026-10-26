import json
from jinja2 import Template
import random as rn

def read_dates(dates: list)->list:  
    USER= 'Matchpoint/Backend/users/user.json'
    try: 
        with open(USER , 'rt', encoding='utf-8-sig') as archivo:
            dates = json.load(archivo)
            return dates
    except FileNotFoundError:
        print(f'El archino no exiiste')
    except(FileExistsError):
        print(f"El archivo no existe")
    finally:
       dates


def new_account(dates:list)->list[dict]:
    plantilla = """
    =====================================
            MATCH POINT  REGISTRO
    =====================================
    """
    mi_plantilla = Template (plantilla)
    print(mi_plantilla.render())
    id = rn.randint(100_000_000,999_000_000)
    firname = str(input(f'    Ingrese su nombre:  ')) 
    secname = str(input(f'    Ingrese su apellido:  '))
    try: 
        year = int(input("    Ingrese su edad:  "))
    except ValueError:
        print("ERROR...Ingrese una edad valida")
    finally:
        year
    psw = str(input("    Ingrese su contraseña:  "))
    psw2 = str(input("    Confirme su contraseña:  "))
    if psw != psw2:
        print("Registro invalido")
        raise ValueError("Las contraseñas no coinciden")
    location = str(input(f'    Ingrese la ciudad donde reside actualmente:  '))

    newUser = {"id"  : id,
        "name": firname,
        "psw" : psw,
        "user": {
        "secname": secname,
        "years": year,
        "location": location}
    }
    
    dates.append(newUser)
    
    platilla = """
    ===================================
        !REGISTRO COMPLETADO! 
        BIENVENIDO  {{ name | upper }}
    ===================================    
    """
    tempalte = Template(platilla)
    print(tempalte.render(newUser))
    return dates

def write_dates(dates: dict)-> list[dict]:
    USER= 'Matchpoint/Backend/users/user.json'
    try:
        with open(USER, 'w', encoding='utf-8') as archivo:
                json.dump(dates, archivo, ensure_ascii=False, indent=4)
    except(FileNotFoundError):
        print("El archivo no se encuentra")
    except(FileExistsError):
        print("El archivo no existe")
    finally:
        pass