"""
Hash.
"""
from hashlib import sha1
from os.path import isfile


def hash_file(file_name: str) -> str:
    """

    :param file_name:
    :return:
    """
    if not isfile(file_name):
        return ""
    current_sha = sha1()
    with open(file_name, "rb") as f:
        for chunk in iter(lambda: f.read(4096), b""):
            current_sha.update(chunk)
    return current_sha.hexdigest()
