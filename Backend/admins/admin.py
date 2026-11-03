# cotrola el apartado de admin 
import json

from jinja2 import Template
import random as rn

from reader import read_admin
from reader import read_courts
from writer import write_admin

# Pide un DNI que no este registrado y que tenga entre 7 y 8 digitos.
def validate_dni()->int:
    data = read_admin()
    try:
        while True:
            dni= int(input("dni:  "))
            duplicate = any(u.get("dni") == dni for u in data)
            if duplicate:
                print("X - DNI YA EXISTENTE - X")
            else:
                large = list(str(dni))
                if len(large) >= 7 and len(large) <= 8: 
                    return dni
                else:
                    print("X - DNI INVALIDO - X")
    except(ValueError):
        print("X - ERROR DNI - USE SOLO NUMEROS - X")
        validate_dni()
    finally:
        pass

# Solicita un nombre compuesto solo por letras.
def validate_name():
    while True:
        name = str(input("INGRESE SU NOMBRE:  ")).strip()
        if name.isalpha():
            return name
        else:
            print("X - EL NOMBRE SOLO DEBE CONTENER LETRAS - X")
            

# Solicita una contrasena de exactamente 6 caracteres, con letras y numeros.
def validate_psw():
    while True:
        psw = str(input("psw:  "))
        large = list(psw)
        contains_num = any(i.isalpha() for i in psw) 
        contains_let= any(i.isdigit() for i in psw)
        if len(large) == 6:
            if contains_num and contains_let:
                return psw
            else:
                print("X - LA CONTRASEÑA DEBE CONTENER AL MENOS UN NÚMERO - X")
        elif len(large) > 6:
            print("X - ERROR - CONTRASEÑA DEMASIADO LARGA - X")
        else:
            print("X - ERROR - CONTRASEÑA DEMASIADO CORTA - X")

# Muestra las empresas/canchas registradas y devuelve el ID elegido.
def choose_court():
    data = read_courts()
    try:
        while True:
            idc = int(input("INGRESE EL ID DE LA EMPRESA:  "))
            confirm = any(u.get("id") == idc for u in data)
            if confirm:
                court = [i for i in data if i["id"] == idc]
                plantilla = """
----------------------------------------------------------------
                    EMPRESA SELECCIONADA
----------------------------------------------------------------
{% for info in cancha -%}
{{ info.data | join(',') | upper  }}
-----------------------------------------------------------------
{% endfor %}
"""
                mi_plantilla = Template(plantilla)
                print(mi_plantilla.render(cancha = court))
                return idc
            else:
                print("X - ID NO VÁLIDO - X")
    except(ValueError):
        print("X - INGRESE SOLO NÚMEROS - X")
        choose_court()
    finally:
            pass        
            
            
    
def back_menu():
    # Importacion local para evitar una dependencia circular al cargar el modulo.
    from main import my_funtion
    my_funtion()

# Valida el acceso del administrador con DNI y contrasena, sin abrir aun otro menu.
def login_admin() -> dict | None:
    try:
        data = read_admin()
    except (OSError, json.JSONDecodeError, ValueError) as error:
        print(f"No se pudieron cargar los administradores: {error}")
        return None

    dni = input("DNI: ").strip()
    psw = input("Contraseña: ")
    if not dni.isdigit() or not 7 <= len(dni) <= 8:
        print("DNI o contraseña incorrectos.")
        return None

    admin = next(
        (
            item
            for item in data
            if item.get("dni") is not None
            and str(item.get("dni")) == dni
            and item.get("psw") == psw
        ),
        None,
    )
    if admin is None:
        print("DNI o contraseña incorrectos.")
        return None

    print(f"INICIO DE SESIÓN CORRECTO. BIENVENIDO, {admin.get('name', '').upper()}.")
    return admin

# Registra un administrador, lo asocia a una cancha y guarda los datos en JSON.
def register_admin():
    dni= validate_dni()
    name = validate_name()
    psw = validate_psw()
    id = rn.randint(1_000_000, 99_000_000)
    idc = choose_court()
    
    new_admin = { "id": id,
                 "dni" : dni,
                 "name": name,
                 "psw" : psw,
                 "court": idc
    } 
    
    data = read_admin()
    data.append(new_admin)
    write_admin(data)
    admin_menu_login()
    
    return print("ok")

# Muestra las opciones de acceso administrativo y deriva a la accion elegida.
def admin_menu_login():
    try:
        plantilla= """
--------------------------------------------------------
                LOGIN ADMINISTRATIVO
--------------------------------------------------------
1 REGISTRAR NUEVO ADMIN
2 INICIAR SESIÓN
3 SALIR

    """
        mi_plantilla = Template(plantilla)
        print(mi_plantilla.render())
        opcion = int(input())
        match opcion:
            case 1:
                register_admin()         
            case 2:
                login_admin()
            case 3:
                back_menu()
            case _ :
                print("-----------------------------------------------------")
                print("            x - OPCION FUERA DE RANGO - x            ")
                print("-----------------------------------------------------")  
                admin_menu_login() 
    except(ValueError):
            print("X - ERROR MENU - INGRESE SOLO NUMEROS - X")
            admin_menu_login()
    finally:
        pass
    
