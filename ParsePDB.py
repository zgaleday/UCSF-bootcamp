import sys
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.font_manager import FontProperties

class ParsePDB(object):
    """Generic class to parse file of pdb format.
    Relevant documentation to load_atoms and parse_ATOM can be found at:
    http://www.wwpdb.org/documentation/file-format-content/format33/sect9.html#ATOM
    """


    def __init__(self, filepath, testing=False, plot=False):
        """Simple constructor just requiring the file path for the pdb file of interest"""
        self.pdb_path = filepath
        self.atoms = self.load_atoms()
        #TODO: Remove after done debugging
        self.atoms = self.atoms[self.atoms['chainID'] == 'A']
        # Extract relevant column from atom DF
        self.coordinate_df = self.atoms[['name', 'resSeq', 'x', 'y', 'z']]
        # Extract all c_alpha coordinates from main coord df
        self.c_alpha_df = self.coordinate_df[self.coordinate_df['name'] == 'CA']
        # Extract all C coords from main coord df
        self.c_df = self.coordinate_df[self.coordinate_df['name'] == 'C']
        # Extract all N coords from main coord df
        self.n_df = self.coordinate_df[self.coordinate_df['name'] == 'N']
        # Instantiate a numpy array to hold the b_vectors
        self.w = np.empty((self.c_alpha_df.shape[0] - 1, 3))
        # Calculate the torsion angles for the residues
        if not testing:
            self.calc_w()
            self.calc_phi()
            self.calc_psi()
        if plot:
            self.ramachandran()


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

    def calc_w(self):
        """
        Vectorized calculation of the w tortions for the entire protein.
        Sets self.w to the result of the calculation.
        Broken into steps for readability.
        """
        c_alpha_prev = self.c_alpha_df[['x', 'y', 'z']][:-1].values
        c_prev = self.c_df[['x', 'y', 'z']][:-1].values
        n_curr = self.n_df[['x', 'y', 'z']][1:].values
        c_alpha_curr = self.c_alpha_df[['x', 'y', 'z']][1:].values
        b0 = c_prev - c_alpha_prev
        b1 = n_curr - c_prev
        b2 = c_alpha_curr - n_curr
        self.w = self._calc_tortion(b0, b1, b2)

    def calc_phi(self):
        """
        Vectorized calculation of the phi tortions for the entire protein.
        Sets self.phi to the result of the calculation.
        Broken into steps for readability.
        """
        c_prev = self.c_df[['x', 'y', 'z']][:-1].values
        n_curr = self.n_df[['x', 'y', 'z']][1:].values
        c_alpha_curr = self.c_alpha_df[['x', 'y', 'z']][1:].values
        c_curr = self.c_df[['x', 'y', 'z']][1:].values
        b0 = n_curr - c_prev
        b1 =  c_alpha_curr - n_curr
        b2 = c_curr - c_alpha_curr
        self.phi = self._calc_tortion(b0, b1, b2)

    def calc_psi(self):
        """
        Vectorized calculation of the psi tortions for the entire protein.
        Sets self.psi to the result of the calculation.
        Broken into steps for readability.
        """
        n_curr = self.n_df[['x', 'y', 'z']][:-1].values
        c_alpha_curr = self.c_alpha_df[['x', 'y', 'z']][:-1].values
        c_curr = self.c_df[['x', 'y', 'z']][:-1].values
        n_next = self.n_df[['x', 'y', 'z']][1:].values
        b0 = c_alpha_curr - n_curr
        b1 = c_curr - c_alpha_curr
        b2 = n_next - c_curr
        self.psi = self._calc_tortion(b0, b1, b2)

    def _calc_tortion(self, b0, b1, b2):
        """
        Vectorized method to determine the tortion angle give the appropriate b vectors for the desired tortion.
        :param b0: first vector array (np array of floats)
        :param b1: second vector array (np array of floats)
        :param b2: third vector array (np array of floats)
        :return: A numpy array of the appropriate torsion angles as determined using the angle between the vector planes
        normals.
        """
        n1 = np.cross(b0, b1)
        n1 /= np.sqrt(np.sum(n1 * n1, axis=1))[:, None]
        n2 = np.cross(b1, b2)
        n2 /= np.sqrt(np.sum(n2 * n2, axis=1))[:, None]
        b1_norm = b1 / np.sqrt(np.sum(b1 * b1, axis=1))[:, None]
        m1 = np.cross(n1, b1_norm)
        x = np.sum(n1 * n2, axis=1)
        y = np.sum(m1 * n2, axis=1)
        return -np.arctan2(y, x) * 180 / np.pi

    def ramachandran(self):
        """
        Plots the torsion anlge as a ramachandran plot.
        """
        prop = FontProperties()
        prop.set_file('resources/STIXGeneral.ttf')
        ax = plt.scatter(self.phi, self.psi)
        plt.xlabel(u"\u03C6", fontproperties=prop)
        plt.ylabel(u"\u03C8", fontproperties=prop)
        plt.show()


pdb = ParsePDB('resources/1AXC.pdb')