import os

def check_path_contained(working_directory, other_target=None):
    if other_target is None:
        return f'Error: OTHER_TARGET_TYPE was not provided', None, None

    abs_working_directory = working_directory
    try:
        if os.path.isabs(abs_working_directory) != True: abs_working_directory = os.path.abspath(abs_working_directory)
    except Exception as error:
        return f'Error: Unable to get absolute path for working_directory "{working_directory}"', None, None
    
    abs_other_target = other_target
    try:
        if os.path.isabs(abs_other_target) != True: abs_other_target = os.path.normpath(os.path.join(abs_working_directory, abs_other_target))
    except:
        return f'Error: Unable to get absolute path for OTHER_TARGET_TYPE "{other_target}"', None, None

    try:
        if os.path.exists(abs_other_target) != True:
            return f'Error: OTHER_TARGET NOT_EXISTS "{other_target}"', None, None
    except:
        return f'Error: Unable to check if OTHER_TARGET_TYPE "{other_target}" exists', None, None

    try:
        if abs_other_target.startswith(abs_working_directory) != True:
            return f'Error: OTHER_TARGET OUT_OF_CONTEXT "{other_target}"', None, None
    except:
        return f'Error: Unable to normalize path {other_target} or {working_directory}', None, None

    return None, abs_working_directory, abs_other_target
