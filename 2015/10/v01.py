import os
from pathlib import Path
import typing
from collections import namedtuple

os.chdir(Path(__file__).parent)

def look_and_say(seed: str) -> str:
    counter = 0
    actual_c = seed[0]
    new_seed = ""
    for c in seed:
        if actual_c == c:
            counter += 1
            continue
        else:
            new_seed += f"{counter}{actual_c}"

            actual_c = c
            counter = 1

    
    new_seed += f"{counter}{actual_c}"

    return new_seed

def main():
    N = 40
    seed = "1113122113"
    
    for _ in range(N):
        seed = look_and_say(seed)

    print("Result:", seed)
    print("Length of result:", len(seed))

if __name__ == "__main__":
    main()