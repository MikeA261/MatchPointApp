import json
from jinja2 import Template
import random as rn
from main import my_funcion

def read_dates(dates: list)->list:  
    USER= 'PadelApp/MatchPointApp/Backend/users/user.json'
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


def write_dates(dates: dict)-> list[dict]:
    USER= 'PadelApp/MatchPointApp/Backend/users/user.json'
    try:
        with open(USER, 'w', encoding='utf-8') as archivo:
                json.dump(dates, archivo, ensure_ascii=False, indent=4)
    except(FileNotFoundError):
        print("El archivo no se encuentra")
    except(FileExistsError):
        print("El archivo no existe")
    finally:
        pass
    
def new_account():
    date = []
    dates = read_dates(date)
    entrada_valida = False
    
    plantilla = """
    =====================================
            MATCH POINT  REGISTRO
    =====================================
    """
    mi_plantilla = Template (plantilla)
    print(mi_plantilla.render())
    id = rn.randint(100_000_000,999_000_000)
    username= str(input(f'    Ingrese su nombre de usuario:  ')).lower()
    firname = str(input(f'    Ingrese su nombre:  ')).lower()
    secname = str(input(f'    Ingrese su apellido:  ')).lower()
    while not entrada_valida:   
        try: 
            year = int(input("    Ingrese su edad:  "))
            if year > 8 and year < 90:
                entrada_valida = True
            else:
                print("    ERROR...INGRESE UNA EDAD ENTRE 8 Y 90")
        except(ValueError):
            print("ERROR...INGRESE NUMEROS ENTEROS")
    
    psw = str(input("    Ingrese su contraseña:  "))
    psw2 = str(input("    Confirme su contraseña:  "))
    confirm = psw == psw2
    while confirm != True:
        print("    ERROR...LAS CONTRASEÑAS NO COINCIDEN")
        psw = str(input("    Ingrese su contraseña:  "))
        psw2 = str(input("    Confirme su contraseña:  "))
        if psw == psw2:
            confirm = True
    location = str(input("    Ingrese la ciudad donde reside actualmente:  ")).lower()

    newUser = {"id"  : id,
        "username": username,
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
    write_dates(dates)
    my_funcion()
    return dates