from jinja2 import Template


plantilla_string = """
========================================
REPORTE DE USUARIO: {{ usuario.nombre }}
========================================
- Estado:     [{{ 'ACTIVO' if usuario.activo else 'INACTIVO' }}]
- Rol:        {{ usuario.rol }}
- Suscripción:
  {% for plan in usuario.planes -%}
  * {{ plan }}
  {% endfor %}
========================================
"""


template = Template(plantilla_string)


datos = {
    "usuario": {
        "nombre": "Carlos Pérez",
        "activo": True,
        "rol": "Administrador",
        "planes": ["Premium Anual", "Soporte 24/7"]
    }
}

print(template.render(datos))