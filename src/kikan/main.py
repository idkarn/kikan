from .engine import Engine
from .utils import LaunchError


def main():
    eng = Engine()
    try:
        eng.start()
    except LaunchError:
        print("start failed")


if __name__ == "__main__":
    main()
