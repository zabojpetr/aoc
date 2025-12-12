import os
from pathlib import Path
import numpy as np
import z3

class Machine:

    @classmethod
    def from_definition(cls, definition: str):
        definition = definition.strip()
        parts = definition.split(" ")
        target = None
        buttons = []
        joltages = None
        for part in parts:
            if part.startswith("["):
                target_str = part[1:-1]
                target = np.array([0 if c == "." else 1 for c in target_str])
            elif part.startswith("("):
                indices = np.array(list(map(int,part[1:-1].split(","))))
                button = np.zeros(target.shape)
                button[indices] += 1
                buttons.append(button)
            elif part.startswith("{"):
                joltages = np.array(list(map(int,part[1:-1].split(","))))
            else:
                raise ValueError("Neznámý typ objektu ve vstpu: ", part)
            
        return cls(target, buttons, joltages)

    def __init__(self, target: list[int], buttons: list[list[int]], joltages: list[int]):
        self.target = target
        self.buttons = buttons
        self.joltages = joltages

    def get_best_sequence_len_to_target(self):
        used_nodes = set()
        nodes = [(0,np.zeros_like(self.target))]

        while True:
            level, state = nodes.pop(0)
            if (state == self.target).all():
                return level
            if tuple(state.tolist()) in used_nodes:
                continue
            used_nodes.add(tuple(state.tolist()))

            for button in self.buttons:
                new_state = (state + button) % 2
                nodes.append((level+1, new_state))

    def get_best_sequence_len_to_joltages(self):
        bx = [z3.Int(f"b_{i}") for i in range(len(self.buttons))]

        optimizer = z3.Optimize()

        for b in bx:
            optimizer.add(b >= 0)

        for i, button_i in enumerate(np.array(self.buttons).T):
            formula = z3.Sum([k * v for k, v in zip(button_i, bx)])
            optimizer.add(formula == self.joltages[i])

        optimizer.check()
        optimizer.minimize(z3.Sum(bx))

        if optimizer.check() == z3.unsat:
            print("Žádné řešení!")
            print("Konfliktní omezení:", optimizer.unsat_core())  # která způsobila unsat
            print("Důvod:", optimizer.reason_unknown())  # pokud solver selhal

        if optimizer.check() == z3.sat:
            result = optimizer.model().eval(z3.Sum(bx))
            return result.as_long()

os.chdir(Path(__file__).parent)

def parse_input(data: list[str]) -> list[Machine]:
    machines = []

    for row in data:
        row = row.strip()
        machines.append(Machine.from_definition(row))

    return machines


def compute(machines: list[Machine]):
    total = 0
    for machine in machines:
        total += machine.get_best_sequence_len_to_joltages()

    return total


def main() -> None:
    with open("input.txt", "r") as fs:
        data = fs.readlines()

    parsed_data = parse_input(data)
    d = compute(parsed_data)
        
    print("Presses:", d)

if __name__ == "__main__":
    main()