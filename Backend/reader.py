import json

def read_courts()->list[dict]:
    courts = []
    COURTS= "PadelApp/MatchPointApp/Backend/locals_json/courts.json"
    try:
        with open(COURTS, "rt", encoding="utf-8_sig") as archivo:
            courts = json.load(archivo)
            return courts
    except FileNotFoundError:
        print(f'El archino no exiiste')
    except(FileExistsError):
        print(f"El archivo no existe")
    finally:
        pass
        
def read_user()->list:
    dates = []  
    USER= 'PadelApp/MatchPointApp/Backend/locals_json/user.json'
    try: 
        with open(USER , 'rt', encoding='utf-8-sig') as archivo:
            dates = json.load(archivo)
            return dates
    except FileNotFoundError:
        print(f'El archino no exiiste')
    except(FileExistsError):
        print(f"El archivo no existe")
    finally:
       dates
       
def read_admin()->list:
    admin= []
    ADMIN= 'PadelApp/MatchPointApp/Backend/locals_json/admin.json'
    try:
        with open(ADMIN, "rt", encoding="utf-8-sig") as archivo:
            admin = json.load(archivo)
            return admin
    except FileNotFoundError:
        print("ERROR... archivo no encontrado")
    except FileExistsError:
        print("ERROR... archivo no existe")
    finally:
        pass
        