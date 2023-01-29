from time import sleep
from sys import argv
import subprocess
import os
import sys

INTERVAL = 0.5  # in seconds
sp = None


def run(file_name):
    global sp
    print(f"\033[32m\033[1m[MON] trying to run {file_name}\033[0m")

    try:
        if sp is not None:
            sp.kill()
        sp = subprocess.Popen([sys.executable, file_name])
    except Exception as e:
        print(e.with_traceback(e.__traceback__))


def find_last(root_path: str, skip_paths: list[str]) -> int:
    mtime = 0
    for current_path, dirs, files in os.walk(root_path):
        for file in files:
            mtime = max(os.path.getmtime(
                os.path.join(current_path, file)), mtime)
        for dir in dirs.copy():
            if dir.startswith(".") or dir in skip_paths:
                dirs.remove(dir)
    return mtime


def main():
    if len(argv) < 2:
        print("Please pass the name of the file to be monitored")
        exit()

    root_path = os.getcwd()  # TODO: turn to optional cli argument
    main_file = argv[1]
    skip_paths = argv[2].split(",") if len(argv) > 2 else []
    last_mtime = 0

    while True:
        mtime = find_last(root_path, skip_paths)
        if mtime > last_mtime:
            last_mtime = mtime
            run(main_file)
        sleep(INTERVAL)


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\rsee u again~")
