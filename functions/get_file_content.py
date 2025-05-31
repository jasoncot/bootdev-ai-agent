import os
from .lib.check_path_contained import check_path_contained

MAX_SIZE = 10000

def get_file_content(working_directory, file_path):
    message, abs_working_directory, abs_file_path = check_path_contained(working_directory, file_path)

    if message is not None:
        if 'OUT_OF_CONTEXT' in message:
            return f'Error: Cannot list "{file_path}" as it is outside the permitted working directory'
        
        if 'OTHER_TARGET_TYPE' in message:
            return message.replace('OTHER_TARGET_TYPE', 'file')
        
        if 'NOT_EXISTS' in message:
            return f'Error: File not found or is not a regular file: "{file_path}"'
        
        return message

    if os.path.isfile(abs_file_path) != True:
        return f'Error: File not found or is not a regular file: "{file_path}"'

    content = ""

    with open(abs_file_path, "r") as file:
        line = None;
        try:
            line = file.readline()
        except:
            return f'Error: Unable to read file {file_path}'
        
        content_length = 0

        while line:
            if (content_length + len(line)) >= MAX_SIZE:
                remaining = MAX_SIZE - content_length
                content += line[:remaining]
                content += f'[]...File "{file_path}" at 10000 characters]'
                break

            content_length += len(line)
            content += line

            try:
                line = file.readline()
            except:
                return f'Error: Unable to read next line of file {file_path}'
         
    return content
