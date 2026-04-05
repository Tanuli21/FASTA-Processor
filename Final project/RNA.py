from sequence import Sequence

class RNAseq(Sequence):
    def __init__(self,header,sequence):
        super().__init__(header,sequence)

    #Overriden method to calculate AT content
    def get_at_content(self):
        count_a = 0
        count_u = 0
        # check the base type and increment the appropriate counter variable
        for base in self.sequence:
            if base == "A":
                count_a += 1
            elif base == "T":
                count_u += 1
        # get total length of the DNA sequence
        total_length = len(self.sequence)
        # get AT content in the DNA sequence
        content_at = ((count_a + count_u) / total_length) * 100
        return content_at





