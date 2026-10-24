from jinja2 import Template
from admin import admin_courts
from user import read_dates
from user import new_account
from user import write_dates
from user import login


def print_template(dates: dict)-> None:
    
    return

def main():
    
    print(f'Para registrarse ingrese 1 \nSi ya tiene una cuenta ingrese 2')
    print(f'Para ingresar como administrador ingrese 3 \nPrecione -1 para finalizar')
    opcion = int(input())
    date = []
    date = read_dates(date)
    match opcion:
        case 1:
            dates= new_account(date)
            write_dates(dates)
            print_template(dates)
        case 2:                                      
            user= str(input(f'Ingrese su Nombre de usuario:  '))
            psw= int(input(f'Ingrese su contraseña:  '))
            login(user,psw)
        case 3:
            admin_courts()
        case -1:
             print(f'Gracias, hasta luego')
        case _ :
            print("Opcion invalida!!!")


if __name__ == '__main__':
    main()