from kikan.engine import Engine, Loop
from kikan.math import Vertex

"""
 self.scr.draw_wireframe([
        #     Vertex(0, 10, 0),
        #     Vertex(0, -9, 20),
        #     Vertex(-20, -9, -20),
        #     Vertex(20, -9, -20)
        # ], [
        #     (1, 2), (2, 3), (1, 3),
        #     (0, 1), (0, 2), (0, 3)
        # ], i/10, 100, 2)
"""


eng = Engine()

i = 0

@Loop
def loop(fps=30):
    global i
    i += 1
    eng.scr.draw_wireframe([
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
    ], i/10, 100, (255, 0, 0))

eng.start()