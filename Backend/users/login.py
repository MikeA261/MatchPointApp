import json
import sys
from jinja2 import Template
from menu.menu import menu

def read_dates(dates: list)->list:  
    USER='Matchpoint/Backend/users/user.json'
    try: 
        with open(USER, 'rt', encoding='utf-8-sig') as archivo:
            dates = json.load(archivo)
            return dates
    except FileNotFoundError:
        print(f'El archino no exiiste')
    except(FileExistsError):
        print(f"El archivo no existe")
    finally:
       pass
       
def validate_user(name: str,psw: str)->tuple:
    data= []
    data = read_dates(data)
    
    confirm = any(u.get("name") == name and u.get("psw") == psw for u in data) 
    user = [u for u in data if u.get("psw") == psw]      

    return confirm,user

def welcome(confirm: bool, user: list)-> None:
    
    if confirm:
        plantilla = """
    =================================
            BIENVENIDO {{ name | upper }}
    =================================
    """
        mi_plantilla = Template (plantilla)
        print(mi_plantilla.render(user[0]))
    else:
        plantilla = """
    =================================
    X-ERROR-X LOS DATOS NO COINCIDEN     
    =================================
    """
        mi_plantilla = Template (plantilla)
        print(mi_plantilla.render())
        sys.exit()
        
    menu(user)     
    return

def login_user():
    plantilla = """
    =================================
            MATCH POINT LOGIN
    =================================
    Ingrese su nombre de usuario:
    """
    mi_plantilla = Template (plantilla)
    print(mi_plantilla.render())
    user= str(input("    "))
    
    plantilla2= """
    =================================
            MATCH POINT LOGIN
    =================================
    Ingrese su contraseña: 
    """
    mi_plantilla = Template (plantilla2)
    print(mi_plantilla.render())
    psw= str(input("    "))
    confirm = validate_user(user,psw)
    welcome(confirm[0],confirm[1])