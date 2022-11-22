# Backup Cloud Folder

During my time at the [Technical University of Munich (TUM)](https://www.tum.de/en/), I often collaborated with others using tools like [LRZ Sync&Share](https://syncandshare.lrz.de/) or [Microsoft 365](https://www.office.com/).
Since I wanted to have a local copy of the files and git version history, I copied the files in a directory under git version control.
Later, I wrote this script to automate this process.

## Usage

```shell
$ backup-cloud-folder --help
Usage: backup-cloud-folder [OPTIONS] COMMAND [ARGS]...

  Script to create a local backup of a cloud folder.

Options:
  --version                       Version
  --install-completion [bash|zsh|fish|powershell|pwsh]
                                  Install completion for the specified shell.
  --show-completion [bash|zsh|fish|powershell|pwsh]
                                  Show completion for the specified shell, to
                                  copy it or customize the installation.
  --help                          Show this message and exit.

Commands:
  copy-cloud-folder  Copies a folder into a git directory and adds new...
```


### Copy Cloud Folder

The first script can be used to copy a folder, e.g., a folder in LRZ Sync&Share, to a folder under git version control.
You can execute the script periodically with [cron](https://en.wikipedia.org/wiki/Cron).
In this case, you will have periodic commits and a git history for your LRZ Sync&Share folder.
**Notabene:** The Sync&Share client has to be running.
Otherwise, changes from other collaborators will not be reflected in your history.

The command is the following:

```shell
$ backup-cloud-folder copy-cloud-folder --help
Usage: backup-cloud-folder copy-cloud-folder [OPTIONS]

  Copies a folder into a git directory and adds new files to stage.

Options:
  -s, --source-directory DIRECTORY
                                  The source directory. Usually, this folder
                                  is in LRZ Sync&Share, e.g.,
                                  '/Users/testuser/LRZ Sync+Share/testfolder'
  -g, --git-directory DIRECTORY   The directory under git version control,
                                  e.g., /Users/testuser/Documents/git/backup_t
                                  estfolder  [default: .]
  -f, --force                     If target already exists, the script will
                                  stop. If you have passed the force tag, the
                                  script will delete the existing folder.
  -S, --sub-folder TEXT           The sub-folder under which the files will be
                                  copied.  [default: syncandshare]
  -r, --read-only                 Make files read-only
  --help                          Show this message and exit.
```

#### Copy Cloud Folder: Example

An example could be

```shell
backup-cloud-folder copy-cloud-folder \
  --source-directory /Users/testuser/LRZ\ Sync+Share/test_folder \
  --git-directory /Users/testuser/Documents/git/test_folder_backup \
  --force
```

This will result in the creation of a folder called `/Users/testuser/Documents/git/test_folder_backup/syncandshare` which contains a copy of all the files in `/Users/testuser/LRZ\ Sync+Share/test_folder`.

#### Copy Cloud Folder: Cron

1. You create script, e.g., `commit.sh` with this content.

  ```shell
  PATH=/path/to/your/python/
  cd /path/to/this/project/ || exit 1
  lrz-sync-and-share-scripts \
    --source_directory /Users/testuser/LRZ\ Sync+Share/test_folder \
    --git_directory /Users/testuser/Documents/git/test_folder_backup \
    --force
  cd /Users/testuser/Documents/git/test_folder_backup || exit 1
  git commit -m "LRZ Sync&Share update" --no-verify
  ```

2. You open the cron service

  ```shell
  crontab -e
  ```

3. Add a line for your script, e.g.,

  ```shell
  1/10  8-20  * * 1-5 /path/to/commit.sh >> /path/to/commit.log 2>&1
  ```

## Contact

If you have any question, please contact [Patrick Stöckle](mailto:patrick.stoeckle@posteo.de).
