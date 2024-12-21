import os
from pathlib import Path
import typing
import json
import re
import timeit
import numpy as np
from collections import namedtuple
import heapq
import functools

os.chdir(Path(__file__).parent)

class Keyboard():
    def __init__(self, keyboard: typing.List[typing.List[str]]):
        self.keyboard = keyboard
        self._possitions = {}

        self._directions = {
            ">": (0,1),
            "v": (1,0),
            "<": (0,-1),
            "^": (-1,0),
        }

    def _get_possition(self, key: str) -> typing.Tuple[int, int]:
        if key in self._possitions:
            return self._possitions[key]
        else:
            possition = [(i, j) for i, r in enumerate(self.keyboard) for j, c in enumerate(r) if c == key][0]
            self._possitions[key] = possition
            return possition

    def _above_keys(self, possition: typing.Tuple[int, int]) -> bool:
        if possition[0] < 0 or possition[0] >= len(self.keyboard) or possition[1] < 0 or possition[1] >= len(self.keyboard[0]):
            return False
        if self._get_possition("") == possition:
            return False
        return True

    def find_shortest_paths(self, start: str, end: str) -> typing.List[str]:
        visited = set()
        queue = [(self._get_possition(start), [])]
        new_queue = []
        candidates = []
        end_possition = self._get_possition(end)
        while len(candidates) == 0:
            for p, path in queue:
                if p == end_possition:
                    candidates.append("".join(path))

                if not self._above_keys(p):
                    continue

                if self.keyboard[p[0]][p[1]] == "":
                    continue

                # if p in visited:
                #     continue
                
                visited.add(p)

                for n, d in self._directions.items():
                    new_queue.append(((p[0]+d[0], p[1]+d[1]), path + [n]))

            queue = new_queue
            new_queue = []

        return candidates

    def pressed(self, seq: str) -> str:
        pressed = ""
        p = self._get_possition("A")
        for c in seq:
            if c == "A":
                pressed += self.keyboard[p[0]][p[1]]
                continue
            d = self._directions[c]
            p = (p[0] + d[0], p[1] + d[1])
        return pressed


@functools.cache
def apply_step(start: str, end: str, keyboards: typing.List[Keyboard]) -> str:
    if len(keyboards) == 0:
        return end
    else:
        candidates = keyboards[0].find_shortest_paths(start, end)
        results = []
        for candidate in candidates:
            result = ""
            ce = "A" + candidate + "A"
            for s, e in zip(ce, ce[1:]):
                result += apply_step(s,e,keyboards[1:])
            results.append(result)
        results_len = [len(r) for r in results]
        min_len = min(results_len)
        best_result_idx = results_len.index(min_len)
        best_result = results[best_result_idx]

        return best_result

def find_last_seqs(seqs: typing.List[str], keyboards: typing.Tuple[Keyboard]) -> typing.Dict[str, str]:
    new_seqs = {}
    for seq in seqs:
        steps = seq
        result = ""
        for start, end in zip("A" + steps, steps):
            res = apply_step(start, end, keyboards)
            result += res
        new_seqs[seq] = result

    return new_seqs

def compute_complexity(seqs: typing.Dict[str, str]) -> int:
    complexity = 0
    for k, v in seqs.items():
        kn = int("".join([i for i in k if ord(i) >= ord("0") and ord(i) <= ord("9")]))
        complexity += len(v) * kn

    return complexity

def main() -> None:

    with open("input.txt", "r") as fs:
        data = list(map(lambda x: x.strip(), fs.readlines()))

    num_keyboard = Keyboard([["7","8","9"],["4","5","6"],["1","2","3"],["","0","A"]])
    robot_keyboard = Keyboard([["", "^","A"],["<", "v", ">"]])

    seqs = find_last_seqs(data, (num_keyboard, robot_keyboard, robot_keyboard))

    complexity = compute_complexity(seqs)

    print(complexity)

    # too high 112690


if __name__ == "__main__":
    start = timeit.default_timer()
    main()
    print(f"Total time: {timeit.default_timer() - start}s.")