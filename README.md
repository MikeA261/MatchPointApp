<div align="center">

# 🎾 MatchPoint

---

## Descripción

MatchPoint es un prototipo que permite explorar canchas de pádel y administrar
reservas desde una aplicación de consola. La idea es reunir la información de
las canchas —horarios, días de atención y disponibilidad— y ofrecer un flujo
simple para reservar o cancelar turnos.

El proyecto se desarrolla como una aplicación académica en **Python**. Los
datos se leen y guardan localmente en archivos **JSON**; no requiere una base
de datos ni un servidor para ejecutar el backend.

## Problema que aborda

Quienes buscan jugar al pádel pueden tener dificultades para encontrar
canchas, conocer sus horarios y coordinar un turno disponible. MatchPoint
propone centralizar esos datos y aplicar reglas simples para evitar que dos
reservas activas ocupen el mismo horario en una cancha.

## Objetivos del proyecto

- Practicar descomposición de un problema en funciones y módulos.
- Trabajar con listas y diccionarios para representar registros.
- Recorrer y buscar datos para validar usuarios, canchas y reservas.
- Aplicar reglas de fechas, horarios y solapamiento de turnos.
- Persistir información entre ejecuciones mediante archivos JSON.

## Cómo funciona

Al ejecutar el programa aparece un menú para crear una cuenta, iniciar sesión
como usuario o ingresar al acceso administrativo.

### Recorrido del usuario

1. Se registra o inicia sesión.
2. Consulta canchas habilitadas y selecciona una.
3. Ingresa una fecha y elige uno de los turnos disponibles de una hora.
4. Confirma la reserva; el sistema guarda el turno y genera una notificación.
5. Puede consultar o cancelar una reserva propia. La cancelación cambia su
   estado y conserva el registro en el historial.
6. Desde «Mi cuenta» puede cambiar el nombre de usuario, la edad o la
   contraseña.

### Recorrido administrativo

- Consulta las canchas y sus estados.
- Habilita o bloquea una cancha, previa confirmación, y guarda el cambio.
- Consulta notificaciones de reservas creadas y canceladas. Se muestran de
  más recientes a más antiguas, en páginas de cinco avisos.

La opción administrativa **«Consultar reservas» está pendiente** y no forma
parte de las funciones implementadas actualmente.

## Algoritmos y estructuras de datos

El prototipo utiliza estructuras sencillas y adecuadas para el volumen de
datos local del proyecto:

- **Listas de diccionarios:** cada lista contiene registros —por ejemplo,
  usuarios, canchas o reservas— y cada diccionario guarda los campos de un
  registro.
- **Búsqueda secuencial:** se recorren las listas para encontrar un usuario,
  una cancha o una reserva que coincida con el identificador o los datos
  ingresados.
- **Filtrado por recorrido:** se construyen listas con canchas habilitadas o
  reservas activas del usuario conectado.
- **Validación de disponibilidad:** se generan los horarios de una hora
  permitidos para la cancha y el día; luego se descartan los que se solapan
  con reservas activas de esa cancha y fecha.
- **Historial de cancelaciones:** una reserva no se elimina; se actualiza su
  estado para conservar el registro y liberar el turno.
- **Paginación de notificaciones:** el historial se consulta en bloques de
  cinco, mostrando primero los avisos más recientes.
- **Persistencia en JSON:** las listas se convierten a JSON al guardar y se
  reconstruyen al leer los archivos.

 Las búsquedas
 recorren las listas registro por registro, lo que mantiene la implementación
 clara para el alcance actual.

## Funcionalidades

| Área | Funciones |
|---|---|
| Cuentas de usuario | Registro, inicio de sesión y edición de datos de la cuenta |
| Canchas | Consulta de datos, horarios y disponibilidad |
| Reservas | Creación, consulta y cancelación de turnos propios |
| Administración | Inicio de sesión y habilitación/bloqueo de canchas |
| Notificaciones | Registro de reservas creadas/canceladas y consulta paginada |

## Tecnologías

- **Python** para la lógica de la aplicación de consola.
- **JSON** para guardar los datos localmente.
- **Jinja2** para componer algunas vistas de texto de los menús.
- **HTML, CSS y JavaScript** para una interfaz estática en desarrollo, todavía
  no conectada al backend es solo demostrativo.

## Instalación y ejecución

### Requisitos

- Python 3.10 o posterior.
- Jinja2.

Desde una terminal abierta en la carpeta raíz del proyecto, instala Jinja2:

```powershell
py -m pip install Jinja2
```

Si el comando `py` no está disponible, utiliza `python`.

Ejecuta la aplicación con:

```powershell
py Backend\main.py
```

## Estructura del proyecto

```text
Backend/
├── admins/             Acceso y menú administrativo
├── locals_json/        Usuarios, administradores y canchas
├── menu/               Menú de usuario autenticado
├── users/              Inicio de sesión de usuario
├── main.py             Punto de entrada
├── notifications.py    Registro y consulta paginada de avisos
├── register.py         Registro de usuarios
├── reserve.py          Reglas y flujo de reservas
├── user_account.py     Edición de los datos de la cuenta
├── reader.py           Lectura de archivos JSON
├── writer.py           Escritura de archivos JSON
├── reservations.json   Historial de reservas
└── notifications.json  Historial de notificaciones
Fronted/                Interfaz web estática en desarrollo
```

## Archivos de datos

- `Backend/locals_json/user.json`: cuentas de usuario.
- `Backend/locals_json/admin.json`: cuentas administrativas.
- `Backend/locals_json/courts.json`: canchas, horarios y disponibilidad.
- `Backend/reservations.json`: reservas activas y canceladas.
- `Backend/notifications.json`: avisos relacionados con reservas.

El repositorio incluye datos locales de demostración. Las contraseñas de las
cuentas de demostración se guardan en texto plano:
**no uses credenciales reales** en estos archivos.

## Alcance y trabajo futuro

- Implementar la consulta de reservas desde el menú administrativo.
- Conectar la interfaz web con el backend, si el alcance de una próxima etapa
  lo requiere.
- Mejorar la navegación entre menús y reducir llamadas anidadas al regresar
  entre secciones.(optimizarlo para no ser demaciado robusto)
## Equipo

Proyecto de **Michael Agreda** y **Sander Quintanilla**.

**Repositorio:** [MikeA261/MatchPointApp](https://github.com/MikeA261/MatchPointApp)