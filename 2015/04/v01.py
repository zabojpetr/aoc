import os
from pathlib import Path
import hashlib
os.chdir(Path(__file__).parent)

def main():
    with open("input.txt", "r") as fs:
        key = fs.read().strip()

    counter = 0
    while True:
        counter += 1
        hash = hashlib.md5(f"{key}{counter}".encode())
        if hash.hexdigest().startswith("00000"):
            break
    print("Answer:", counter)

if __name__ == "__main__":
    main()