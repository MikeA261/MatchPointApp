import json

from jinja2 import Template

from reader import read_user
from writer import write_user


def _guardar_cambio(
    usuarios: list[dict],
    usuario_guardado: dict,
    usuario_actualizado: dict,
    usuario_sesion: dict,
) -> None:
    usuarios_actualizados = [
        usuario_actualizado if usuario is usuario_guardado else usuario
        for usuario in usuarios
    ]
    write_user(usuarios_actualizados)
    # Mantiene actualizada la sesión para que el menú refleje los cambios.
    usuario_guardado.update(usuario_actualizado)
    usuario_sesion.update(usuario_actualizado)


def user_account(usuario_sesion: dict) -> None:
    try:
        usuarios = read_user()
    except (OSError, json.JSONDecodeError, ValueError) as error:
        print(f"No se pudo cargar la cuenta: {error}")
        return

    user_id = usuario_sesion.get("id")
    usuario_guardado = next(
        (usuario for usuario in usuarios if usuario.get("id") == user_id),
        None,
    )
    if usuario_guardado is None:
        print("No se encontró la cuenta del usuario conectado.")
        return

    plantilla = """
========================================================
                    MI CUENTA
========================================================
USUARIO: {{ usuario.username | upper }}
NOMBRE: {{ usuario.name | upper }}
APELLIDO: {{ usuario.user.secname | upper }}
EDAD: {{ usuario.user.years }}
CIUDAD: {{ usuario.user.location | upper }}
--------------------------------------------------------
¿QUÉ DESEA MODIFICAR?
1 - Nombre de usuario
2 - Edad
3 - Contraseña
0 - Regresar al menú
========================================================
"""

    while True:
        print(Template(plantilla).render(usuario=usuario_guardado))
        opcion = input("Seleccione una opción: ").strip()
        if opcion == "0":
            return

        usuario_actualizado = usuario_guardado.copy()
        usuario_actualizado["user"] = usuario_guardado.get("user", {}).copy()

        if opcion == "1":
            nuevo_usuario = input("Ingrese el nuevo nombre de usuario: ").strip().lower()
            if not nuevo_usuario:
                print("El nombre de usuario no puede quedar vacío.")
                continue
            if any(
                otro.get("id") != user_id
                and str(otro.get("username", "")).strip().lower() == nuevo_usuario
                for otro in usuarios
            ):
                print("Ese nombre de usuario ya está en uso.")
                continue
            usuario_actualizado["username"] = nuevo_usuario
        elif opcion == "2":
            try:
                nueva_edad = int(input("Ingrese la nueva edad: ").strip())
            except ValueError:
                print("La edad debe ser un número entero.")
                continue
            if not 8 < nueva_edad < 90:
                print("La edad debe ser mayor que 8 y menor que 90.")
                continue
            usuario_actualizado["user"]["years"] = nueva_edad
        elif opcion == "3":
            contrasena_actual = input("Ingrese la contraseña actual: ")
            if contrasena_actual != usuario_guardado.get("psw"):
                print("La contraseña actual no es correcta.")
                continue
            nueva_contrasena = input("Ingrese la nueva contraseña: ")
            confirmacion = input("Confirme la nueva contraseña: ")
            if not nueva_contrasena:
                print("La contraseña no puede quedar vacía.")
                continue
            if nueva_contrasena != confirmacion:
                print("Las contraseñas no coinciden.")
                continue
            usuario_actualizado["psw"] = nueva_contrasena
        else:
            print("Opción fuera de rango.")
            continue

        try:
            _guardar_cambio(
                usuarios,
                usuario_guardado,
                usuario_actualizado,
                usuario_sesion,
            )
        except OSError as error:
            print(f"No se pudo guardar el cambio: {error}")
            return
        print("CAMBIO GUARDADO CORRECTAMENTE.")
