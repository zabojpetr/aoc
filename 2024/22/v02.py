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

def get_prices(number: int, times: int) -> typing.List[int]:
    prices = [number%10]
    for _ in range(times):
        number = generate_new_secret_number(number)
        prices.append(number%10)

    return prices

def get_price_for_foursome(prices: typing.List[int]) -> typing.Dict[typing.Tuple[int], int]:
    diffs = list(map(lambda x: x[0] - x[1], zip(prices, prices[1:])))

    price_seq = {}

    for i in range(len(diffs)-3):
        k = tuple(diffs[i:i+4])
        if k not in price_seq:
            price_seq[k] = prices[i+4]

    return price_seq

def main() -> None:

    with open("input.txt", "r") as fs:
        data = list(map(lambda x: x.strip(), fs.readlines()))

    price_seqs = []
    sum_seqs = {}
    for r in data:
        if r == "":
            continue
        number = int(r)
        prices = get_prices(number, 2000)
        price_seqs.append(get_price_for_foursome(prices))

    for ps in price_seqs:
        for k, v in ps.items():
            if k in sum_seqs:
                sum_seqs[k] += v
            else:
                sum_seqs[k] = v

    seq = None
    val = None
    for k, v in sum_seqs.items():
        if seq == None or val < v:
            seq = k
            val = v

    print(val)
    


if __name__ == "__main__":
    start = timeit.default_timer()
    main()
    print(f"Total time: {timeit.default_timer() - start}s.")