import os
from pathlib import Path
import typing
os.chdir(Path(__file__).parent)

def parse_dimensions(dimensions: str) -> typing.Tuple[int, int, int]:
    return sorted(map(int, dimensions.split("x")))

def compute_wrapping_paper_surface(ds: typing.Tuple[int, int, int]) -> int:
    surface = 3*ds[0]*ds[1] + 2*ds[1]*ds[2] + 2*ds[0]*ds[2]
    return surface

def compute_ribbon_length(ds: typing.Tuple[int, int, int]) -> int:
    length = 2*(ds[0]+ds[1]) + ds[0]*ds[1]*ds[2]
    return length

def main():
    total_surface = 0
    total_length = 0
    with open("input.txt", "r") as fs:
        for l in fs:
            ds = parse_dimensions(l.strip())
            total_surface += compute_wrapping_paper_surface(ds)
            total_length += compute_ribbon_length(ds)

    print("Surface:",total_surface)
    print("Ribbon:",total_length)

if __name__ == "__main__":
    main()