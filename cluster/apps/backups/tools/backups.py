import json
import logging
import os
import subprocess
import time
from pathlib import Path
from typing import List, Union, Dict

import coloredlogs
import fire
import yaml

logger = logging.getLogger("backups")

coloredlogs.install(level='DEBUG', logger=logger)

BACKUPS_PATH = '/backups'
CURRENT_DIRECTORY = os.path.join(BACKUPS_PATH, "current/")

target_remotes = [r for r in os.environ.get("TARGET_REMOTES", "").split(",") if r]
target_remotes = ["gdrive-boundcorp-leeward:",
                  "gdrive-personal:",
                  "gphotos-leeward:media/by-month",
                  "gphotos-leeward:media/albums"]

KB = 1024 ** 2
MB = 1024 ** 2
GB = 1024 ** 3


def get_path_size(path=Path('.'), recursive=True):
    """
    Gets file size, or total directory size

    Parameters
    ----------
    path: str | pathlib.Path
        File path or directory/folder path

    recursive: bool
        True -> use .rglob i.e. include nested files and directories
        False -> use .glob i.e. only process current directory/folder

    Returns
    -------
    int:
        File size or recursive directory size in bytes
        Use cleverutils.format_bytes to convert to other units e.g. MB
    """
    path = Path(path)
    if path.is_file():
        size = path.stat().st_size
    elif path.is_dir():
        path_glob = path.rglob('*.*') if recursive else path.glob('*.*')
        size = sum(file.stat().st_size for file in path_glob)
    else:
        logger.warning("Ignoring: %s", path)
        size = 0
    return size


def get_latest(path=Path('.'), recursive=True):
    path = Path(path)
    if path.is_file():
        latest = path
    elif path.is_dir():
        path_glob = path.rglob('*.*') if recursive else path.glob('*.*')
        latest = max(path_glob, key=os.path.getctime)
    else:
        logger.warning("Ignoring: %s", path)
        latest = path
    return latest


def large_files(path=Path("."), relative_to=Path(".")) -> Dict[str, int]:
    abs = lambda fn: Path(os.path.join(path, fn))
    rel = lambda fn: fn.relative_to(relative_to)

    files = {
        fn: get_path_size(fn)
        for fn in map(abs, os.listdir(path))
    }

    for fn, _size in reversed(sorted(files.items(), key=lambda item: item[1])):
        if _size > 500 * MB:
            if os.path.isdir(fn):
                large_children = list(large_files(fn, relative_to))
                yield str(rel(fn)), _size
                for f, s in large_children:
                    yield f, s
            else:
                yield str(rel(fn)), _size


DictOfSizes = Dict[str, Union[int, "DictOfSizes"]]


def sizeof_fmt(num, suffix="B"):
    for unit in ["", "Ki", "Mi", "Gi", "Ti", "Pi", "Ei", "Zi"]:
        if abs(num) < 1024.0:
            return f"{num:3.1f}{unit}{suffix}"
        num /= 1024.0
    return f"{num:.1f}Yi{suffix}"


def age(t):
    diff = time.time() - t

    for unit, size in [
        ["sec", 60],
        ["min", 60],
        ["hr", 24],
        ["day", 7],
        ["wk", 4],
        ["Mo", 12],
    ]:
        if abs(diff) < size:
            return f"{diff:3.1f}{unit}"
        diff /= size
    return f"{diff:.1f}Yr"


class Backups(object):
    remotes: List[str]

    def __init__(self):
        os.chdir(BACKUPS_PATH)
        if not os.path.exists(CURRENT_DIRECTORY):
            os.mkdir(CURRENT_DIRECTORY)

        self.remotes = target_remotes or subprocess.check_output(["rclone", "listremotes"]).decode('utf-8').split()

    def status(self):
        logger.debug("%s", yaml.safe_dump({
            "remotes": [self.remote_status(remote) for remote in self.remotes]
        }, indent=2))

    def remote_status(self, remote):
        local = self.destination(remote)
        if not os.path.exists(local):
            return {
                "remote": remote,
                "local": str(local),
                "error": "Does not exist"
            }
        latest = get_latest(local)
        return {
            "remote": remote,
            "local": str(local),
            "size": get_path_size(local, recursive=True),
            "latest": [str(latest), age(latest.stat().st_ctime)],
            "large": [(k, sizeof_fmt(v)) for k, v in large_files(local, local)]
        }

    def destination(self, remote) -> Path:
        location, path = remote.split(":")
        return Path(os.path.join(CURRENT_DIRECTORY, "remotes", location + (path and f"-{path}" or "")))

    def sync(self, dryrun=False):
        for remote in self.remotes:
            destination = self.destination(remote)
            logger.info("Syncing %s -> %s", remote, destination)
            subprocess.check_output([
                "rclone", "sync", remote, destination
            ])


if __name__ == "__main__":
    fire.Fire(Backups)
