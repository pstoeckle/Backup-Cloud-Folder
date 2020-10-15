"""
Copy.
"""
from os import chmod, mkdir, sep, walk
from os.path import isdir, isfile, join
from re import compile as re_compile
from shutil import copy2, rmtree
from stat import S_IRUSR, S_IWUSR
from subprocess import call

from click import command, option

_SOURCE_DIRECTORY_OPTION = option("--source_directory", "-s", default="")
_TARGET_DIRECTORY_OPTION = option("--target_directory", "-t", default="")
_GIT_DIRECTORY_OPTION = option("--git_directory", "-g", default=".")

_IGNORED_FOLDERS = {".PowerFolder"}
_IGNORED_FILES = {".DS_Store"}
_IGNORED_PATTERNS = {re_compile(r"^~\$.*$")}


@_SOURCE_DIRECTORY_OPTION
@_TARGET_DIRECTORY_OPTION
@_GIT_DIRECTORY_OPTION
@command()
def copy_lrz_sync_and_share(
    source_directory: str, target_directory: str, git_directory: str
) -> None:
    """
    Hallo
    :return:
    """
    if not isdir(target_directory):
        mkdir(target_directory)
    ignored_parts = set()
    files_for_git = set()
    if isdir(source_directory):
        for root, dirs, files in walk(source_directory):
            last_part = root.split(sep)[-1]
            if last_part in _IGNORED_FOLDERS:
                ignored_parts.add(root)
                continue
            skip_this_folder = False
            for ignored_part in ignored_parts:
                if ignored_part in root:
                    skip_this_folder = True
                    break
            if skip_this_folder:
                continue
            new_root = root.replace(source_directory, target_directory)
            if isdir(new_root):
                rmtree(new_root)
            mkdir(new_root)
            for file in [f for f in files if _should_file_be_included(f)]:
                new_file = join(new_root, file)
                if isfile(new_file):
                    chmod(new_file, S_IWUSR | S_IRUSR)
                copy2(join(root, file), new_file)
                files_for_git.add(new_file)
        for name in files_for_git:
            chmod(name, S_IRUSR)
            call(["git", "add", name], cwd=git_directory)
        print(f"#{len(files_for_git)} files added!")


def _should_file_be_included(f: str) -> bool:
    for ignored_pattern in _IGNORED_PATTERNS:
        if ignored_pattern.match(f) is not None:
            return False
    if f in _IGNORED_FILES:
        return False
    return True


if __name__ == "__main__":
    copy_lrz_sync_and_share()
