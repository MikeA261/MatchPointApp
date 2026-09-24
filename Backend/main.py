import json


def readDates():  
    try: 
        with open('Matchpoint/Backend/dates.json' , 'r', encoding='utf-8') as archivo:
            dates = json.load(archivo)
            return dates
    except FileNotFoundError:
        print(f'El archino no exiiste')
        return None

def login(user,pws,datos)->list:
    return print(datos)

def newAccount(dates)->list:
    newuser = str(input(f'Ingrese su nombre de usuario:  ')) 
    newpsw = str(input(f'Ingrese su contraseña:  ')) 
    location = str(input(f'Ingrese la ciudad donde reside actualmente:  '))

    newUser = [{
        "name": newuser,
        "psw": newpsw,
        "location": location
    }]

    dates.append(newUser)

    with open('Matchpoint/Backend/dates.json', 'w', encoding='utf-8') as archivo:
            json.dump(dates, archivo, ensure_ascii=False, indent=4)
    

def main():

    while True:

        print(f'Para crear una cuenta ingrese 1 \nSi ya tiene una ingrese 2 \nPrecione -1 para finalizar')
        opcion = int(input())

        if opcion == 2:                                      
            user= str(input(f'Ingrese su Nombre de usuario:  '))
            psw= int(input(f'Ingrese su contraseña:  '))
            datos = readDates()
            login(user,psw,datos)
        elif opcion == 1:
            newDates= readDates()
            newAccount(newDates)
        elif opcion == -1:
             print(f'Gracias, hasta luego')
             break


if __name__ == '__main__':
    main()