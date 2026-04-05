from sequence import Sequence

#Create subclass DNAseq using Sequence as the parent class
class DNAseq(Sequence):
    #Define the constructor including all attributes
    def __init__(self,header,sequence):
        #To avoid repetition, use super keyword. Call parent constructor with type='DNA'
        super().__init__(header,sequence)

    #Define a method to get AT content
    def get_at_content(self):
        count_a = 0
        count_t = 0
        # check the base type and increment the appropriate counter variable
        for base in self.sequence:
            if base == "A":
                count_a += 1
            elif base == "T":
                count_t += 1
        # get total length of the DNA sequence
        total_length = len(self.sequence)
        # get AT content in the DNA sequence
        content_at = ((count_a + count_t) / total_length) * 100
        return content_at





