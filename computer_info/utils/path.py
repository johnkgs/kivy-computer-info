from os import path


def get_kv_file_path(current_file: str, kv_file: str):
    return path.join(path.dirname(current_file), kv_file)
