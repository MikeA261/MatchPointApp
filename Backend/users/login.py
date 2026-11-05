#IMPORTACION DE LIBRERÍAS
from jinja2 import Template

#IMPORTACIONES DE ARCHIVOS LOCALES
from menu.menu_user import menu
from main import my_funtion
from reader import read_user
       
def save_user(usrname: str,psw: str, data: list)->dict:
    user = next((u for u in data if u["psw"] == psw and u["username"] == usrname), None) 
    welcome(user)
    return

def welcome(user: dict)-> None:
    plantilla = """
========================================================
            BIENVENIDO: {{ name | upper }}
========================================================
    """
    mi_plantilla = Template (plantilla)
    print(mi_plantilla.render(user))
    menu(user) 
    return

def login_user():
    data = read_user() 
    plantilla = """
=======================================================
        MATCH POINT     -----    LOGIN USUARIO
=======================================================
Ingrese su nombre de usuario:
    """
    mi_plantilla = Template (plantilla)
    print(mi_plantilla.render())
    while True:
        user= str(input("")).lower()
        confirm = any(u for u in data if u.get("username") == user)
        if confirm:
            tryes = 3
            while tryes != 0:
                plantilla2= """
=======================================================
        MATCH POINT     ----    LOGIN CONTRASEÑA
=======================================================
Ingrese su contraseña: 
    """
                mi_plantilla = Template (plantilla2)
                print(mi_plantilla.render())
                psw= str(input(""))
                confirmpsw = any(u for u in data if u.get("psw") == psw)
                if confirmpsw:
                    return save_user(user,psw,data)
                elif tryes == 0:
                    print("       X - DEMASIADOS INTENTOS - X         ")
                    my_funtion() 
                else:
                    print("LA CONTRASEÑA ES ERRONEÁ - INTENTE DE NUEVO :  ")
                    tryes -= 1
        else:
            print("EL USUARIO NO EXISTE - INTENTE DE NUEVO :  ")
            