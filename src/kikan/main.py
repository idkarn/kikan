import curses
from engine import Engine
from utils import LaunchError


def main():
    eng = Engine()
    try:
        eng.start()
    except LaunchError:
        curses.endwin()
        print("start failed")


if __name__ == "__main__":
    main()
