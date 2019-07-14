"""File to interact with the user on the command line interface specified"""

import sys
from PDBLoader import *
from ParsePDB import *

def main():
    id = sys.argv[1]

    #Part 1 requirement
    print(id)

    #Download pdb file
    loader = PDBLoader(id[:4])

    #Load pdb file
    container = ParsePDB(loader.out_path)
    container.dump_pdb()


main()