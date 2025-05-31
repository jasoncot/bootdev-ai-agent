import os
import subprocess
from .lib.is_path_in_working_directory import is_path_in_working_directory, get_absolute_combined_path

def run_python_file(working_directory, file_path):
    try:
        if is_path_in_working_directory(working_directory, file_path) != True:
            return f'Error: Cannot execute "{file_path}" as it is outside the permitted working directory'
    except:
        return f'Error: Unable to determine if "{file_path} is contained within working directory'
    
    abs_working_directory, abs_file_path = get_absolute_combined_path(working_directory, file_path)

    try:
        if os.path.exists(abs_file_path) != True:
            return f'Error: File "{file_path}" not found.'
    except:
        return f'Error: Unable to determine if "{file_path}" exists'
    
    if abs_file_path.endswith('.py') != True:
        return f'Error: "{file_path}" is not a Python file.'
    
    run_result = None;
    try:
        run_result = subprocess.run(["python3", file_path], capture_output=True, timeout=30, cwd=abs_working_directory)
    except Exception as error:
        return f'Error: executing Python file: {error}'

    output = []
    output.append(f'STDOUT: ' + run_result.stdout.decode())
    output.append(f'STDERR: ' + run_result.stderr.decode())
    if run_result.returncode != 0:
        output.append(f'Process exited with code {run_result.returncode}')
    if run_result.stdout == b'' and run_result.stderr == b'':
        output.append(f'No output produced.')
    
    return '\n'.join(output)
