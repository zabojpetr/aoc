import os
from pathlib import Path
import typing
import timeit
import itertools

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

def _find_kn(es: typing.Dict[str, typing.Set[str]], ks: typing.Set[str], gs: typing.Set[str], rs: typing.Set[str]) -> typing.Set[typing.Set[str]]:
    kns = set()
    if len(gs) == 0:
        return set([tuple(sorted(ks))])
    while len(gs) > 0:
        v = next(gs.__iter__())
        kns.update(_find_kn(es, ks.union([v]), gs.intersection(es[v]), rs.intersection(es[v])))
        gs.remove(v)
        rs.add(v)

    return kns



def find_kns(edges: typing.Dict[str, typing.Set[str]]) -> typing.Set[typing.Tuple[str]]:
    kns = set()
    
    vs = edges.keys()
    for v, es in edges.items():
        kns.update(_find_kn(edges, set([v]), es, set()))
    
    return kns



def main() -> None:

    with open("input.txt", "r") as fs:
        data = list(map(lambda x: x.strip(), fs.readlines()))

    edges = create_edges(data)
    kns = find_kns(edges)
    max_kn = set()
    for kn in kns:
        if len(kn) > len(max_kn):
            max_kn = kn

    

    print(",".join(sorted(list(max_kn))))

if __name__ == "__main__":
    start = timeit.default_timer()
    main()
    print(f"Total time: {timeit.default_timer() - start}s.")