"""
Copy.
"""
from logging import INFO, basicConfig, getLogger

from click import Path, group, option

from lrz_sync_and_share_scripts.logic.copy_lrz_sync_and_share import (
    copy_lrz_sync_and_share_internal,
)

basicConfig(
    level=INFO,
    format="%(asctime)s-%(levelname)s: %(message)s",
    datefmt="%Y_%m_%d %H:%M",
)
_LOGGER = getLogger(__name__)


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
@option(
    "--read-only",
    "-r",
    default=False,
    is_flag=True,
    help="Make files read-only",
)
@main_group.command()
def copy_lrz_sync_and_share(
    source_directory: str, git_directory: str, force: bool, sub_folder: str, read_only: bool
) -> None:
    """
    Copies a folder into a git directory and adds new files to stage.
    """
    copy_lrz_sync_and_share_internal(force, git_directory, source_directory, sub_folder, read_only)


if __name__ == "__main__":
    main_group()
