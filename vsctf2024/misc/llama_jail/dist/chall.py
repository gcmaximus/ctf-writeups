#!/usr/local/bin/python

from exec_utils import safe_exec
def my_safe_exec(__source):
    # even MORE safe, surely nothing you can do now!!!
    assert __source.isascii(), "ascii check failed"
    blacklist = ["match", "case", "async", "def", "class", "frame", "_", "byte", "coding"]
    for x in blacklist:
        assert x not in __source, f"{x} is banned"
    return safe_exec(__source)

if __name__ == "__main__":
    __source = ""
    print("Enter code: ")
    try:
        while (inp:=input()) != "#EOF":
            __source += inp + "\n"
    except EOFError:
        pass
    try:
        my_safe_exec(__source)
    except AssertionError as err:
        print(err)