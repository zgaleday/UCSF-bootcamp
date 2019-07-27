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
    response = raw_input("Generate ramachandran plot? (y/n):").lower().strip()
    while True:
        if response == 'y':
            container = ParsePDB(loader.out_path, plot=True)
            break
        elif response == 'n':
            container = ParsePDB(loader.out_path, plot=False)
        else:
            response = raw_input("Invalid response, please enter (y/n):").lower().strip()
    #Code to dump pdb file to console. Commented out for functionality.
    # container = ParsePDB(loader.out_path)
    # container.dump_pdb()


main()