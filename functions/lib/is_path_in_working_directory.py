import os

def get_absolute_combined_path(path0, path1):
    path0_abs = path0
    if os.path.isabs(path0_abs) != True: path0_abs = os.path.abspath(path0_abs)

    path1_abs = path1
    if os.path.isabs(path1_abs) != True: path1_abs = os.path.abspath(os.path.join(path0_abs, path1_abs))

    return path0_abs, path1_abs

def is_path_in_working_directory(path0, path1):
    path0_abs, path1_abs = get_absolute_combined_path(path0, path1)

    return path1_abs.startswith(path0_abs)
