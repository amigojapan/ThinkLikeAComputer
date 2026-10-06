#!/usr/bin/env python3
from TLAC_turtle_class import Turtle, prepare_board
import TLACsimulator as TLAC

prepare_board()
aki = Turtle("Aki", 1, 4)
aki.mark_and_move()
aki.mark_and_move()
aki.right()
aki.mark_and_move()
TLAC.end(TLAC.globals)
