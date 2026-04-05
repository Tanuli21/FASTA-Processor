from sequence import Sequence

class ProteinSeq(Sequence):
    def __init__(self,header,sequence):
        super().__init__(header,sequence)

    # define a method to get the hydrophobicity
    def calculate_hydrophobicity(self):
        seq = self.sequence

        # get the total count of amino acids in the sequence
        total = len(seq)

        # list for hydrophobic acids
        aa = ['A', 'I', 'L', 'M', 'F', 'W', 'Y', 'V']
        count = 0

        for amino_acid in seq:
            if amino_acid.upper() in aa:
                count += 1
        self.hydrophobicity = (count / total) * 100
        return self.hydrophobicity