import os
from pathlib import Path
import typing
import timeit

os.chdir(Path(__file__).parent)

def create_edges(data: typing.List[str]) -> typing.Dict[str, typing.Set[str]]:
    edges = {}
    for r in data:
        u, v = r.split("-")
        if u not in edges:
            edges[u] = set()
        if v not in edges:
            edges[v] = set()

        edges[u].add(v)
        edges[v].add(u)

    return edges

def find_triples(edges: typing.Dict[str, typing.Set[str]]) -> typing.Set[typing.Tuple[str, str, str]]:
    triples = set()

    for u, vs in edges.items():
        for v in vs:
            ws = vs.intersection(edges[v])
            for w in ws:
                if u != v and v != w and u != w:
                    t = sorted([u,v,w])
                    triples.add(tuple(t))
    
    return triples

def chief_here(triple: typing.Tuple[str, str, str]):
    chief = False
    for t in triple:
        if t.startswith("t"):
            chief = True
            break

    return chief


def main() -> None:

    with open("input.txt", "r") as fs:
        data = list(map(lambda x: x.strip(), fs.readlines()))

    edges = create_edges(data)
    triples = find_triples(edges)
    filtered_tripels = list(filter(chief_here, triples))

    print(len(filtered_tripels))

if __name__ == "__main__":
    start = timeit.default_timer()
    main()
    print(f"Total time: {timeit.default_timer() - start}s.")