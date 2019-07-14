"""File to interact with the user on the command line interface specified"""

import sys
from PDBLoader import *
from ParsePDB import *

def main():
    id = sys.argv[1]

    #Part 1 requirement
    print(id)

    #Download pdb file
    PDBLoader(id[:4])


main()