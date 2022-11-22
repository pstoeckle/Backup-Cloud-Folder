"""
Copy.
"""
from logging import INFO, basicConfig, getLogger
from pathlib import Path

from backup_cloud_folder import __version__
from backup_cloud_folder.logic.copy_cloud_folder import copy_lrz_sync_and_share_internal
from typer import Exit, Option, Typer, echo

basicConfig(
    level=INFO,
    format="%(asctime)s-%(levelname)s: %(message)s",
    datefmt="%Y_%m_%d %H:%M",
)
_LOGGER = getLogger(__name__)


app = Typer()


def _version_callback(value: bool) -> None:
    if value:
        echo(f"backup-cloud-folder {__version__}")
        raise Exit()


@app.callback()
def _call_back(
    _: bool = Option(
        None,
        "--version",
        is_flag=True,
        callback=_version_callback,
        expose_value=False,
        is_eager=True,
        help="Version",
    )
) -> None:
    """
    Script to create a local backup of a cloud folder.
    """


@app.command()
def copy_cloud_folder(
    source_directory: Path = Option(
        "",
        "--source-directory",
        "-s",
        help="The source directory. Usually, this folder is in LRZ Sync&Share, e.g., '/Users/testuser/LRZ Sync+Share/testfolder'",
        exists=True,
        file_okay=False,
        resolve_path=True,
    ),
    git_directory: Path = Option(
        ".",
        "--git-directory",
        "-g",
        help="The directory under git version control, e.g., /Users/testuser/Documents/git/backup_testfolder",
        exists=True,
        file_okay=False,
        resolve_path=True,
    ),
    force: bool = Option(
        False,
        "--force",
        "-f",
        is_flag=True,
        help="If target already exists, the script will stop. If you have passed the force tag, the script will delete the existing folder.",
    ),
    sub_folder: str = Option(
        "syncandshare",
        "--sub-folder",
        "-S",
        help="The sub-folder under which the files will be copied.",
    ),
    read_only: bool = Option(
        False,
        "--read-only",
        "-r",
        is_flag=True,
        help="Make files read-only",
    ),
) -> None:
    """
    Copies a folder into a git directory and adds new files to stage.
    """
    copy_lrz_sync_and_share_internal(
        force, git_directory, source_directory, sub_folder, read_only
    )


if __name__ == "__main__":
    app()
