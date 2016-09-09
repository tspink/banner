#
# SPADE
# Copyright (C) University of Edinburgh 2016
# All Rights Reserved
#
# Tom Spink <tspink@inf.ed.ac.uk>
#
import sys

import curses
from curses import wrapper

from symbolreader import SymbolReader
from symbol import Symbol

def render(scr, reader, start_symbol, display_symbol):
    index = 0

    scr.clear()

    symbol = start_symbol
    while index < 16:
        attr = curses.color_pair(0)

        if display_symbol != None and symbol.paddr == display_symbol.paddr:
            attr = attr | curses.A_REVERSE

        scr.addstr(index, 0, "[%08x] %s" % (symbol.vaddr, symbol.render()), attr)

        symbol = symbol.next()
        index += 1

    scr.refresh()

def annotate(scr, input_file, annotations_file):
    reader = SymbolReader(input_file)

    current_symbol = reader.first()
    while True:
        render(scr, reader, reader.first(), current_symbol)

        key = scr.getch()
        if key == 10:
            return
        elif key == curses.KEY_DOWN:
            current_symbol = current_symbol.next()
        #elif key == curses.KEY_UP:
            #current_symbol = current_symbol.prev

def main(stdscr):
    with open(sys.argv[1], 'rb') as infile:
        with open(sys.argv[2], 'rb') as anfile:
            annotate(stdscr, infile, anfile)


if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("usage: spade <input file> <annotations>")
    else:
        wrapper(main)
        