import os
from pathlib import Path
import typing
import json
import re
import timeit
import numpy as np

os.chdir(Path(__file__).parent)

class Mapa():
    def __init__(self, data):
        self.mapa = None
        self.seen = None
        self.load_data(data)

    def load_data(self, data):
        self.mapa = np.array(data)
        self.seen = np.full(self.mapa.shape, False)

    def _new_possition(self) -> np.array:
        idxs = np.where(self.seen == False)
        if idxs[0].shape[0] == 0:
            return np.array([])
        return np.array([idxs[0][0], idxs[1][0]])

    def _is_same_region(self, actual: np.array, other: np.array) -> bool:
        in_mapa = 0 <= other[0] and other[0] < self.mapa.shape[0] and 0 <= other[1] and other[1] < self.mapa.shape[1]
        same_region = in_mapa and self.mapa[*actual] == self.mapa[*other]
        return same_region

    def _fence_area(self, possition: np.array):
        self.seen[*possition] = True
        directions = [
            np.array([0,1]),
            np.array([1,0]),
            np.array([0,-1]),
            np.array([-1,0]),
        ]
        fences = 0
        area = 1
        for d in directions:
            if self._is_same_region(possition, possition + d) and self.seen[*(possition+d)]:
                pass
            elif self._is_same_region(possition, possition + d) and not self.seen[*(possition+d)]:
                a,f = self._fence_area(possition + d)
                area += a
                fences += f
            else:
                fences += 1

        return area, fences

    def compute_price(self):
        price = 0
        while True:
            possition = self._new_possition()
            if possition.shape[0] == 0:
                break
            area, fences = self._fence_area(possition)
            price += area * fences

        return price


def main() -> None:

    with open("input.txt", "r") as fs:
        data = list(filter(lambda x: len(x) > 0, map(lambda x: x.strip(), fs.readlines())))

    data = list(map(list, data))

    m = Mapa(data)
    price = m.compute_price()


    print("Sum:", price)

if __name__ == "__main__":
    start = timeit.default_timer()
    main()
    print(f"Total time: {timeit.default_timer() - start}s.")