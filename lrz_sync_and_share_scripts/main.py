"""
Copy.
"""
from logging import INFO, basicConfig, getLogger
from os import chmod, mkdir, sep, walk
from os.path import isdir, isfile, join
from re import compile as re_compile
from shutil import copy2, rmtree
from stat import S_IRUSR, S_IWUSR
from subprocess import call

from click import command, option

basicConfig(level=INFO)
_LOGGER = getLogger(__name__)


_IGNORED_FOLDERS = {".PowerFolder"}
_IGNORED_FILES = {".DS_Store"}
_IGNORED_PATTERNS = {re_compile(r"^~\$.*$")}


@option("--source_directory", "-s", default="")
@option("--target_directory", "-t", default="")
@option("--git_directory", "-g", default=".")
@option("--force", "-f", default=False, is_flag=True)
@command()
def copy_lrz_sync_and_share(
    source_directory: str, target_directory: str, git_directory: str, force: bool
) -> None:
    """
    Hallo
    :return:
    """
    if isdir(target_directory):
        if force:
            _LOGGER.warning(f"The folder {target_directory} was deleted...")
            rmtree(target_directory)
        else:
            _LOGGER.error(f"The folder {target_directory} does exist. Aborting...")
            exit(1)
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
            if not isdir(new_root):
                _LOGGER.info(f"Create folder {new_root}")
                mkdir(new_root)
            for file in [f for f in files if _should_file_be_included(f)]:
                new_file = join(new_root, file)
                if isfile(new_file):
                    chmod(new_file, S_IWUSR | S_IRUSR)
                current_file = join(root, file)
                _LOGGER.info(f"Copy file {current_file} to {new_file}")
                copy2(current_file, new_file)
                files_for_git.add(new_file)
        for name in files_for_git:
            chmod(name, S_IRUSR)
            call(["git", "add", name], cwd=git_directory)
        _LOGGER.info(f"#{len(files_for_git)} files added!")


def _should_file_be_included(f: str) -> bool:
    for ignored_pattern in _IGNORED_PATTERNS:
        if ignored_pattern.match(f) is not None:
            return False
    if f in _IGNORED_FILES:
        return False
    return True


if __name__ == "__main__":
    copy_lrz_sync_and_share()
