from dataclasses import dataclass
from typing import Dict, Iterator, List, Tuple

from clingcon import ClingconTheory
from clingo import Control, Symbol
from clingo.ast import ProgramBuilder, parse_string
from clingo.symbol import Function, Number


@dataclass
class Rectangle:
    width: int
    height: int
    isRotated: bool
    x_pos : int
    y_pos : int

@dataclass
class Dimension:
    width: int
    height: int


class Controller:

    def __init__(self) -> None:
        prg = ""

        with open("encoding.lp") as f:
            prg = f.read()

        self.__thy = ClingconTheory()
        self.__ctl = Control(['-n0'
                            , '--single-shot'
                            , '-t2'
                            ])
        self.__thy.register(self.__ctl)
        with ProgramBuilder(self.__ctl) as bld:
            parse_string(prg,lambda ast: self.__thy.rewrite_ast(ast,bld.add))

    def solve(self, big_rect: Dimension, rect_dim:Dimension, on_model):
        self.__rect_dim = rect_dim
        # add input facts
        with self.__ctl.backend() as backend:
            atm_a = backend.add_atom(Function(name="big_rectangle", arguments=[Number(big_rect.width), Number(big_rect.height)]))
            backend.add_rule([atm_a])
            atm_a = backend.add_atom(Function(name="rect_dim", arguments=[Number(rect_dim.width), Number(rect_dim.height)]))
            backend.add_rule([atm_a])


        self.__ctl.ground([('base',[])])
        self.__thy.prepare(self.__ctl)
        last_symbols =[]
        last_assignments = []
        with self.__ctl.solve(yield_=True) as hnd:
            for mdl in hnd:
                last_symbols = mdl.symbols(shown=True)
                last_assignments = [(key,val) for key, val in self.__thy.assignment(mdl.thread_id)]
                rects = self.createRectangles(last_symbols, last_assignments)
                max_rects = next((s.arguments[0].number for s in last_symbols if s.name == "max_rects"), 0)

                on_model(rects, max_rects)

    def __is_rotated(self, sym:Symbol):
        return (self.__rect_dim.width, self.__rect_dim.height) == (sym.arguments[2].number, sym.arguments[1].number)

    def createRectangles(self, rect_symbols: List[Symbol], assigned_symbols: Iterator[Tuple[Symbol, int]]) -> Dict[int,Rectangle]:
        rects = {r.arguments[0].number: Rectangle(width=r.arguments[1].number,
                                                  height=r.arguments[2].number,
                                                  isRotated=self.__is_rotated(r),
                                                  x_pos=0,
                                                  y_pos=0) for r in rect_symbols if r.name == "r"}
        for key, val in assigned_symbols:
            if key.name in ['x', 'y']:
                id = key.arguments[0].number
                if id in rects:
                    if key.name == 'x':
                        rects[id].x_pos = val
                    elif key.name == 'y':
                        rects[id].y_pos = val

        return rects
