# este controla el login del main.py cuando iniciamos sesion
# Ajuste reciente: informa si no puede cargar los usuarios y evita continuar
# con datos inválidos.
import json

from jinja2 import Template

from menu.menu import menu
from reader import read_user


def save_usuario( psw: str, coincidencia: list[dict]) -> dict | None:
    """Devuelve la cuenta coincidente con la contraseña, o None si no existe."""
    return next(
        (
            item for item in coincidencia
            if item.get("psw") == psw
        ),
        None,
    )


def welcome(user: list[dict]) -> None:
    """Muestra el saludo y abre el menú de la cuenta autenticada."""
    plantilla = """
========================================================
            BIENVENIDO: {{ name | upper }}
========================================================
    """
    print(Template(plantilla).render(user[0]))
    menu(user)


def iniciar_sesion_user() -> None:
    """Autentica a una cuenta y regresa al menú principal al terminar."""
    try:
        datos = read_user()
    except (OSError, json.JSONDecodeError, ValueError) as error:
        print(f"No se pudieron cargar los usuarios: {error}")
        return

    # Repite la solicitud del nombre hasta encontrar una cuenta registrada.
    while True:
        plantilla = """
=======================================================
        MATCH POINT     -----    LOGIN USUARIO
=======================================================
Ingrese su nombre de usuario:
        """
        print(Template(plantilla).render())


        username = input("").strip().lower()
        # Conserva las cuentas con ese nombre para comprobar después la contraseña.
        coincidencia = [user for user in datos if user.get("username") == username]

        if not coincidencia:
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
            # Comprueba la contraseña entre las cuentas que coinciden con el nombre.
            usuario = save_usuario(password, coincidencia)

            if usuario is not None:
                welcome([usuario])
                return

            intentos -= 1
            print(f"LA CONTRASEÑA ES INCORRECTA. Intentos restantes --> {intentos}")

        # Después de tres errores, termina el login para volver al menú principal.
        print("DEMASIADOS INTENTOS.")
        return