#IMPORTACION DE LIBRERIÁS
# este apartado relacionado con main.py controla el registro 
# Ajuste reciente: informa errores de lectura/escritura y vuelve al menú con
# el nombre correcto de la función.
import json

from jinja2 import Template
import random as rn

#IMPORTACIONES DE ARCHIVOS LOCALES
from reader import read_user
from writer import write_user


def pedir_texto_obligatorio(mensaje: str) -> str:
    while True:
        valor = input(mensaje).strip()
        if not valor: # si el valor(aux) esta vacio se reproduce el print 
            print("Este campo no puede quedar vacío.")
        else: 
            return valor.lower()


def confirmar_edad()-> int:

    """Se pide validar que la edad ingresada este dentro de
       los parametros limites que se imponen(de 18 a 90 años).
       
       Pre: Se pide una entrada con numeros enteros.
       
       Post: se retorna un numero entero 
    """
    entrada_valida = False # revisar
    while not entrada_valida: # mientras entrada_valida sea False 
                # tambien podriamos hacer while true y ahorrarnos todo eso 
        try: 
            edad = int(input("Ingrese su edad:"))

        except(ValueError):
            print("ERROR...INGRESE SOLO NUMEROS ENTEROS")
            continue

        if  edad  >= 18 and edad <= 90:
            entrada_valida = True

            return edad
        else:
            print("ERROR...INGRESE UNA EDAD ENTRE 18 Y 90")


def validacion_psw():

    while True:

        psw = input("Ingrese su contraseña:  ").replace(" ","")
        if not psw.strip(): # si cadena psw esta vacia has lo siguiente 
            print("ERROR... LA CONTRASEÑA NO PUEDE ESTAR VACÍA!!")

            continue

        psw2 = input("Confirme su contraseña(si ingreso algun espacio anteriomente este habra sido borrado):  ")

        while psw2 != psw:
            print("ERROR...LAS CONTRASEÑAS NO COINCIDEN")

            psw2 = input("Confirme su contraseña:  ")
        return psw

def cuenta_nueva() -> list[dict] | None:

    """Esta funcion recibe todos los datos del usuario que se 
       piden en el registro, para la creación de una nueva cuenta.
       Luego se escriben los datos en el archivo json
       
       Precondición: recibe strings y numeros. Todo los datos se guardan
       en una variable diccionario.
       
       Postcondición: retorna una lista con los datos ingresados  
    """
    try:
        datos = read_user()  # Carga las cuentas existentes para poder agregar la nueva.
        
    except (OSError, json.JSONDecodeError, ValueError) as error:

        print(f"No se pudieron cargar los usuarios: {error}")  # Informa por qué falló.
        return None  # Termina la función; no continúa con el registro.
    
    plantilla = """
=========================================================
                MATCH POINT  REGISTRO
=========================================================
    """

    mi_plantilla = Template (plantilla)
    print(mi_plantilla.render())

    #ZONA DE INPUTS
    id_usuario = rn.randint(100_000_000,999_000_000)
    # Comprueba si el ID generado ya pertenece a alguna cuenta cargada.

    while any(usuario.get("id") == id_usuario for usuario in datos):
        # Si ya existe, genera otro y vuelve a comprobarlo.
        id_usuario = rn.randint(100_000_000,999_000_000)

    username = pedir_texto_obligatorio("Ingrese su nombre de usuario: ")

    while any(usuario.get("username") == username for usuario in datos):
        print(" nombre de usuario ya existente , pruebe otro porfavor")
        username = pedir_texto_obligatorio("Ingrese su nombre de usuario: ")
    
    firname = pedir_texto_obligatorio("Ingrese su nombre: ")
    secname = pedir_texto_obligatorio("Ingrese su apellido: ")

    edad = confirmar_edad() # anteriores funciones 
    psw = validacion_psw() 

    lugar = pedir_texto_obligatorio(
        "Ingrese la ciudad donde reside actualmente: "
    )
# te falta cambia nombres y unos reckels adicionales  NO OLVIDAR
    new_usuario = {
        "id"  : id_usuario,
        "username": username,
        "name": firname,
        "psw" : psw,

        "user": {
            "secname": secname,
            "years": edad,
            "location": lugar
            }
    }
    datos.append(new_usuario) # posterior lo prueba en el archivo 

    try:
        write_user(datos)

    except OSError as error:
        print(f"No se pudo guardar el registro: {error}")
        return None
    
    platilla = """
    
    
==========================================================
                !REGISTRO COMPLETADO! 
                BIENVENIDO  {{ name | upper }}
==========================================================  

  
    """
    template = Template(platilla)

    print(template.render(new_usuario))
    
    return datos