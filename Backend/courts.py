import json

def read_courts(courts):
    COURTS= "Matchpoint/Backend/courts.json"
    try:
        with open(COURTS, "rt", encoding="utf-8_sig") as archivo:
            courts = json.load(archivo)
    except FileNotFoundError:
        print(f'El archino no exiiste')
    except(FileExistsError):
        print(f"El archivo no existe")
    finally:
        print(courts)
        
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
        
        
