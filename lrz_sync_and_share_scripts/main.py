"""
Copy.
"""
from hashlib import sha1
from logging import INFO, basicConfig, getLogger
from os import chmod, mkdir, sep, walk
from os.path import isdir, isfile, join
from re import compile as re_compile
from shutil import copy2, rmtree
from stat import S_IRUSR, S_IWUSR
from subprocess import call

from click import Path, group, option

basicConfig(
    level=INFO,
    format="%(asctime)s-%(levelname)s: %(message)s",
    datefmt="%Y_%m_%d %H:%M",
)
_LOGGER = getLogger(__name__)


_IGNORED_FOLDERS = {".PowerFolder"}
_IGNORED_FILES = {".DS_Store"}
_IGNORED_PATTERNS = {re_compile(r"^~\$.*$")}


@group()
def main_group() -> None:
    """
    Scripts for LRZ Sync&Share
    """


@option(
    "--source_directory",
    "-s",
    default="",
    help="The source directory. Usually, this folder is in LRZ Sync&Share, e.g., '/Users/testuser/LRZ Sync+Share/testfolder'",
    type=Path(exists=True, file_okay=False, resolve_path=True),
)
@option(
    "--git_directory",
    "-g",
    default=".",
    help="The directory under git version control, e.g., /Users/testuser/Documents/git/backup_testfolder",
    type=Path(exists=True, file_okay=False, resolve_path=True),
)
@option(
    "--sub_folder",
    "-S",
    default="syncandshare",
    help="The sub-folder under which the files will be copied.",
)
@option(
    "--force",
    "-f",
    default=False,
    is_flag=True,
    help="If target already exists, the script will stop. If you have passed the force tag, the script will delete the existing folder.",
)
@main_group.command()
def copy_lrz_sync_and_share(
    source_directory: str, git_directory: str, force: bool, sub_folder: str
) -> None:
    """
    Copies a folder into a git directory and adds new files to stage.
    """
    target_directory = join(git_directory, sub_folder)
    is_there_a_new_file = _is_there_a_new_file(source_directory, target_directory)
    if is_there_a_new_file:
        ignored_parts = set()
        files_for_git = set()
        if isdir(target_directory):
            if force:
                _LOGGER.warning(f"The folder {target_directory} was deleted...")
                rmtree(target_directory)
            else:
                _LOGGER.error(f"The folder {target_directory} does exist. Aborting...")
                exit(1)
        mkdir(target_directory)
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
                copy2(current_file, new_file)
                files_for_git.add(new_file)
                _LOGGER.debug(f"Copy file {current_file} to {new_file}")
            for name in files_for_git:
                chmod(name, S_IRUSR)
                call(["git", "add", name], cwd=git_directory)
            _LOGGER.info(f"#{len(files_for_git)} files added!")
    else:
        _LOGGER.info(
            "There was no new file in the source directory. Thus, we have nothing to do ..."
        )


def _is_there_a_new_file(source_directory: str, target_directory: str) -> bool:
    ignored_parts = set()
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
        for file in [f for f in files if _should_file_be_included(f)]:
            new_file = join(new_root, file)
            current_file = join(root, file)
            if _hash_file(current_file) != _hash_file(new_file):
                _LOGGER.info(
                    f"File {current_file} and {new_file} have different hashes."
                )
                return True
    return False


def _hash_file(file_name: str) -> str:
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


def _should_file_be_included(f: str) -> bool:
    for ignored_pattern in _IGNORED_PATTERNS:
        if ignored_pattern.match(f) is not None:
            return False
    if f in _IGNORED_FILES:
        return False
    return True


if __name__ == "__main__":
    main_group()
