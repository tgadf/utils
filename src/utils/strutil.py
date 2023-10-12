""" String Utility Functions """

__all__ = ["genStr", "header", "fixName"]

from random import choice
from string import ascii_letters, digits


def genStr(size: int) -> str:
    charpool = ascii_letters + digits
    return "".join([choice(charpool) for _ in range(size)])


def header(name, width=175, delim="*"):
    space = " " * int((width - len(name) - 2 * len('*')) / 2)
    star = f"{delim}" * (len(name) + (2 * len(space)) + 2)
    print(f"{star}")
    print(f"*{space}{name}{space}*")
    print(f"{star}")

    
def fixName(name):
    if name:
        try:
            name = name.decode('string_escape')
        except Exception as error:
            name = name
    return name
