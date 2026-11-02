#IMPORTACION DE LIBRERÍAS
from jinja2 import Template

#IMPORTACIONES DE ARCHIVOS LOCALES
from menu.menu import menu
from main import my_funtion
from reader import read_user
       
def save_user(usrname: str,psw: str, data: list)->tuple:
    user = [u for u in data if u.get("psw") == psw and u.get("username") == usrname]      
    welcome(user)
    return

def welcome(user: list)-> None:
    plantilla = """
========================================================
            BIENVENIDO: {{ name | upper }}
========================================================
    """
    mi_plantilla = Template (plantilla)
    print(mi_plantilla.render(user[0]))
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
    user= str(input("")).lower()
    
    confirm = True
    while confirm:
        confirm = any(u for u in data if u.get("username") == user)
        match confirm:
            case True:
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
                        save_user(user,psw,data)
                        confirm = False
                        break
                    else:
                        print("LA CONTRASEÑA ES ERRONEÁ - INTENTE DE NUEVO :  ")
                        tryes -= 1
                    if tryes == 0:
                        print("-----------------------------------------------------------")
                        print("             X - DEMASIADOS INTENTOS - X ")
                        print("-----------------------------------------------------------")
                        my_funtion() 
            case False:
                print("EL USUARIO NO EXISTE - INTENTE DE NUEVO :  ")
                login_user()