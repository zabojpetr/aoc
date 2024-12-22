import os
from pathlib import Path
import typing
import json
import re
import timeit

os.chdir(Path(__file__).parent)

def _mix_prune(old_number: int, new_number: int) -> int:
    return (old_number ^ new_number)%16777216

def generate_new_secret_number(number: int) -> int:
    n1 = _mix_prune(number, number * 64)
    n2 = _mix_prune(n1, n1 // 32)
    n3 = _mix_prune(n2, n2 * 2048)

    return n3
    
def main() -> None:

    with open("input.txt", "r") as fs:
        data = list(map(lambda x: x.strip(), fs.readlines()))

    results = []
    for r in data:
        if r == "":
            continue
        number = int(r)
        for _ in range(2000):
            number = generate_new_secret_number(number)
        results.append(number)

    print(sum(results))
    


if __name__ == "__main__":
    start = timeit.default_timer()
    main()
    print(f"Total time: {timeit.default_timer() - start}s.")