#IMPORTACION DE LIBRERIÁS
import json
from jinja2 import Template
import random as rn

#IMPORTACIONES DE ARCHIVOS LOCALES
from main import my_funtion
from reader import read_user
from writer import write_user

def confirm_year()-> int:
    """Se pide validar que la edad ingresada este dentro de
       los parametros limites que se imponen(de 8 a 90 años).
       
       Pre: Se pide una entrada con numeros enteros.
       
       Post: se retorna un numero entero 
    """
    entrada_valida = False
    while not entrada_valida:   
        try: 
            year = int(input("Ingrese su edad:  "))
            if year > 8 and year < 90:
                entrada_valida = True
                return year
            else:
                print("ERROR...INGRESE UNA EDAD ENTRE 8 Y 90")
        except(ValueError):
            print("ERROR...INGRESE NUMEROS ENTEROS")

def psw_comparative():
    psw = str(input("Ingrese su contraseña:  "))
    psw2 = str(input("Confirme su contraseña:  "))
    confirm = psw == psw2
    while confirm != True:
        print("    ERROR...LAS CONTRASEÑAS NO COINCIDEN")
        psw = str(input("Ingrese su contraseña:  "))
        psw2 = str(input("Confirme su contraseña:  "))
        if psw == psw2:
            confirm = True
    return psw

def new_account():
    """Esta funcion recibe todos los datos del usuario que se 
       piden en el registro, para la creación de una nueva cuenta.
       Luego se escriben los datos en el archivo json
       
       Precondición: recibe strings y numeros. Todo los datos se guardan
       en una variable diccionario.
       
       Postcondición: retorna una lista con los datos ingresados  
    """
    dates = read_user()
    plantilla = """
=========================================================
                MATCH POINT  REGISTRO
=========================================================
    """
    mi_plantilla = Template (plantilla)
    print(mi_plantilla.render())
    #ZONA DE INPUTS
    id = rn.randint(100_000_000,999_000_000)
    username= str(input(f'Ingrese su nombre de usuario:  ')).lower()
    firname = str(input(f'Ingrese su nombre:  ')).lower()
    secname = str(input(f'Ingrese su apellido:  ')).lower()
    year = confirm_year()
    psw = psw_comparative()
    location = str(input("Ingrese la ciudad donde reside actualmente:  ")).lower()
    newUser = {"id"  : id,
        "username": username,
        "name": firname,
        "psw" : psw,
        "user": {
        "secname": secname,
        "years": year,
        "location": location}
    }
    dates.append(newUser)
    write_user(dates)
    platilla = """
    
    
==========================================================
                !REGISTRO COMPLETADO! 
                BIENVENIDO  {{ name | upper }}
==========================================================  

  
    """
    tempalte = Template(platilla)
    print(tempalte.render(newUser))
    my_funcion()
    return dates