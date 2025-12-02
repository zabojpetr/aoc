import os
from pathlib import Path
import typing
import json

os.chdir(Path(__file__).parent)

def parse_input(row: str):
    parts = row.split(",")
    intervals = list(map(lambda x: x.split("-"), parts))

    return intervals

def half_num(num: str, start: bool) -> int:    
    if len(num) % 2 == 1:
        # lichy pocet cifer -> takze prvni vyssi sudy muze byt double
        # 100 -> 3 -> 3//2 = 1 -> 10**1 = 10 -> prvni double = 1010
        half_num = 10**(len(num)//2)

        if not start:
            half_num -= 1
    else:
        # sudy pocet cifer -> kontrola pouze jestli cifry v nizsim radu jsou mensi nez ty ve vyssim, jinak + 1
        # 59 -> 5 < 9 -> prvni je 66, 53 5 > 3 -> prvni je 55, 55 -> 5=5 -> prvni je 55
        # start false: 59 -> 5 < 9 -> posledni je 55, 53 -> 5> 3  -> posledni je 44, 55 5=5 -> posledni je 55
        first_half = int(num[:len(num)//2])
        second_half = int(num[len(num)//2:])

        half_num = first_half
        if first_half < second_half:
            half_num += 1
        
        if not start and first_half != second_half:
            half_num -= 1


    return half_num

def double_it(num: int) -> int:
    return int(str(num)*2)

def find_double_nums(intervals: list[list[int]]):
    double_nums = []
    for start_num, end_num in intervals: 
        start_half = half_num(start_num, True)
        end_half = half_num(end_num, False)

        for i in range(start_half, end_half+1):
            double_nums.append(i)
    
    return sum(map(double_it, double_nums))



def main() -> None:
    with open("input.txt", "r") as fs:
        data = fs.read().strip()

    parsed_data = parse_input(data)
    d = find_double_nums(parsed_data)
        
    print("Heslo:", d)

if __name__ == "__main__":
    main()