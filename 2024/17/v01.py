import os
from pathlib import Path
import typing
import timeit
import numpy as np

os.chdir(Path(__file__).parent)

class Computer():
    def __init__(self):
        self.A = None
        self.B = None
        self.C = None
        self.instructions = None
        self.instruction_pointer = 0
        self.first_print = True
    
    def load_data(self, data: typing.List[str]):
        for r in data:
            if len(r) == 0:
                continue
            parts = r.split(":")
            if r.startswith("R"):
                if parts[0].endswith("A"):
                    self.A = int(parts[1])
                elif parts[0].endswith("B"):
                    self.B = int(parts[1])
                elif parts[0].endswith("C"):
                    self.C = int(parts[1])
            elif r.startswith("P"):
                self.instructions = list(map(int,parts[1].split(",")))
            


    def get_operand(self, i: int):
        if i <= 3:
            return i
        elif i == 4:
            return self.A 
        elif i == 5:
            return self.B 
        elif i == 6:
            return self.C 
        else:
            raise ValueError()
        
    def _dv(self, res: str, op: int):
        r = self.A // 2**self.get_operand(op)
        if res == "A":
            self.A = r
        elif res == "B":
            self.B = r
        elif res == "C":
            self.C = r
        

    def adv(self, op:int):
        self._dv("A", op)
        self.instruction_pointer += 2

    def bdv(self, op:int):
        self._dv("B", op)
        self.instruction_pointer += 2

    def cdv(self, op:int):
        self._dv("C", op)
        self.instruction_pointer += 2

    def bxl(self, op: int):
        self.B ^= op
        self.instruction_pointer += 2

    def bst(self, op: int):
        self.B = self.get_operand(op) % 8
        self.instruction_pointer += 2

    def jnz(self, op: int):
        if self.A == 0:
            self.instruction_pointer += 2
        else:
            self.instruction_pointer = self.get_operand(op)

    def bxc(self, op: int):
        self.B ^= self.C 
        self.instruction_pointer += 2

    def out(self, op: int):
        sep = "" if self.first_print else ","
        print(f"{sep}{self.get_operand(op)%8}", end = "")
        self.first_print = False
        self.instruction_pointer += 2
        
    def apply_instruction(self, ins, op):
        inss = {
            0: self.adv,
            1: self.bxl,
            2: self.bst,
            3: self.jnz,
            4: self.bxc,
            5: self.out,
            6: self.bdv,
            7: self.cdv,
        }

        inss[ins](op)

    def apply_instructions(self):
        while self.instruction_pointer + 1 < len(self.instructions):
            self.apply_instruction(self.instructions[self.instruction_pointer], self.instructions[self.instruction_pointer+1])

        print()
  

def main() -> None:

    with open("input.txt", "r") as fs:
        data = list(map(lambda x: x.strip(), fs.readlines()))

    c = Computer()
    c.load_data(data)
    c.apply_instructions()

if __name__ == "__main__":
    start = timeit.default_timer()
    main()
    print(f"Total time: {timeit.default_timer() - start}s.")