from jinja2 import Template
from admins.admin import admin_courts

def loguin_funcion():
    from users.login import login_user
    login_user()

def register_funcion():
    from register import new_account
    new_account()

def my_funcion():
    try:    
        plantilla= """
    ===========================================================
                    BIENVENIDOS A  MATCH POINT    
    ===========================================================  
    -D Para registrarse ingrese 1
    -D Si ya tiene una cuenta ingrese 2
    -D Para ingresar como administrador ingrese 3
    Precione -1 para finalizar
    """
        mi_plantilla = Template (plantilla)
        print(mi_plantilla.render())
    
        opcion = int(input("    "))
        match opcion:
            case 1:
                register_funcion()
            case 2:
                loguin_funcion()                                      
            case 3:
                admin_courts()
            case -1:
                print(f'Gracias, hasta luego')
            case _ :
                print("    OPCION NO VALIDA")
                main()      
    except ValueError:
        print("    OPCION NO VALIDA")
        main()
    finally:
        pass

def main():
    my_funcion()

if __name__ == '__main__':
    main()