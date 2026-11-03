# Lee los JSON desde Backend/locals_json usando rutas relativas a este archivo.
# También valida que cada archivo contenga una lista de objetos.
import json
from pathlib import Path

BACKEND_DIR = Path(__file__).resolve().parent
DATA_DIR = BACKEND_DIR / "locals_json"


def _read_json_list(path: Path, label: str) -> list[dict]:
    with path.open("r", encoding="utf-8-sig") as archivo:
        data = json.load(archivo)
    if not isinstance(data, list) or not all(isinstance(item, dict) for item in data):
        raise ValueError(f"El archivo de {label} debe contener una lista de objetos.")
    return data


def read_courts()->list[dict]:
    return _read_json_list(DATA_DIR / "courts.json", "canchas")


def read_user() -> list[dict]:
    return _read_json_list(DATA_DIR / "user.json", "usuarios")


def read_admin() -> list[dict]:
    return _read_json_list(DATA_DIR / "admin.json", "administradores")
        
