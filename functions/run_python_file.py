from pathlib import Path
import subprocess
from google import genai
from google.genai import types

schema_run_python_file = types.FunctionDeclaration(
    name="run_python_file",
    description="Executes a Python file in the working directory.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="The path to the Python file to execute, relative to the working directory.",
            ),
            "args": types.Schema(
                type=types.Type.ARRAY,
                items=types.Schema(
                    type=types.Type.STRING,
                    description="Arguments to pass to the Python script.",
                ),
            ),
        },
    ),
)



def run_python_file(working_directory, file_path, args=[]):
    working_dir_path = Path.cwd() / working_directory
    file = working_dir_path / file_path

    if not file.resolve().is_relative_to(working_dir_path.resolve()):
        return f'Error: Cannot execute "{file_path}" as it is outside the permitted working directory'

    if not file.is_file():
        return f'Error: File "{file_path}" not found.'

    if file.suffix != '.py':
        return f'Error: "{file_path}" is not a Python file.'

    try:
        result = subprocess.run(["python3", str(file)] + (args or []),
                                check=True,
                                cwd=working_dir_path,
                                timeout=30,
                                stdout=subprocess.PIPE,
                                stderr=subprocess.PIPE)
    except subprocess.TimeoutExpired as e:
        return f'Process timed out after 30 seconds.'
    except Exception as e:
        return f'Error executing the file: {str(e)}'

    if result.returncode != 0:
        return f'Process exited with code {result.returncode}: {result.stderr.decode()}'

    if not result.stderr and not result.stdout:
        return 'No output produced.'

    return "STDOUT: " + result.stdout.decode() + "\nSTDERR: " + result.stderr.decode()