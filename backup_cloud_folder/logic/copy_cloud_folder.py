"""
Copy.
"""
import pathlib
from logging import getLogger
from os import chmod, mkdir, sep, walk
from os.path import isdir, isfile, join
from re import compile as re_compile
from shutil import copy2, rmtree
from stat import S_IRUSR, S_IWUSR
from subprocess import call
from typing import AbstractSet, Pattern

from backup_cloud_folder.utils.hash_file import hash_file

_IGNORED_FOLDERS = {".PowerFolder"}
_IGNORED_FILES = {".DS_Store"}
_IGNORED_PATTERNS: AbstractSet[Pattern[str]] = frozenset(
    (
        re_compile(r"^~\$.*$"),
        re_compile(r".[A-Z0-9]+-[A-Z0-9]+-[A-Z0-9]+-[A-Z0-9]+-[A-Z0-9]+"),
    )
)
_LOGGER = getLogger(__name__)


def copy_lrz_sync_and_share_internal(
    force: bool,
    git_directory: pathlib.Path,
    source_directory: pathlib.Path,
    sub_folder: str,
    read_only: bool,
) -> None:
    target_directory = git_directory.joinpath(sub_folder)
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
            new_root = root.replace(str(source_directory), str(target_directory))
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
                if read_only:
                    chmod(name, S_IRUSR)
                call(["git", "add", name], cwd=git_directory)
            _LOGGER.info(f"#{len(files_for_git)} files added!")
    else:
        _LOGGER.info(
            "There was no new file in the source directory. Thus, we have nothing to do ..."
        )


def _is_there_a_new_file(source_directory: pathlib.Path, target_directory: pathlib.Path) -> bool:
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
        new_root = root.replace(str(source_directory), str(target_directory))
        for file in [f for f in files if _should_file_be_included(f)]:
            new_file = join(new_root, file)
            current_file = join(root, file)
            if hash_file(current_file) != hash_file(new_file):
                _LOGGER.info(
                    f"File {current_file} and {new_file} have different hashes."
                )
                return True
    return False


def _should_file_be_included(f: str) -> bool:
    for ignored_pattern in _IGNORED_PATTERNS:
        if ignored_pattern.match(f) is not None:
            return False
    if f in _IGNORED_FILES:
        return False
    return True
