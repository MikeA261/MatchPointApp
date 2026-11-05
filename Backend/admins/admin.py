#IMPORTACIONES DE LIBRERIAS
from jinja2 import Template
import random as rn
#IMPORTACIONES DE ARCHIVOS LOCALES
from reader import read_admin
from reader import read_courts
from writer import write_admin
from menu.menu_a import menu_a
    

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

def validate_name():
    while True:
        name = str(input("INGRESE SU NOMBRE:  ")).strip()
        if name.isalpha():
            return name
        else:
            print("X - EL NOMBRE SOLO DEBE CONTENER LETRAS - X")
            
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
    from main import my_funtion
    my_funtion()

def confirm_a_name(data):
    while True:
        a_name = str(input("INGRESE SU NOMBRE:  ")).strip().lower()
        validate = a_name.isalpha()  
        if validate:
            exist_name = any(a for a in data if a["name"] == a_name)
            if exist_name:
                return a_name
            else:
                plantilla = """
-------------------------------------------------
          X - EL NOMBRE NO EXISTE - X            
-------------------------------------------------
1 REINTENTAR
2 SALIR    
                """
                mi_plantilla = Template(plantilla)
                print(mi_plantilla.render())
                option = str(input())
                match option:
                    case "1":
                        login_admin()
                    case "2":
                        admin_menu_login()
        else:
            plantilla = """
-------------------------------------------------
X - NOMBRE NO VALIDO   -  INGRESE SOLO LETRAS - X
-------------------------------------------------
            """
            mi_plantilla = Template(plantilla)
            print(mi_plantilla.render())

def confirm_psw(data):
    while True:
        psw = str(input("INGRESE SU CONTRASEÑA:  ")).strip().lower()
        large = list(psw)
        if len(large) == 6:
            contains_num = any(i.isalpha() for i in psw) 
            contains_let= any(i.isdigit() for i in psw)
            exist_psw = any(a for a in data if a["psw"] == psw)
            if contains_let and contains_num and exist_psw:
                return psw
            else:
                print("X - CONTRASEÑA NO VÁLIDA - X")
        else:
            print("X - CONTRASEÑA NO VÁLIDA - X")
            plantilla = """
-------------------------------------------------
          X - CONTRASEÑA NO VALIDA - X            
-------------------------------------------------
1 REINTENTAR
2 SALIR    
                """
            mi_plantilla = Template(plantilla)
            print(mi_plantilla.render())
            option = str(input())
            match option:
                case "1":
                    login_admin()
                case "2":
                    admin_menu_login()
                    
def login_admin()->None:
    """ Función llama a dos funciones que validan los sus datos de ingresados.
        Una vez validados, se buscan los datos del administrador que ingresa,
        junto con su empresa correspondiente. Por último se imprime por consola 
        un saludo de binevenida al administrador y la empresa asociada.  

        Pre: Debe tener cargado los datos de los administradores y empresas 
        que se encuentran en los archivos json.
        
        Post: No retorna nada.

    """
    
    data = read_admin()
    court = read_courts()
    a_name = confirm_a_name(data)
    a_psw = confirm_psw(data)
    admin = next((a for a in data if a["psw"] == a_psw and a["name"] == a_name), None)
    selec_court = next((a for a in court if a["id"] == admin.get("court")), None)
    plantilla = """
----------------------------------------------------------
    BIENVENIDO {{ administrator.name | upper }}
    EMPRESA : {{empress.data | join(",") |upper }}
----------------------------------------------------------
        """
    mi_plantilla = Template(plantilla)
    print(mi_plantilla.render(administrator = admin, empress = selec_court))
    menu_a(selec_court)
    return

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
    