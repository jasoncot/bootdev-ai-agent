import os
from .lib.check_path_contained import check_path_contained

def get_files_info(working_directory, directory=""):
    message, abs_working_directory, abs_directory = check_path_contained(working_directory, directory)

    if message is not None:
        if 'OUT_OF_CONTEXT' in message:
            return f'Error: Cannot list "{directory}" as it is outside the permitted working directory'
        
        if 'OTHER_TARGET_TYPE' in message:
            return message.replace('OTHER_TARGET_TYPE', 'directory')
        
        return message
    
    try:
        if os.path.isdir(abs_working_directory) != True:
            return f'Error: working directory "{working_directory}" is not a directory'
    except:
        return f'Error: Unable to check if {working_directory} is a directory'
    
    file_details = []

    try:
        files = os.listdir(abs_directory)
        for file_name in files:
            f = os.path.join(abs_directory, file_name)

            file_size = 0
            if os.path.isfile(f):
                file_size = os.path.getsize(f)

            is_dir = os.path.isdir(f)
            
            file_details.append(f'- {file_name}: file_size={file_size} bytes, is_dir={is_dir}')
    except:
        return f'Error: unable to scan directory "{directory}"'
    
    return "\n".join(file_details)

