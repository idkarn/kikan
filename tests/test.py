import curses
import _curses


"""
# cube
self.scr.draw_wireframe([
        Vertex(-20, 10, 20),
        Vertex(-20, -9, 20),
        Vertex(20, 10, 20),
        Vertex(20, -9, 20),
        Vertex(-20, 10, -20),
        Vertex(-20, -9, -20),
        Vertex(20, 10, -20),
        Vertex(20, -9, -20)
    ], [
        (0, 1), (2, 3), (0, 2),
        (1, 3), (4, 5), (6, 7),
        (4, 6), (5, 7), (3, 7),
        (2, 6), (1, 5), (0, 4)
    ], i/10, 100, 1)
"""

"""
# pymarid
self.scr.draw_wireframe([
        Vertex(0, 10, 0),
        Vertex(0, -9, 20),
        Vertex(-20, -9, -20),
        Vertex(20, -9, -20)
    ], [
        (1, 2), (2, 3), (1, 3),
        (0, 1), (0, 2), (0, 3)
    ], i/10, 100, 2)
"""

"""
# tesseract
self.scr.draw_wireframe([
        Vertex(-20, 10, 20),
        Vertex(-20, -9, 20),
        Vertex(20, 10, 20),
        Vertex(20, -9, 20),
        Vertex(-20, 10, -20),
        Vertex(-20, -9, -20),
        Vertex(20, 10, -20),
        Vertex(20, -9, -20),

        Vertex(7, 4, 7),
        Vertex(-7, 4, 7),
        Vertex(7, -4, 7),
        Vertex(-7, -4, 7),
        Vertex(7, 4, -7),
        Vertex(-7, 4, -7),
        Vertex(7, -4, -7),
        Vertex(-7, -4, -7),
    ], [
        (0, 1), (2, 3), (0, 2),
        (1, 3), (4, 5), (6, 7),
        (4, 6), (5, 7), (3, 7),
        (2, 6), (1, 5), (0, 4),
        (8, 9), (10, 11), (12, 13),
        (14, 15), (8, 10), (9, 11),
        (12, 14), (13, 15), (8, 12),
        (9, 13), (10, 14), (11, 15),
        (8, 2), (9, 0), (10, 3),
        (11, 1), (12, 6), (13, 4),
        (14, 7), (15, 5)
    ], i/20, 300, 3)
"""


def draw_line(x1, y1, x2, y2):

    m_new = 2 * (y2 - y1)
    slope_error_new = m_new - (x2 - x1)

    y = y1
    for x in range(x1, x2+1):

        yield x, y

        # Add slope to increment angle formed
        slope_error_new = slope_error_new + m_new

        # Slope error reached limit, time to
        # increment y and update slope error.
        if (slope_error_new >= 0):
            y = y+1
            slope_error_new = slope_error_new - 2 * (x2 - x1)


def main(win: "_curses._CursesWindow"):
    win.erase()

    for x, y in draw_line(0, 0, 25, 3):
        win.addch(y, x, "*")

    win.getkey()


# curses.wrapper(main)
