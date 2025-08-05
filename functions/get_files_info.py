import os
import json
from pathlib import Path
from google.genai import types

# --- CAMBIO 1: Actualizar la descripción del schema ---
# Le decimos explícitamente al modelo que la función devuelve un JSON.
schema_get_files_info = types.FunctionDeclaration(
    name="get_files_info",
    description="Lists files and subdirectories in a specified directory. Returns a JSON string representing a list of items, each with a 'name', 'type' ('file' or 'directory'), and 'size'.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "directory": types.Schema(
                type=types.Type.STRING,
                description="The directory to list, relative to the working directory. Use '.' for the current directory.",
            ),
        },
    ),
)

def get_files_info(working_directory, directory=None):
    if directory is None:
        directory = '.'

    working_dir_path = Path(working_directory).resolve()
    dir_path = (working_dir_path / directory).resolve()

    # ¡Tu comprobación de seguridad es excelente! La mantenemos.
    if not dir_path.is_relative_to(working_dir_path):
        return json.dumps({"error": f"Cannot list '{directory}' as it is outside the permitted working directory"})
    
    if not dir_path.exists():
        return json.dumps({"error": f"'{directory}' does not exist"})
    
    if not dir_path.is_dir():
        return json.dumps({"error": f"'{directory}' is not a directory"})

    # --- CAMBIO 2: Construir una lista de diccionarios, no un string ---
    results_list = []
    try:
        for item_path in dir_path.iterdir():
            stats = item_path.stat()
            # Obtenemos la ruta relativa para que el agente la pueda usar en llamadas futuras
            relative_path = item_path.relative_to(working_dir_path).as_posix()
            
            item_info = {
                "name": relative_path,
                "type": "directory" if item_path.is_dir() else "file",
                "size_bytes": stats.st_size
            }
            results_list.append(item_info)
        
        # --- CAMBIO 3: Devolver la lista convertida a formato JSON ---
        return json.dumps(results_list)

    except Exception as e:
        return json.dumps({"error": str(e)})

