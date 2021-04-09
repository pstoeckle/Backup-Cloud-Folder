"""
Copy.
"""
from logging import CRITICAL, DEBUG, ERROR, INFO, WARNING, basicConfig, getLogger, root
from typing import Any

from click import Context, Path, echo, group, option

from lrz_sync_and_share_scripts import __version__
from lrz_sync_and_share_scripts.logic.copy_lrz_sync_and_share import (
    copy_lrz_sync_and_share_internal,
)

basicConfig(
    level=INFO,
    format="%(asctime)s-%(levelname)s: %(message)s",
    datefmt="%Y_%m_%d %H:%M",
)
_LOGGER = getLogger(__name__)


def _print_version(ctx: Context, _: Any, value: Any) -> None:
    """

    :param ctx:
    :param _:
    :param value:
    :return:
    """
    if not value or ctx.resilient_parsing:
        return
    echo(__version__)
    ctx.exit()


def _set_log_level(ctx: Context, _: Any, value: int) -> None:
    """

    :param ctx:
    :param _:
    :param value:
    :return:
    """
    if not value or ctx.resilient_parsing:
        return
    level = INFO
    if value == 1:
        level = CRITICAL
    elif value == 2:
        level = ERROR
    elif value == 3:
        level = WARNING
    elif value == 4:
        level = INFO
    elif value == 5:
        level = DEBUG

    for logger in (getLogger(name) for name in root.manager.loggerDict):  # type: ignore
        logger.setLevel(level)


@option(
    "--version",
    "-v",
    is_flag=True,
    callback=_print_version,
    expose_value=False,
    is_eager=True,
    help="Log level",
)
@option(
    "--log-level",
    "-l",
    count=True,
    callback=_set_log_level,
    is_eager=True,
    expose_value=False,
    help="Version",
)
@group()
def main_group() -> None:
    """
    Scripts for LRZ Sync&Share
    """
    pass


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
    source_directory: str,
    git_directory: str,
    force: bool,
    sub_folder: str,
    read_only: bool,
) -> None:
    """
    Copies a folder into a git directory and adds new files to stage.
    """
    copy_lrz_sync_and_share_internal(
        force, git_directory, source_directory, sub_folder, read_only
    )


if __name__ == "__main__":
    main_group()
