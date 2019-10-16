from sys import argv
from parts.parser import Parser

if __name__ == '__main__':
    file_name = argv[1]
    with open(file_name) as file:
        parser = Parser(file)
