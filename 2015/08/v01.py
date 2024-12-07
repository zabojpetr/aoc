import os
from pathlib import Path
import typing

os.chdir(Path(__file__).parent)

def char_in_memory(raw: str) -> int:
    counter = -2 # start + end quotes
    escape = False
    for c in raw:
        if not escape and c == "\\":
            escape = True
            continue

        if escape:
            escape = False
            if c == "x":
                counter -= 2

        counter += 1

    return counter

def main():
    in_memory_counter = 0
    code_counter = 0
    with open("input.txt", "r") as fs:
        for l in fs:
            in_memory_counter += char_in_memory(l.strip())
            code_counter += len(l.strip())
        
    print(code_counter, in_memory_counter)
    print("Diff:", code_counter - in_memory_counter)

if __name__ == "__main__":
    main()