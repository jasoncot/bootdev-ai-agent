import os
from .lib.check_path_contained import check_path_contained

def overwrite_file(working_directory, file_path, contents):
    abs_working_directory = working_directory
    try:
        if os.path.isabs(abs_working_directory) != True: abs_working_directory = os.path.abspath(abs_working_directory)
    except Exception as error:
        return f'Error: Unable to get absolute path for working_directory "{working_directory}"'
    
    abs_file_path = file_path
    try:
        if os.path.isabs(abs_file_path) != True: abs_file_path = os.path.normpath(os.path.join(abs_working_directory, abs_file_path))
    except:
        return f'Error: Unable to get absolute path for file "{file_path}"'

    try:
        if abs_file_path.startswith(abs_working_directory) != True:
            return f'Error: Cannot write to "{file_path}" as it is outside the permitted working directory'
    except:
        return f'Error: Unable to normalize path {file_path} or {working_directory}'

    abs_dirname = os.path.dirname(abs_file_path)

    if os.path.exists(abs_dirname) != True:
        try:
            os.makedirs(abs_dirname, exist_ok=True)
        except:
            return f'Error: Unable to create directories for "{file_path}"'
        
    try:
        with open(abs_file_path, "w") as file:
            file.write(contents)
    except:
        return f'Error: Unable to write contents to file "{file_path}"'
    
    return f'Successfully wrote to "{file_path}" ({len(contents)} bytes written)'

