import os
from pathlib import Path
import typing
from collections import namedtuple

os.chdir(Path(__file__).parent)

def toInt(c):
    return ord(c) - ord("a")

def toChr(i):
    return chr(i + ord("a"))

def isSecure(password: typing.List[int]) -> bool:
    secure = True
    if any([x in password for x in map(toInt,{"i", "o", "l"})]):
        secure = False
    same_chars = [i for i,(x,y) in enumerate(zip(password, password[1:])) if x==y]
    if len([i for i,j in zip(same_chars, same_chars[1:] + [99]) if i + 1 < j]) < 2:
        secure = False
    if not any((x+1 == y) and (y+1 == z) for x,y,z in zip(password, password[1:], password[2:])):
        secure = False

    return secure

def wrong_number_possition(password: typing.List[int]) -> int:
    possitions = [password.index(x) for x in map(toInt,{"i", "o", "l"}) if x in password]
    if len(possitions) == 0:
        return -1
    else:
        return min(possitions)
    
def plus_one(password: typing.List[int]) -> typing.List[int]:
    add_one = True
    for i in range(-1, -1*len(password) - 1, -1):
        val = password[i] + 1
        if val <= toInt("z"):
            add_one = False
        password[i] = val % (toInt("z")+1)

        if not add_one:
            break

    return password

def generate(old_password):
    new_password = old_password
    while True:
        new_password = plus_one(new_password)
        pos = wrong_number_possition(new_password)
        if pos != -1:
            new_password = [x if i <= pos else toInt("z") for i, x in enumerate(new_password)]
            continue
        if isSecure(new_password):
            return new_password

def main():
    old_password = "vzbxkghb"
    old_password_ord = list(map(toInt, old_password))
    
    new_password_ord = generate(old_password_ord)
    new_password = "".join(map(toChr, new_password_ord))

    print("Result:", new_password)

if __name__ == "__main__":
    main()