import os
def get_subfiles_recursively(folder_path):
    '''
    Get subfiles under 'folder_path' recursively
    Args:
        folder_path: A folder(dir) whose subfiles/subfolders will be returned.
    Returns:
        python_files: A list including subfiles endwith '.py'.
        other_files: A list including subfiles not endwith '.py'.
        empty_subfolders: A list including empty subfolders.
    '''
    if not os.path.exists(folder_path):
        raise ValueError("Path '{}' don't exist.".format(folder_path))
    elif not os.path.isdir(folder_path):
        raise ValueError('Input should be a folder, not a file.')
    else:
        python_files = []
        other_files = []
        empty_subfolders = []
        for root, dirs, files in os.walk(folder_path):
            if files:
                for sub_file in files:
                    if sub_file.endswith('.py'):
                        python_files.append(
                            os.path.normpath(os.path.join(root, sub_file)))
                    else:
                        other_files.append(
                            os.path.normpath(os.path.join(root, sub_file)))
            elif len(dirs) == 0:
                empty_subfolders.append(os.path.normpath(root))
        return python_files, other_files, empty_subfolders
get_subfiles_recursively("train_log")

