import os
from pathlib import Path
import numpy as np
from collections import namedtuple
os.chdir(Path(__file__).parent)

Settings = namedtuple("Settings", ["mode", "x1", "y1", "x2", "y2"])

def parse_coords(parts: list):
    return [*map(int,parts[0].split(",")), *map(lambda x: x+1, map(int,parts[2].split(",")))]

def parse_settings(raw: str) -> Settings:
    settings = None
    parts = raw.split(" ")
    if parts[0] == "toggle":
        settings = Settings("toggle", *parse_coords(parts[1:]))
    elif parts[0] == "turn":
        if parts[1] == "on":
            settings = Settings("on", *parse_coords(parts[2:]))
        elif parts[1] == "off":
            settings = Settings("off", *parse_coords(parts[2:]))
    
    assert settings is not None, f"Unknown mode: {parts[0:2]}"

    return settings
    
    

def set_lights(arr: np.array, settings: Settings):
    if settings.mode == "toggle":
        arr[settings.x1:settings.x2, settings.y1:settings.y2] += 2
    elif settings.mode == "on":
        arr[settings.x1:settings.x2, settings.y1:settings.y2] += 1
    elif settings.mode == "off":
        arr[settings.x1:settings.x2, settings.y1:settings.y2] -= 1
        arr[arr < 0] = 0

    return arr

def main():
    arr = np.full((1000,1000), 0)
    with open("input.txt", "r") as fs:
        for l in fs:
            settings = parse_settings(l)
            arr = set_lights(arr, settings)

    print("lighting bulbs:", arr.sum())

if __name__ == "__main__":
    main()