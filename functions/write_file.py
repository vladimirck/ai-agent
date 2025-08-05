from pathlib import Path

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
