import os
from pathlib import Path
import hashlib
os.chdir(Path(__file__).parent)

def is_vowel(x: str) -> bool:
    return x in {"a", "e", "i", "o", "u"}

def is_forbidden(x: str) -> bool:
    return x in {"ab", "cd", "pq", "xy"}

def is_nice(text: str) -> bool:
    vowels = 0
    double_char = False
    evil_comb = False

    first = True

    for x,y in zip(text, text[1:]):
        if first and is_vowel(x):
            vowels += 1
        if is_vowel(y):
            vowels += 1
        if x == y:
            double_char = True
        if is_forbidden(x+y):
            evil_comb = True
            break
        first = False

    return vowels >= 3 and double_char and not evil_comb
        

def main():
    nice_count = 0
    with open("input.txt", "r") as fs:
        for l in fs:
            if is_nice(l.strip()):
                nice_count += 1

    print("Nice words:", nice_count)

if __name__ == "__main__":
    main()