import os
from pathlib import Path
import typing
import json
import re
import timeit
import numpy as np
import scipy
from matplotlib import pyplot as plt

os.chdir(Path(__file__).parent)

def get_robot(row: str) -> typing.Tuple[np.array]:
    p, v = row.split(" ")

    p = np.array(list(map(lambda x: int(x.strip()),p.split("=")[1].split(","))))
    v = np.array(list(map(lambda x: int(x.strip()),v.split("=")[1].split(","))))

    return (p,v)

def possition_at(step: int, possition: np.array, velocity: np.array, board:typing.Set[int]):
    new_possition = (possition + step*velocity)%np.array(board)

    return new_possition

def compute_safety_factor(poss: typing.List[np.array], board: typing.Set[int]) -> int:
    middle = (np.array(board)/2).astype(int)
    qs = [0,0,0,0]

    for p in poss:
        q = 0
        if p[0] < middle[0]:
            q+=0
        elif p[0] > middle[0]:
            q+=1
        else:
            continue
        
        if p[1] < middle[1]:
            q+=0
        elif p[1] > middle[1]:
            q+=2
        else:
            continue
        qs[q]+=1

    return np.prod(qs)

def show_board(poss: typing.List[np.array], board: typing.Set[int], ax):
    x,y = list(zip(*poss))
    m = scipy.sparse.csr_matrix(([True]*len(poss), (x,y)), shape=board).T.toarray()
    m = np.where(m == True, 1, 0)

    ax.imshow(m, cmap='binary')
    ax.axis('off')


def main() -> None:

    with open("input.txt", "r") as fs:
        data = list(filter(lambda x: len(x) > 0, map(lambda x: x.strip(), fs.readlines())))

    board = (101,103)
    # board = (11,7)

    robots = list(map(get_robot, data))

    steps = 0

    figsize = (8,8)
    fig, axs = plt.subplots(10,10, figsize=figsize)

    while True:
        steps += 1
        ax_p = ((steps - 1)%100)//10, ((steps - 1)%100)%10
        ax = axs[ax_p[0]][ax_p[1]]
        ax.set_title(f"{steps}")
        poss = list(map(possition_at, [steps]*len(robots), *zip(*robots), [board]*len(robots)))
        show_board(poss, board, ax)
        if (steps) % 100 == 0:
            fig.tight_layout()
            plt.show()
            fig, axs = plt.subplots(10,10, figsize=figsize)


    # safety_factor = compute_safety_factor(poss, board)

    # print("Sum:", safety_factor)

if __name__ == "__main__":
    start = timeit.default_timer()
    main()
    print(f"Total time: {timeit.default_timer() - start}s.")