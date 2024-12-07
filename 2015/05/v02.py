import os
from pathlib import Path
import hashlib
os.chdir(Path(__file__).parent)

def has_repeat_with_between(x: str) -> str:
    return any([x[i] == x[i+2] for i in range(len(x)-2)])

def has_twice_pair(x: str) -> bool:
    pairs = {}
    for i, p in enumerate(zip(x, x[1:])):
        if p in pairs:
            if pairs[p] + 1 < i:
                return True
        else:
            pairs[p] = i


def is_nice(text: str) -> bool:
    return has_repeat_with_between(text) and has_twice_pair(text)

        

def main():
    nice_count = 0
    with open("input_test.txt", "r") as fs:
        for l in fs:
            if is_nice(l.strip()):
                nice_count += 1

    print("Nice words:", nice_count)

if __name__ == "__main__":
    main()