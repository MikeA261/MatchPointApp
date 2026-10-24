import json
import random as rn

def read_dates(dates):  

    try: 
        with open('Matchpoint/Backend/dates.json' , 'rt', encoding='utf-8-sig') as archivo:
            dates = json.load(archivo)
    except FileNotFoundError:
        print(f'El archino no exiiste')
    except(FileExistsError):
        print(f"El archivo no existe")
    finally:
       dates

def login(user,pws)->list:
    return 

def new_account(dates:list)->list[dict]:

    id = rn.randint(1_000_000,99_000_000)
    firname = str(input(f'Ingrese su nombre:  ')) 
    secname = str(input(f'Ingrese su apellido:  '))
    try: 
        year = int(input("Ingrese su edad:  "))
    except ValueError:
        print("ERROR...Ingrese una edad valida")
    finally:
        year
    psw = str(input("Ingrese su contraseña:  "))
    psw2 = str(input("Confirme su contraseña:  "))
    if psw != psw2:
        print("Registro invalido")
        raise ValueError("Las contraseñas no coinciden")
    
    location = str(input(f'Ingrese la ciudad donde reside actualmente:  '))

    newUser = {
        "id"  : id,
        "name": firname,
        "secname": secname,
        "years": year,
        "psw" : psw,
        "location": location
    }

    dates.append(newUser)
    
    return dates

def write_dates(dates: dict)-> list[dict]:
    
    try:
        with open('Matchpoint/Backend/dates.json', 'w', encoding='utf-8') as archivo:
                json.dump(dates, archivo, ensure_ascii=False, indent=4)
    except(FileNotFoundError):
        print("El archivo no se encuentra")
    except(FileExistsError):
        print("El archivo no existe")
    finally:
        print("Registro completado")