from capstone import *
from capstone.arm import *

class Symbol:
    def __init__(self, owner, address, size):
        self.owner = owner
        self.paddr = address
        self.vaddr = address
        self.size = size

    def next(self):
        return self.owner.get(self.paddr + self.size)

    def render(self):
        return "X"

    def data(self):
        return self.owner.data(self.paddr, self.size)

class DataSymbol(Symbol):
    def __init__(self, owner, address, size):
        super(DataSymbol, self).__init__(owner, address, size)

    def render(self):
        return "?????????"

class InstructionSymbol(Symbol):
    da = Cs(CS_ARCH_ARM, CS_MODE_THUMB)

    def __init__(self, owner, address, size):
        super(InstructionSymbol, self).__init__(owner, address, size)

    def disassemble(self):
        self.da.detail = True

        d = list(self.da.disasm(self.data(), self.vaddr))
        if len(d) == 0:
            return None
        else:
            return d[0]

    def render(self):
        insn = self.disassemble()
        if insn == None:
            return "?"
        else:
            return "%s %s" % (insn.mnemonic, insn.op_str)