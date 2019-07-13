import requests


class PDBLoader(object):
    """A class used to take in a pdb id and retrieve the relevent file. The class places the retrieve file in the
    resources directory of the current directory space."""

    def __init__(self, id, path='resources'):
        """
        Constructor requiring only a pdb id for instantiation
        :param id: corisponding pdb id used to retrieve the pdb file, assumes to be a four character string
        :param path: the path to which the file will be stored, default set to the relative resources path
        """
        self.structure_path = 'https://www.rcsb.org/structure/'
        self.id = id
        self.path = path
        self.validate_id()
        # The defualt path leading to the pdb id structure page for use by requests


    def validate_id(self):
        """
        Checks that the given PDBID is valid. Raised a ValueError is the given id is not of the expected form or it is
        not a valid url/structural id.
        """
        response = requests.get(self.structure_path + self.id)
        if len(self.path) != 4:
            raise ValueError("PDB ID must be a 4 character string")
        if response.status_code != 200:
            raise ValueError("Invalid PDB given to constructor")