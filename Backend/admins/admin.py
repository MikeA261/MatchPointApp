import json
from courts import read_courts


def admin_login(admin: list[dict])-> bool:
    
    ADMIN= 'Matchpoint/Backend/admins/admin.json'
    try:
        with open(ADMIN, "rt", encoding="utf-8-sig") as archivo:
            admin = json.load(archivo)
    except FileNotFoundError:
        print("ERROR... archivo no encontrado")
    except FileExistsError:
        print("ERROR... archivo no existe")
    finally:
        admin
       
    user= str(input(f"Ingrese su nombre ->  "))
    psw= str(input(f"Ingrese su contraseña ->  "))
    id = int(input("Ingrese su ID de administrador ->  "))
    
    adminl = {
        "id": id,
        "name": user,
        "psw" : psw
    }

    for a in admin:
        confirm = a.get("id")
        if id == confirm:
            userad = a
        else:
            raise(ValueError("ERROR!!!!........En el ID"))
    
    validate = adminl == userad  
    
    return validate

def court_opcion():
    return


def admin_courts():
    
    admin = []
    admin = admin_login(admin)
    print("Bienvenido al sistema de administradores")
    if admin:
        datec = []
        datec = read_courts(datec)
        court_opcion()
    
