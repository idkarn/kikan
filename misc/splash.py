from blessed import Terminal
from time import sleep

DELAY = 0.02
IGNORE_FIRST_LINE = True

term = Terminal()
raw_picture = """▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄
████ █▀█▄█ █▀█▀▀▀█▀▀██
█▄▀█ ▄▀█ █ ▄▀█▀▀ █ █ █
█▄██▄█▄█▄█▄█▄█▄▄▄█▄█▄█"""
picture = raw_picture.replace("\n", "")
print(
    term.home
    + term.clear
    + term.on_color_rgb(0, 0, 0)
    + term.color_rgb(255, 255, 255)
    + term.move_y(term.height // 2 - 2)
)
rows_count = raw_picture.count("\n") + 1
row_len = len(picture) // rows_count
for y in range(rows_count):
    for is_lower in range(1 if IGNORE_FIRST_LINE and y == 0 else 1, 2):
        for x in range(row_len):
            s = picture[(b := row_len * y) : b + x + 1]
            print(term.move_y(term.height // 2 - (rows_count // 2 - y)), end="")
            print(
                " " * ((term.width - row_len) // 2)
                + (s if is_lower else s.replace("█", "▀").replace("▄", " "))
            )
            sleep(DELAY)
with term.cbreak():
    term.inkey()
