from dataclasses import dataclass
from typing import Dict, Iterator, List, Tuple

from clingcon import ClingconTheory
from clingo import Control, Symbol
from clingo.ast import ProgramBuilder, parse_string


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

    def __init__(self, files) -> None:
        prg = ""

        for file_ in files:
            with open(file_) as f:
                prg += '\n' + f.read()

        self.__thy = ClingconTheory()
        self.__ctl = Control(['-n0'
                            , '--single-shot'
                            , '-t2'
                            ])
        self.__thy.register(self.__ctl)
        with ProgramBuilder(self.__ctl) as bld:
            parse_string(prg,lambda ast: self.__thy.rewrite_ast(ast,bld.add))

    def solve(self, on_model):
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
                sym_big = next((s for s in last_symbols if s.name == "big_rectangle"))
                big_rect = Rectangle(sym_big.arguments[0].number,
                                     sym_big.arguments[1].number,
                                     False, 0, 0)
                on_model(rects, big_rect, max_rects)

    def __is_rotated(self, sym:Symbol, rotated_symbols: List[Symbol]):
        id = sym.arguments[0].number
        return next((sym for sym in rotated_symbols if sym.arguments[0].number == id), None) is not None

    def createRectangles(self, rect_symbols: List[Symbol], assigned_symbols: Iterator[Tuple[Symbol, int]]) -> Dict[int,Rectangle]:
        rotated_symbols = [sym for sym in rect_symbols if sym.name == "is_rotated"]
        rects = {r.arguments[0].number: Rectangle(width=r.arguments[1].number,
                                                  height=r.arguments[2].number,
                                                  isRotated=self.__is_rotated(r, rotated_symbols),
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
