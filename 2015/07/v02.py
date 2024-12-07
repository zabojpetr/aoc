import os
from pathlib import Path
from collections import namedtuple
import typing

os.chdir(Path(__file__).parent)

Comp = namedtuple("Comp", ["gate", "inputs"])

def get_value(graph, value, signals):
    try:
        return int(value)
    except:
        return get_signal(graph, value, signals)

def get_signal(graph: typing.Dict[str, Comp], wire: str, signals: dict):
    comp = graph[wire]
    if wire in signals:
        signal = signals[wire]
    elif comp.gate == "SOURCE":
        signal = get_value(graph, comp.inputs[0], signals)
    elif comp.gate == "WIRE":
        signal = get_value(graph, comp.inputs[0], signals)
    elif comp.gate == "AND":
        signal = get_value(graph, comp.inputs[0], signals) & get_value(graph, comp.inputs[1], signals) 
    elif comp.gate == "OR":
        signal = get_value(graph, comp.inputs[0], signals) | get_value(graph, comp.inputs[1], signals) 
    elif comp.gate == "NOT":
        signal = ~ get_value(graph, comp.inputs[0], signals)
    elif comp.gate == "LSHIFT":
        signal = get_value(graph, comp.inputs[0], signals) << int(comp.inputs[1])
    elif comp.gate == "RSHIFT":
        signal = get_value(graph, comp.inputs[0], signals) >> int(comp.inputs[1])
    else:
        raise Exception("Unsupported Gate")
    
    signal = signal & 2**16-1
    signals[wire] = signal

    return signal

def create_component(raw: str) -> typing.Union[ str, Comp]:
    ins, out = map(lambda x: x.strip(), raw.split("->"))

    parts = ins.split(" ")
    if len(parts) == 3:
        comp = Comp(parts[1], [parts[0], parts[2]])
    elif len(parts) == 2:
        comp = Comp(parts[0], [parts[1]])
    elif len(parts) == 1:
        try:
            comp = Comp("SOURCE", [int(parts[0])])
        except:
            comp = Comp("WIRE", [parts[0]])
    else:
        raise Exception(f"Invalid input '{raw}'")
    
    return out, comp



def main():
    graph = {}
    with open("input.txt", "r") as fs:
        for l in fs:
            name, comp = create_component(l)
            assert name not in graph, f"Wire '{name}' already exists!"
            graph[name] = comp
        

    signal_a = get_signal(graph, 'a', {})
    signal_a2 = get_signal(graph, 'a', {"b":signal_a})
    print("Signal on 'a':", signal_a2)

if __name__ == "__main__":
    main()