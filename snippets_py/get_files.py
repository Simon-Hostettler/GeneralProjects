import os


def get_files_recursively(dir):
    subfolders, files = [], []

    for file in os.scandir(dir):
        if file.is_dir():
            subfolders.append(file.path)
        if f.is_file():
            files.append(file.path)

    for directory in subfolders:
        subf, f = get_files_recursively(dir)
        subfolders.extend(subf)
        files.extend(f)

    return subfolders, files
