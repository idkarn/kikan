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


def main():
    if len(argv) < 2:
        print("Please pass the name of the file to be monitored")
        exit()

    file_name = argv[1]
    last_mtime = 0

    while True:
        mtime = os.path.getmtime(f"{os.getcwd()}/{file_name}")
        if mtime > last_mtime:
            last_mtime = mtime
            run(file_name)

        sleep(INTERVAL)


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\rsee u again~")
