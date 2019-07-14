import sys
import pandas as pd
import numpy as np

class ParsePDB(object):
    """Generic class to parse file of pdb format.
    Relevant documentation to load_atoms and parse_ATOM can be found at:
    http://www.wwpdb.org/documentation/file-format-content/format33/sect9.html#ATOM
    """


    def __init__(self, filepath):
        """Simple constructor just requiring the file path for the pdb file of interest"""
        self.pdb_path = filepath
        self.atoms = self.load_atoms()
        # Extract relevant column from atom DF
        self.coordinate_df = self.atoms[['name', 'resSeq', 'x', 'y', 'z']]
        # Extract all c_alpha coordinates from main coord df
        self.c_alpha_df = self.coordinate_df[self.coordinate_df['name'] == 'CA']
        # Extract all C coords from main coord df
        self.c_df = self.coordinate_df[self.coordinate_df['name'] == 'C']
        # Extract all N coords from main coord df
        self.n_df = self.coordinate_df[self.coordinate_df['name'] == 'N']


    def load_atoms(self):
        """Loads the atoms into a dataframe ready for future computation.
        :return A pandas dataframe with the atoms and relevant columns as defined by pdb documentation (see above).
        """
        with open(self.pdb_path) as f:
            atoms = [self.parse_ATOM(line)[1:] for line in f if line.split()[0] == "ATOM"]
        #Column names correspond to the exact ontology defined in cited documentation.
        columns = ["serial", "name", "altLoc", "resName", "chainID", "resSeq", "iCode", "x", "y", "z",
                   "occupancy", "tempFactor", "element", "charge"]
        df = pd.DataFrame(atoms, columns=columns)
        return df

    def parse_ATOM(self, line):
        """Class to split ATOM line into parts as defined by documentation cited in class docstring (see above)
        :return list split in appropriate manner with appropriate types
        """
        return [line[:6].strip(), int(line[6:11]), line[12:16].strip(), line[16], line[17:20].strip(), line[21],
                int(line[22:26]), line[26], float(line[30: 38]), float(line[38:46]), float(line[46:54]),
                float(line[54:60]), float(line[60:66]), line[76:78].strip(), line[78:80].strip()]


    def dump_pdb(self):
        """Simple method to print out PDB file contents to console"""
        with open(self.pdb_path) as f:
            for line in f:
                sys.stdout.write(line)


pdb = ParsePDB('resources/1AXC.pdb')