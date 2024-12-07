import os
from pathlib import Path
os.chdir(Path(__file__).parent)

def compute_wrapping_paper_surface(dimensions: str) -> int:
    ds = sorted(map(int, dimensions.split("x")))
    surface = 3*ds[0]*ds[1] + 2*ds[1]*ds[2] + 2*ds[0]*ds[2]
    return surface

def main():
    total = 0
    with open("input.txt", "r") as fs:
        for l in fs:
            total += compute_wrapping_paper_surface(l.strip())
    print("Surface:",total)

if __name__ == "__main__":
    main()