from symbol import Symbol, DataSymbol, InstructionSymbol

class SymbolReader:
    def __init__(self, file):
        self.file = file
        self.symbols = {}

    def first(self):
        return self.get(0)

    def get(self, address):
        if address in self.symbols:
            return self.symbols[address]
        else:
            if (address & 1) == 0:
                symbol = InstructionSymbol(self, address, 2)
            else:
                symbol = DataSymbol(self, address, 1)

            self.symbols[address] = symbol
            return symbol

    def data(self, address, length):
        self.file.seek(address)
        return self.file.read(length)