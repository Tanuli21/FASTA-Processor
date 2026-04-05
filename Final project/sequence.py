#Define parent class
class Sequence:

    #Create constructor
    def __init__(self,header,sequence):
        self.header = header
        self.sequence = sequence.upper()
        self.length = len(sequence)
        self.type = self.get_seq_type(sequence)



    # Get the sequence type using static method
    @staticmethod
    def get_seq_type(sequence):

        if not sequence:
            return 'Empty'

        if sequence.startswith('M'):
            return 'Protein'

        elif 'T' in sequence and 'U' not in sequence:
            return 'DNA'


        elif 'U' in sequence and 'T' not in sequence:
            return 'RNA'

        else:
            return 'Unknown'


    # Method to calculate GC content only for DNA and RNA
    def get_gc_content(self):
        # Check whether sequence is DNA or RNA
        if self.type == 'DNA' or self.type == 'RNA':
            count_g = 0
            count_c = 0
            # check the base type and increment the appropriate counter variable
            for base in self.sequence:
                if base == "G":
                    count_g += 1
                elif base == "C":
                    count_c += 1
            # get total length of the DNA sequence
            total_length = len(self.sequence)
            # get GC content in the DNA sequence
            content_gc = ((count_g + count_c) / total_length) * 100
            return content_gc
        else:
            return None  # Not applicable for protein


    #Parse FASTA file and return appropriate objects
    @staticmethod
    def parse_fasta(fil_path):
        sequences = []
        with open(fil_path,'r') as f:
            current_header = ''
            current_sequence = ''
            for line in f:
                line = line.strip() #To remove whitespaces
                if line.startswith('>'): #To identify header line
                    if current_header:
                        #clean the accumulated sequence-split the sequence at any white space, tab or newline character and join bases
                        cleaned_seq=''.join(current_sequence.split()).upper()
                        sequences.append(Sequence.create_sequence(current_header,cleaned_seq))
                    current_header=line[1:] #Remove >
                    current_sequence = ''

                else:
                    current_sequence += line

            if current_header:
                cleaned_seq=''.join(current_sequence.split()).upper()
                sequences.append(Sequence.create_sequence(current_header,cleaned_seq))

        return sequences

    # method to split multiple FASTA sequences and save each sequence in separate file
    @staticmethod
    def split_sequences_from_list(sequences, output_dir):  # list of sequence objects are used as an argument

        import os

        # Create output directory if it doesn't exist
        if not os.path.exists(output_dir):
            os.makedirs(output_dir)

        output_files = []

        # Write each sequence to a separate file
        for i, seq in enumerate(sequences, 1):
            filename = os.path.join(output_dir,f"{seq.header}.fasta")

            # Write the sequence to file
            with open(filename, 'w') as f:
                f.write(f'>{seq.header}\n')
                # Write sequence in 80-character lines
                for j in range(0, len(seq.sequence), 80):
                    f.write(seq.sequence[j:j + 80] + '\n')

            output_files.append(filename)

        return output_files

    #Factory method to create appropriate sequence object - import inside the method to avoid circular import
    @staticmethod
    def create_sequence(header,sequence):
        seq_type = Sequence.get_seq_type(sequence) #Detect sequence type

        #conditional object creation
        if seq_type == 'DNA':
            from DNA import DNAseq
            return DNAseq(header,sequence) #create DNA specific object
        elif seq_type == 'RNA':
            from RNA import RNAseq
            return RNAseq(header,sequence)
        elif seq_type == 'Protein':
            from protein import ProteinSeq
            return ProteinSeq(header,sequence)
        else:
            return Sequence(header,sequence) #Generic sequence

    #Combine multiple FASTA files into one
    @staticmethod
    def combine_files(file_paths,output_file):
        with open(output_file,'w') as output_file:
            for file_path in file_paths:
                with open(file_path,'r') as infile: #Open input files one by one
                    output_file.write(infile.read()) #Read input file and write it in the output file
                    output_file.write('\n')
        return output_file

    # Method remove unknown characters from nucleotide sequence
    @staticmethod
    def clean_nucleotide_sequence(sequence):
        valid_nucleotides = set('ATCGUNatcgun')
        cleaned = ''.join(char.upper() for char in sequence if char.upper() in valid_nucleotides)
        return cleaned

    # Method to remove unknown characters from protein sequence
    @staticmethod
    def clean_protein_sequence(sequence):
        valid_amino_acids = set('ACDEFGHIKLMNPQRSTVWYXacdefghiklmnpqrstvwyx')
        cleaned = ''.join(char.upper() for char in sequence if char.upper() in valid_amino_acids)
        return cleaned


    def add_content_to_header(self, content_type='both'):
        header_parts = [self.header]

        # Always add length
        header_parts.append(f'Length:{self.length}bp')

        # Add content if requested and applicable
        if content_type != 'none' and self.type in ['DNA', 'RNA']:
            at_content = self.get_at_content() if hasattr(self, 'get_at_content') else None
            gc_content = self.get_gc_content()

            if content_type in ['AT', 'both'] and at_content is not None:
                label = 'AU' if self.type == 'RNA' else 'AT'
                header_parts.append(f'{label}:{at_content:.1f}%')

            if content_type in ['GC', 'both'] and gc_content is not None:
                header_parts.append(f'GC:{gc_content:.1f}%')

        return '|'.join(header_parts)

    @staticmethod
    def add_content_to_file(input_file, output_file, content_type='both'):

        # Parse sequences
        sequences = Sequence.parse_fasta(input_file)

        with open(output_file, 'w') as out_f:
            for seq in sequences:
                # Get enhanced header with content
                enhanced_header = seq.add_content_to_header(content_type)
                out_f.write(f'>{enhanced_header}\n')

                # Write sequence in 80-character lines
                for i in range(0, len(seq.sequence), 80):
                    out_f.write(seq.sequence[i:i + 80] + '\n')

        return output_file

    #method to calculate the number of sequences in a given file
    @staticmethod
    def count_sequences(file_path):
        count=0
        with open(file_path,'r') as f:
            for line in f:
                if line.startswith('>'):
                    count += 1
        return count












