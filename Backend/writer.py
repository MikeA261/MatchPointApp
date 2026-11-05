import json

def write_user(dates: dict):
    USER= 'PadelApp/MatchPointApp/Backend/locals_json/user.json'
    try:
        with open(USER, 'w', encoding='utf-8') as archivo:
                json.dump(dates, archivo, ensure_ascii=False, indent=4)
    except(FileNotFoundError):
        print("El archivo no se encuentra")
    except(FileExistsError):
        print("El archivo no existe")
    finally:
        pass
    
def write_courts(dates: dict):   
    COURTS= "PadelApp/MatchPointApp/Backend/locals_json/courts.json"
    try:
        with open(COURTS, "w", encoding="utf-8_sig") as archivo:
            json.dump(dates,archivo, indent=4, ensure_ascii=False)
    except FileNotFoundError:
        print(f'El archino no exiiste')
    except(FileExistsError):
        print(f"El archivo no existe")
    finally:
        pass

def write_admin(data: dict):
    ADMIN = "PadelApp/MatchPointApp/Backend/locals_json/admin.json"
    try:
        with open(ADMIN, "w", encoding= "utf-8") as archivo:
            json.dump(data, archivo, indent= 4, ensure_ascii=False)
    except FileNotFoundError:
        print(f'El archino no exiiste')
    except(FileExistsError):
        print(f"El archivo no existe")
    finally:
        pass
        