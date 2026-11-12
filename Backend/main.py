#desde aqui se ejecuta para que funcione  todo 
# ejecutarlo desde otro lado no tirara nada 
from jinja2 import Template
from admins.admin import admin_menu_login

def iniciar_sesion():

    from users.login import iniciar_sesion_user
    iniciar_sesion_user()

def registrarse():

    """
    ejecutara el archivos Registrarse para posterior ejecutar la funcion
    cuenta_nueva , que se encargara de resgistrar al usuario
    
    """
    from registrarse import cuenta_nueva # importamos la funcion desde el archivo 

    cuenta_nueva() # la llamamos aqui 

def mi_funcion():
    while True:
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
    
        try:
            opcion = int(input(""))
        except ValueError:
            print("----------------------------------------------------")
            print("         X - POR FAVOR USE SOLO NUMEROS - X         ")
            print("----------------------------------------------------")
            
            continue

        if opcion == 1:
            registrarse() # hecho 

        elif opcion == 2:
            iniciar_sesion()# en proceso    

        elif opcion == 3:
            admin_menu_login()

        elif opcion == 4:
            print("HASTA LUEGO")
            break
        else :
            print("-----------------------------------------------------")
            print("            x - OPCION FUERA DE RANGO - x            ")
            print("-----------------------------------------------------")


def main():
    mi_funcion()

if __name__ == '__main__':
    main()