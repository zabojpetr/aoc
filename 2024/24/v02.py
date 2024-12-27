import os
from pathlib import Path
import typing
import timeit
from collections import namedtuple
import networkx as nx
from matplotlib import pyplot as plt
import sys


os.chdir(Path(__file__).parent)

Gate = namedtuple("Gate", ["typ", "inputs", "output"])

def load_data(data: typing.List[str]) -> typing.Tuple[typing.Dict[str, typing.List[Gate]], typing.Dict[str, Gate]]:
    gates_out = {}
    gates_in = {}
    wires = True

    for r in data:
        if len(r) == 0:
            wires = False
            continue
        if wires:
            continue
        else:
            inputs, output = r.split("->")
            output = output.strip()
            i1, typ, i2 = inputs.strip().split(" ")
            inputs = (i1, i2)
            g = Gate(typ, (i1, i2), output)
            gates_out[output] = g
            if i1 not in gates_in:
                gates_in[i1] = []
            if i2 not in gates_in:
                gates_in[i2] = []
            gates_in[i1].append(g)
            gates_in[i2].append(g)

    return gates_in, gates_out

def show_graph(gates_in, gates_out):
    names = {}
    labels = {}
    possition = {}
    gates = {k: (i, v) for i, (k,v) in enumerate(gates_out.items())}
    graph = nx.DiGraph()
    for k, (i, g) in gates.items():
        labels[f"{g.typ}_{i}"] = g.typ
        labels[g.output] = g.output
        graph.add_edge(f"{g.typ}_{i}", g.output)
        for inp in g.inputs:
            labels[inp] = inp
            graph.add_edge(inp, f"{g.typ}_{i}")
            
    pos = nx.nx_agraph.graphviz_layout(graph, "dot", None)
    nx.draw(graph, pos, labels=labels, with_labels = True)
    plt.show()
    print(nx.drawing.nx_pydot.write_dot(graph, sys.stdout))




def op(typ: str, inputs: typing.List[int]) -> int:
    if typ == "AND":
        return inputs[0] & inputs[1]
    elif typ == "OR":
        return inputs[0] | inputs[1]
    elif typ == "XOR":
        return inputs[0] ^ inputs[1]
    else:
        raise ValueError(f"Operation '{typ}' is not supported!")

def compute_voltages(wire: str, gates: typing.Dict[str, Gate], wires: typing.Dict[str, int]):
    if wire in wires:
        return wires
    
    gate = gates[wire]
    for i in gate.inputs:
        wires = compute_voltages(i, gates, wires)
    wires[gate.output] = op(gate.typ, [wires[i] for i in gate.inputs])

    return wires

def compute_outputs(gates: typing.Dict[str, Gate], wires: typing.Dict[str, int]):
    output_wires = []
    for w in gates.keys():
        if w not in wires and w.startswith("z"):
            output_wires.append(w)
            wires = compute_voltages(w, gates, wires)

    output_wires = sorted(output_wires, reverse = True)
    output = 0
    for w in output_wires:
        output = output * 2 + wires[w]

    return output

def set_wires(N:int, x: int, y: int) -> typing.Dict[str, int]:
    wires = {}

    for i in range(N):
        wires[f"x{i:02}"] = (x >> i) & 1
        wires[f"y{i:02}"] = (y >> i) & 1

    return wires

def check_gate_and(g: Gate, gates_in: typing.Dict[str, typing.List[Gate]], gates_out: typing.Dict[str, Gate]):
    swaps = set({})

    if g.inputs[0] in set(["x00", "y00"]):
        # specialni pripad
        next_gs = gates_in.get(g.output,[])
        if len(next_gs) == 2:
            ts = set([ng.typ for ng in next_gs])
            if len(ts.intersection(set(["AND", "XOR"]))) == 2:
                pass
            else:
                swaps.add(g)
                print("Error gate:", g)
        else:
            swaps.add(g)
            print("Error gate:", g)
    else:
        next_gs = gates_in.get(g.output,[])
        if len(next_gs) == 1:
            t = next_gs[0].typ
            if t == "OR":
                pass
            else:
                swaps.add(g)
                print("Error gate:", g)
        else:
            swaps.add(g)
            print("Error gate:", g)

    return swaps


def check_gate_or(g: Gate, gates_in: typing.Dict[str, typing.List[Gate]], gates_out: typing.Dict[str, Gate]):
    swaps = set()

    if g.output == "z45":
        pass
    else:
        next_gs = gates_in.get(g.output,[])
        if len(next_gs) == 2:
            ts = set([ng.typ for ng in next_gs])
            if len(ts.intersection(set(["AND", "XOR"]))) == 2:
                pass
            else:
                swaps.add(g)
                print("Error gate:", g)
        else:
            swaps.add(g)
            print("Error gate:", g)

    return swaps

def check_gate_xor(g: Gate, gates_in: typing.Dict[str, typing.List[Gate]], gates_out: typing.Dict[str, Gate]):
    swaps = set()
    if g.output[0] == "z":
        # druhy xor
        if g.output == "z00":
            if len(set(g.inputs).intersection(set(["x00", "y00"]))) == 2:
                pass
            else:
                swaps.add(g)
                print("Error gate:", g)
        else:
            if g.inputs[0][0] in "xy":
                swaps.add(g)
                print("Error gate:", g)
            else:
                pass
    else:
        # prvni xor
        if g.inputs[0][0] in "xy":
            pass
        else:
            swaps.add(g)
            print("Error gate:", g)
        
        next_gs = gates_in.get(g.output,[])
        if len(next_gs) == 2:
            ts = set([ng.typ for ng in next_gs])
            if len(ts.intersection(set(["AND", "XOR"]))) == 2:
                pass
            else:
                swaps.add(g)
                print("Error gate:", g)
        else:
            swaps.add(g)
            print("Error gate:", g)
    return swaps


def check_gates(gates_in: typing.Dict[str, typing.List[Gate]], gates_out: typing.Dict[str, Gate]):
    swaps = set()
    for _,g in gates_out.items():
        if g.typ == "XOR" and g.output == 'kfr':
            pass
        if g.typ == "AND":
            swaps.update(check_gate_and(g, gates_in, gates_out))
        elif g.typ == "OR":
            swaps.update(check_gate_or(g, gates_in, gates_out))
        elif g.typ == "XOR":
            swaps.update(check_gate_xor(g, gates_in, gates_out))
        else:
            print("Unsupported gate", g)

    print(",".join(sorted([g.output for g in swaps])))


def check_plus_block_from_start(i: int, gates_in: typing.Dict[str, typing.List[Gate]], gates_out: typing.Dict[str, Gate]):
    x = gates_in[f"x{i:02}"]
    c = gates_in[c_in]

    if len(x) != 2:
        print

    if i == 0:
        # half adder
        pass




def check_plus_blocks(N: int, gates_in: typing.Dict[str, typing.List[Gate]], gates_out: typing.Dict[str, Gate]):
    # zmena je u outputu
    switches = []
    for i in range(N):
        wires = set_wires(N, 1<<i, 0)
        output = compute_outputs(gates_out, wires)
        if output != 1<<i:
            # what wires has 1?
            one_wires = [w for w, u in wires.items() if u == 1]


def test_sums(N: int, gates_in: typing.Dict[str, typing.List[Gate]], gates_out: typing.Dict[str, Gate]):
    for i in range(N):
        print(i)
        for (xs, ys, t) in [
            (lambda x: 1<<x, lambda y: 0, "Same number"),
            (lambda x: 1<<x, lambda y: 1<<y, "Two times"),
            (lambda x: 3<<(x-1), lambda y: 1<<y, "Transient one"),
            (lambda x: 3<<(x-1), lambda y: 3<<(y-1), "Transient one, Two times"),
        ]:
            try:
                x = xs(i)
                y = ys(i)
                right = x+y
                wires = set_wires(N, x, y)
                output = compute_outputs(gates_out, wires)
                if output != right:
                    print(f"Test x:{x} + y:{y} = {right}, {t}")
                    print(f"         {x:044b}({x})")
                    print(f"        +{y:044b}({y})")
                    print("-"*70)
                    print(f"Rigth:  {right:045b} ({right})")
                    print(f"Output: {output:045b} ({output})")
                    print()
            except:
                pass

    
def main() -> None:

    with open("input.txt", "r") as fs:
        data = list(map(lambda x: x.strip(), fs.readlines()))

    gates_in, gates_out = load_data(data)
    N = int(len([x for x in gates_in if x.startswith("x")]))

    test_sums(N, gates_in, gates_out)
    show_graph(gates_in, gates_out)
    check_gates(gates_in, gates_out)



if __name__ == "__main__":
    start = timeit.default_timer()
    main()
    print(f"Total time: {timeit.default_timer() - start}s.")