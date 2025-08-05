from pathlib import Path
from google import genai
from google.genai import types

schema_get_file_content = types.FunctionDeclaration(
    name="get_file_content",
    description="Retrieves the content of a specific file in the working directory.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="The path to the file to retrieve content from, relative to the working directory.",
            ),
        },
    ),
)


def get_file_content(working_directory, file_path):
    working_dir_path = Path.cwd() / working_directory
    full_file_path = working_dir_path / file_path

    if not full_file_path.resolve().is_relative_to(working_dir_path.resolve()):
        return f'Error: Cannot read "{file_path}" as it is outside the permitted working directory'

    if not full_file_path.is_file():
        return f'Error: File not found or is not a regular file: "{file_path}"'

    # Leer el contenido del archivo
    try:
        with open(full_file_path, 'r', encoding='utf-8') as file:
            content = file.read()
        if len(content) > 10000:
            content = content[:10000] + f"[...File \"{file_path}\" truncated at 10000 characters]"
        return content
    except Exception as e:
        return f'Error reading the file: {str(e)}'
    
