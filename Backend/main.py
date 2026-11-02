from jinja2 import Template
from admins.admin import admin_menu_login

def login_funcion():
    from users.login import login_user
    login_user()

def register_funcion():
    from register import new_account
    new_account()

def my_funtion():
    try:    
        plantilla= """
==============================================================
                  BIENVENIDOS A  MATCH POINT    
==============================================================  
-D 1 CREAR NUEVA CUENTA
-D 2 INICIAR SESIÓN
-D 3 INGRESAR COMO ADMINISTRADOR
 X 4 SALIR
    """
        mi_plantilla = Template (plantilla)
        print(mi_plantilla.render())
    
        opcion = int(input(""))
        match opcion:
            case 1:
                register_funcion()
            case 2:
                login_funcion()                                      
            case 3:
                admin_menu_login()
            case 4:
                print(f'HASTA LUEGO')
            case  _ :
                print("-----------------------------------------------------")
                print("            x - OPCION FUERA DE RANGO - x            ")
                print("-----------------------------------------------------")
                main()      
    except ValueError:
        print("----------------------------------------------------")
        print("         X - POR FAVOR USE SOLO NUMEROS - X         ")
        print("----------------------------------------------------")
        main()
        
def main():
    my_funtion()

if __name__ == '__main__':
    main()