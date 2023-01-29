curses.init_pair(1, curses.COLOR_GREEN, curses.COLOR_BLACK)
curses.init_pair(2, curses.COLOR_RED, curses.COLOR_BLACK)
curses.init_pair(3, curses.COLOR_MAGENTA, curses.COLOR_BLACK)

for i in range(100):
    self.scr.draw_wireframe([
        Vertex(0, 10, 0),
        Vertex(0, -9, 20),
        Vertex(-20, -9, -20),
        Vertex(20, -9, -20)
    ], [
        (1, 2), (2, 3), (1, 3),
        (0, 1), (0, 2), (0, 3)
    ], i/10, 100, 2)
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
    sleep(0.1)
    self.scr.scr.clear()

# terminal trap
self.scr.get_key()
curses.endwin()
