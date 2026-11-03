# este controla el login del main.py cuando iniciamos sesion
# Ajuste reciente: informa si no puede cargar los usuarios y evita continuar
# con datos inválidos.
import json

from jinja2 import Template

from main import my_funtion
from menu.menu import menu
from reader import read_user


def save_user(usrname: str, psw: str, data: list[dict]) -> dict | None:
    user = next(
        (
            item
            for item in data
            if item.get("username") == usrname and item.get("psw") == psw
        ),
        None,
    )
    if user is not None:
        welcome([user])
    return user


def welcome(user: list[dict]) -> None:
    plantilla = """
========================================================
            BIENVENIDO: {{ name | upper }}
========================================================
    """
    print(Template(plantilla).render(user[0]))
    menu(user)


def login_user() -> None:
    try:
        data = read_user()
    except (OSError, json.JSONDecodeError, ValueError) as error:
        print(f"No se pudieron cargar los usuarios: {error}")
        return

    while True:
        plantilla = """
=======================================================
        MATCH POINT     -----    LOGIN USUARIO
=======================================================
Ingrese su nombre de usuario:
        """
        print(Template(plantilla).render())
        username = input("").strip().lower()
        usuarios = [user for user in data if user.get("username") == username]
        if not usuarios:
            print("EL USUARIO NO EXISTE.")
            continue

        intentos = 3
        while intentos > 0:
            plantilla = """
=======================================================
        MATCH POINT     ----    LOGIN CONTRASEÑA
=======================================================
Ingrese su contraseña:
            """
            print(Template(plantilla).render())
            password = input("")
            usuario = next(
                (user for user in usuarios if user.get("psw") == password),
                None,
            )
            if usuario is not None:
                welcome([usuario])
                return

            intentos -= 1
            print("LA CONTRASEÑA ES INCORRECTA.")

        print("DEMASIADOS INTENTOS.")
        my_funtion()
        return
