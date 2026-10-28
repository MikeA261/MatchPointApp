import json
from jinja2 import Template
from menu.menu import menu
from main import my_funcion

def read_dates(dates: list)->list:  
    USER='PadelApp/MatchPointApp/Backend/users/user.json'
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
       
def validate_user(usrname: str,psw: str)->tuple:
    data= []
    data = read_dates(data)
    
    confirm = any(u.get("username") == usrname and u.get("psw") == psw for u in data) 
    user = [u for u in data if u.get("psw") == psw and u.get("username") == usrname]      
    welcome(confirm,user)
    return

def welcome(confirm: bool, user: list)-> None:
    
    if confirm:
        plantilla = """
    ========================================================
                BIENVENIDO {{ name | upper }}
    ========================================================
    """
        mi_plantilla = Template (plantilla)
        print(mi_plantilla.render(user[0]))
        menu(user) 
    else:
        plantilla = """
    ========================================================
                X-ERROR-X LOS DATOS NO COINCIDEN     
    ========================================================
    """
        mi_plantilla = Template (plantilla)
        print(mi_plantilla.render())
        my_funcion()  
    return

def login_user():
    plantilla = """
    =======================================================
            MATCH POINT     -----    LOGIN USUARIO
    =======================================================
    Ingrese su nombre de usuario:
    """
    mi_plantilla = Template (plantilla)
    print(mi_plantilla.render())
    user= str(input("    ")).lower()
    
    plantilla2= """
    =======================================================
            MATCH POINT     ----    LOGIN CONTRASEÑA
    =======================================================
    Ingrese su contraseña: 
    """
    mi_plantilla = Template (plantilla2)
    print(mi_plantilla.render())
    psw= str(input("    "))
    validate_user(user,psw)
