import os
from pathlib import Path

def get_files_info(working_directory, directory=None):
    working_dir_path = Path.cwd() / working_directory
    if directory is not None:
        dir_path = working_dir_path / directory
    else:
        dir_path = working_dir_path 

    #print(f"Woking directory: {working_dir_path}")
    #print(f"Full path: {dir_path}")

    if not dir_path.resolve().is_relative_to(working_dir_path.resolve()):
        return f'Error: Cannot list "{directory}" as it is outside the permitted working directory'
    
    if not dir_path.exists():
        return f'Error: "{directory}" does not exist'
    
    if not dir_path.is_dir():
        return f'Error: "{directory}" is not a directory'
    result = ""
    for file_path in dir_path.iterdir():
        stats = file_path.stat()
        result = result + f"- {file_path.name}: file_size={stats.st_size} bytes, is_dir={file_path.is_dir()}\n"
    
    return result


