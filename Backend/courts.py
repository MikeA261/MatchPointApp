import json

def read_courts(courts: list)->list[dict]:
    COURTS= "PadelApp/MatchPointApp/Backend/courts.json"
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
        
def update_courts(dates):
    
    COURTS= "Matchpoint/Backend/courts.json"
    try:
        with open(COURTS, "rt", encoding="utf-8_sig") as archivo:
            json.dump(dates,archivo, indent=4, ensure_ascii=False)
    except FileNotFoundError:
        print(f'El archino no exiiste')
    except(FileExistsError):
        print(f"El archivo no existe")
    finally:
        print("Cancha agregada exitosamente")
        
        
