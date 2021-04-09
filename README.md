# LRZ Sync&Share Scripts

The idea of this repository is to gather scripts related to [LRZ Sync&Share](https://syncandshare.lrz.de/).

```bash
lrz-sync-and-share-scripts --help
Usage: lrz-sync-and-share-scripts [OPTIONS] COMMAND [ARGS]...

  Scripts for LRZ Sync&Share

Options:
  --version  Version
  --help     Show this message and exit.

Commands:
  copy-lrz-sync-and-share  Copies a folder into a git directory and adds
                           new...
```


## Backup Folder

The first script can be used to copy a folder, e.g., a folder in LRZ Sync&Share, to a folder under git version control.
You can execute the script periodically with [cron](https://en.wikipedia.org/wiki/Cron).
In this case, you will have periodic commits and a git history for your LRZ Sync&Share folder.
**Notabene:** The Sync&Share client has to be running.
Otherwise, changes from other collaborators will not be reflected in your history.

### Command

The command is the following:

```bash
$ lrz-sync-and-share-scripts copy-lrz-sync-and-share --help
Usage: lrz-sync-and-share-scripts copy-lrz-sync-and-share [OPTIONS]

  Copies a folder into a git directory and adds new files to stage.

Options:
  -r, --read-only                 Make files read-only
  -f, --force                     If target already exists, the script will
                                  stop. If you have passed the force tag, the
                                  script will delete the existing folder.

  -S, --sub_folder TEXT           The sub-folder under which the files will be
                                  copied.

  -g, --git_directory DIRECTORY   The directory under git version control,
                                  e.g., /Users/testuser/Documents/git/backup_t
                                  estfolder

  -s, --source_directory DIRECTORY
                                  The source directory. Usually, this folder
                                  is in LRZ Sync&Share, e.g.,
                                  '/Users/testuser/LRZ Sync+Share/testfolder'

  --help                          Show this message and exit.
```

### Example

An example could be

```bash
lrz-sync-and-share-scripts \
  --source_directory /Users/testuser/LRZ\ Sync+Share/test_folder \
  --git_directory /Users/testuser/Documents/git/test_folder_backup \
  --force
```

This will result in the creation of a folder called `/Users/testuser/Documents/git/test_folder_backup/syncandshare` which contains a copy of all the files in `/Users/testuser/LRZ\ Sync+Share/test_folder`.

### Cron

1. You create script, e.g., `commit.sh` with this content.

  ```bash
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

  ```bash
  crontab -e
  ```

3. Add a line for your script, e.g.,

  ```bash
  1/10  8-20  * * 1-5 /path/to/commit.sh >> /path/to/commit.log 2>&1
  ```
