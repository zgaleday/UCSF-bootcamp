import requests
import os


class PDBLoader(object):
    """A class used to take in a pdb id and retrieve the relevent file. The class places the retrieve file in the
    resources directory of the current directory space."""

    def __init__(self, id, path='resources/'):
        """
        Constructor requiring only a pdb id for instantiation
        :param id: corisponding pdb id used to retrieve the pdb file, assumes to be a four character string
        :param path: the path to which the file will be stored, default set to the relative resources path.
        The indicated path must exist.
        """
        # The defualt path leading to the pdb id structure page for use by requests
        self.structure_path = 'https://files.rcsb.org/download/'
        self.id = id.upper()
        self.path = path
        if not os.path.exists(self.path):
            raise ValueError("Indicated directory given as 'path' arguement does not exist.")
        self.validate_id()
        self.out_path = self.path + self.id + ".pdb"
        self.retrieve_pdb()


    def validate_id(self):
        """
        Checks that the given PDBID is valid. Raised a ValueError is the given id is not of the expected form or it is
        not a valid url/structural id.
        """
        response = requests.get(self.structure_path + self.id + ".pdb")
        if len(self.id) != 4:
            raise ValueError("PDB ID must be a 4 character string")
        if response.status_code != 200:
            raise ValueError("Invalid PDB given to constructor")


    def retrieve_pdb(self):
        """
        Retrieves the indicated pdb file from the standardized url structure. Writes the file to the indicated directory
        from the constructor with the name of id.pdb.
        :return: None
        """
        response = requests.get(self.structure_path + self.id + ".pdb")
        f = open(self.out_path, 'wb')
        f.write(response.content)
        f.close()


