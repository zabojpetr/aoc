import os
from pathlib import Path
import typing
import timeit
from collections import namedtuple


os.chdir(Path(__file__).parent)

Gate = namedtuple("Gate", ["typ", "inputs", "output"])

def load_data(data: typing.List[str]) -> typing.Tuple[typing.Dict[str, Gate], typing.Dict[str, int]]:
    gates = {}
    wires_voltage = {}
    wires = True

    for r in data:
        if len(r) == 0:
            wires = False
            continue
        if wires:
            name, voltage = r.split(":")
            wires_voltage[name.strip()] = int(voltage.strip())
        else:
            inputs, output = r.split("->")
            i1, typ, i2 = inputs.strip().split(" ")
            gates[output.strip()] = Gate(typ, (i1, i2), output.strip())

    return gates, wires_voltage

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
    

def main() -> None:

    with open("input.txt", "r") as fs:
        data = list(map(lambda x: x.strip(), fs.readlines()))

    gates, wires = load_data(data)
    output = compute_outputs(gates, wires)

    print(output)



if __name__ == "__main__":
    start = timeit.default_timer()
    main()
    print(f"Total time: {timeit.default_timer() - start}s.")