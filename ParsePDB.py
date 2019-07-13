"""Generic class to parse file of pdb format"""
import pandas as pd
import numpy as np

class ParsePDB(object):

    def __init__(self, filepath):
        """Simple constructor just requiring the filepath for the pdb file of interest"""
        self.pdb_path = filepath
        self.load_atoms()


    def load_atoms(self):
        """Loads the atoms into a dataframe ready for future computation."""
        with open(self.pdb_path) as f:
            atoms = [self.parse_ATOM(line)[1:] for line in f if line.split()[0] == "ATOM"]
        #Column names corrispond to the exact ontology defined at:
        #http://www.wwpdb.org/documentation/file-format-content/format33/sect9.html#ATOM
        columns = ["serial", "name", "altLoc", "resName", "chainID", "resSeq", "iCode", "x", "y", "z",
                   "occupancy", "tempFactor", "element", "charge"]
        df = pd.DataFrame(atoms, columns=columns)
        print df.head(10)

    def parse_ATOM(self, line):
        """Class to split ATOM line into parts as defined by:
         http://www.wwpdb.org/documentation/file-format-content/format33/sect9.html#ATOM
        :return list split in appropriate manner with appropriate types
        """
        return [line[:6], int(line[6:11]), line[12:16], line[16], line[17:20], line[21], int(line[22:26]), line[26],
                float(line[30: 38]), float(line[38:46]), float(line[46:54]), float(line[54:60]), float(line[60:66]),
                line[76:78], line[78:80]]


pdb = ParsePDB('resources/1AXC.pdb')