"""A small turtle class for the advanced TLAC lesson.

Objects share one board but keep their own position and direction. Selecting
the receiving object lets the existing single-player simulator move it while
its other turtle objects remain visible as stationary sprites.
"""
import TLACsimulator as TLAC


def prepare_board():
    board = TLAC.initGlobals()
    board.W = board.H = 6
    board.slots = TLAC.initSlots(board)
    board.turtle = None
    board.ghosts = []
    board.lesson_turtles = []
    TLAC.globals = board


class Turtle:
    def __init__(self, name, x, y):
        self.name = name
        self.X = x
        self.Y = y
        self.direction = "^"
        TLAC.globals.lesson_turtles.append(self)
        self._select()

    @property
    def char(self):
        return self.direction

    def _select(self):
        TLAC.globals.turtle = self
        TLAC.globals.ghosts = [
            turtle for turtle in TLAC.globals.lesson_turtles if turtle is not self
        ]

    def forward(self):
        self._select()
        TLAC.fd(TLAC.globals)

    def right(self):
        self._select()
        TLAC.rt(TLAC.globals)

    def lay_egg(self):
        self._select()
        TLAC.layEgg(TLAC.globals)

    def mark_and_move(self):
        self.lay_egg()
        self.forward()
