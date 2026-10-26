from jinja2 import Template
from admins.admin import admin_courts
from register import read_dates
from register import new_account
from register import write_dates

def loguin_funcion():
    from users.login import login_user
    login_user()

def my_funcion():
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
            date = []
            date = read_dates(date)
            dates = new_account(date)
            write_dates(dates)
        case 2:
            loguin_funcion()                                      
        case 3:
            admin_courts()
        case -1:
             print(f'Gracias, hasta luego')
        case _ :
            print("Opcion invalida!!!")


def main():
    my_funcion()

if __name__ == '__main__':
    main()