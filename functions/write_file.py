from pathlib import Path
from google import genai
from google.genai import types

schema_write_file = types.FunctionDeclaration(
    name="write_file",
    description="Writes content to a specific file in the working directory.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="The path to the file to write content to, relative to the working directory.",
            ),
            "content": types.Schema(
                type=types.Type.STRING,
                description="The content to write to the file.",
            ),
        },
    ),
)

def write_file(working_directory, file_path, content):
    working_dir_path = Path.cwd() / working_directory
    file = working_dir_path / file_path

    if not file.resolve().is_relative_to(working_dir_path.resolve()):
        return f'Error: Cannot write to "{file_path}" as it is outside the permitted working directory'
    
    try:
        file.touch(exist_ok=True)
        with open(file, 'w', encoding='utf-8') as f:
            f.write(content)
    except Exception as e:
        return f'Error writing the file: {str(e)}'
    
    return f'Successfully wrote to "{file_path}" ({len(content)} characters written)'
