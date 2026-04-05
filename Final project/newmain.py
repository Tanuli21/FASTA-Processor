''''
Author : Tanuli Erathna
Program : FASTA processor
'''

import tkinter as tk
from tkinter import filedialog,messagebox,scrolledtext,ttk
from sequence import Sequence #Import sequence class
import os


#Create GUI class to handle the user interface
class FastaProcessorGUI:
    #Define constructor
    def __init__(self,root):
        #store the main window (root) in an instance variable
        self.root = root
        #Set the window title
        self.root.title("FASTA Processor")
        #set the window size
        self.root.geometry("800x600")
        self.root.iconbitmap('logo.ico')

        #color scheme
        self.colors={
            'primary': '#2c3e50',  # Dark blue for titles
            'secondary': '#3498db',  # Blue for buttons
            'accent': '#1abc9c',  # Teal for highlights
            'background': '#f5f7fa',  # Light background
            'surface': '#ffffff',  # White for panels
            'text': '#2c3e50',  # Dark text
            'text_light': '#7f8c8d',  # Light text
            'success': '#27ae60',  # Success green
            'warning': '#f39c12',  # Warning orange
            'error': '#e74c3c',
        }

        #configure root window background
        self.root.configure(bg=self.colors['background'])

        #style configuration
        self.setup_styles()

        self.sequences=[] #LIST of sequence objects
        self.output_dir='output_files'
        self.files_to_combine=[]

        #Create output directory
        if not os.path.exists(self.output_dir):
            os.makedirs(self.output_dir)

        #create main interface
        self.create_interface()

    #Setup ttk styles
    def setup_styles(self):
        style = ttk.Style()
        style.theme_use('clam')

        # Configure colors for all widgets
        style.configure('TFrame', background=self.colors['background'])
        style.configure('TLabel', background=self.colors['background'],foreground=self.colors['text'], font=('Segoe UI', 10))
        style.configure('TButton', background=self.colors['secondary'],foreground='white', borderwidth=1, font=('Segoe UI', 10, 'bold'))
        style.map('TButton',background=[('active', self.colors['accent']),('pressed', self.colors['primary'])])

        # Title style
        style.configure('Title.TLabel',font=('Segoe UI', 18, 'bold'),foreground=self.colors['primary'],background=self.colors['background'])

        # Header frame style
        style.configure('Header.TLabelframe',background=self.colors['surface'],relief='solid',borderwidth=1)
        style.configure('Header.TLabelframe.Label',background=self.colors['surface'],foreground=self.colors['primary'],font=('Segoe UI', 11, 'bold'))

        # Action button style
        style.configure('Action.TButton', background=self.colors['secondary'],foreground='white',font=('Segoe UI', 10, 'bold'),padding=8)
        style.map('Action.TButton',background=[('active', self.colors['accent']),('pressed', self.colors['primary'])])

        # Success button style
        style.configure('Success.TButton',background=self.colors['success'],foreground='white')

        # Warning button style
        style.configure('Warning.TButton',background=self.colors['warning'],foreground='white')


    #create main notebook interface
    def create_interface(self):
        #create notebook(tabbed interface)
        self.notebook = ttk.Notebook(self.root)
        self.notebook.pack(fill=tk.BOTH,expand=True,padx=10,pady=10)

        #create tabs
        self.create_parse_tab()
        self.create_operations_tab()
        self.create_help_tab()

    # Parse and analyze FASTA files
    def create_parse_tab(self):
        tab = ttk.Frame(self.notebook)
        self.notebook.add(tab, text='Parse & Analyze')

        #configure tab background
        tab.configure(style='TFrame')

        # Title
        title = ttk.Label(tab, text="FASTA Sequence Analyzer",style='Title.TLabel')
        title.pack(fill=tk.X,pady=(0,10))

        # File selection frame
        file_frame = ttk.LabelFrame(tab,text='File selection',style='Header.TLabelframe',padding=10)
        file_frame.pack(pady=5, padx=10, fill=tk.X)

        self.file_path=tk.StringVar(value='No file selected')
        ttk.Entry(file_frame,textvariable=self.file_path,width=60,state='readonly').pack(side=tk.LEFT,padx=5)
        ttk.Button(file_frame,text='Browse',command=self.browse_file,style='Action.TButton').pack(side=tk.LEFT,padx=5)

        #options frame
        options_frame=ttk.LabelFrame(tab,text='Analysis Options',style='Header.TLabelframe',padding=10)
        options_frame.pack(pady=5, padx=10, fill=tk.X)

        ttk.Label(options_frame,text='Show content:').pack(side=tk.LEFT,padx=5)
        self.content_type=tk.StringVar(value='both')

        radio_frame=ttk.Frame(options_frame)
        radio_frame.pack(padx=10, side=tk.LEFT)

        options=[('None','none'),('GC','GC'),('AT','AT'),('Both','both')]
        #store radio buttons for styling
        self.radio_buttons=[]
        for text, value in options:
            rb=tk.Radiobutton(radio_frame,text=text,variable=self.content_type,value=value,font=('Segoe UI', 11, 'bold'),bg=self.colors['surface'],fg=self.colors['text'],selectcolor='#7f8c8d',activebackground=self.colors['background'],activeforeground=self.colors['primary'],padx=15,pady=5)
            rb.pack(side=tk.LEFT,padx=8,pady=3)
            self.radio_buttons.append(rb)

        #action buttons
        action_frame = ttk.LabelFrame(tab, text='Actions', style='Header.TLabelframe', padding=10)
        action_frame.pack(pady=5, padx=10, fill=tk.X)

        btn_frame=ttk.Frame(action_frame)
        btn_frame.pack(pady=10)

        ttk.Button(btn_frame,text="Parse & Analyze",command=self.parse_file,style='Action.TButton').pack(side=tk.LEFT,padx=5)
        ttk.Button(btn_frame, text="Clear results", command=self.clear_results, style='Warning.TButton').pack(side=tk.LEFT, padx=5)
        ttk.Button(btn_frame, text="Count sequences", command=self.count_sequences, style='Action.TButton').pack(side=tk.LEFT, padx=5)

        btn_frame2 = ttk.Frame(action_frame)
        btn_frame2.pack(pady=5)

        ttk.Button(btn_frame2, text="Save with Enhanced Headers", command=self.save_enhanced_file,style='Success.TButton', width=25).pack(side=tk.LEFT, padx=5)

        #Results display
        results_frame = ttk.LabelFrame(tab, text='Analysis Results',style='Header.TLabelframe', padding=10)
        results_frame.pack(pady=5, padx=10, fill=tk.BOTH, expand=True)

        # Add scrollable text widget
        self.results_text = scrolledtext.ScrolledText(results_frame, height=20, font=('Consolas', 10),bg='white',fg=self.colors['text'],relief='flat',borderwidth=1,state='disabled')
        self.results_text.pack(fill=tk.BOTH, expand=True)



    #create file operation tab
    def create_operations_tab(self):
        tab=ttk.Frame(self.notebook)
        self.notebook.add(tab,text='File Operations')

        #Title
        title=ttk.Label(tab,text="File operations",style='Title.TLabel')
        title.pack(fill=tk.X,pady=(20,15))

        #split section
        split_frame=ttk.LabelFrame(tab,text='Split sequences',padding=15)
        split_frame.pack(pady=10,padx=20, fill=tk.X)

        ttk.Label(split_frame,text='Split multi-FASTA into individual FASTA files:').pack(anchor=tk.W)

        btn_split_frame=ttk.Frame(split_frame)
        btn_split_frame.pack(pady=10)

        ttk.Button(btn_split_frame,text='Split Sequences',command=self.split_sequences,style='Action.TButton').pack(side=tk.LEFT,padx=10)
        ttk.Button(btn_split_frame,text='Refresh list',command=self.refresh_files,style='Action.TButton').pack(side=tk.LEFT,padx=10)

        # Generated files list
        files_frame = ttk.Frame(split_frame)
        files_frame.pack(fill=tk.X, pady=15)

        ttk.Label(files_frame, text="Generated Files:").pack(anchor=tk.W)
        self.files_listbox = tk.Listbox(files_frame, height=8,font=('Segoe UI', 9))
        self.files_listbox.pack(fill=tk.X, pady=5)

        ttk.Button(split_frame, text="Download Selected",command=self.download_file, style='Success.TButton',padding=8).pack(pady=10)


        # Combine section
        combine_frame = ttk.LabelFrame(tab, text="Combine Files", padding=10)
        combine_frame.pack(fill=tk.X, padx=10, pady=10)

        ttk.Label(combine_frame,text="Combine multiple FASTA files:").pack(anchor=tk.W)

        self.combine_listbox = tk.Listbox(combine_frame, height=6,font=('Segoe UI', 9))
        self.combine_listbox.pack(fill=tk.X, pady=10)

        btn_combine_frame = ttk.Frame(combine_frame)
        btn_combine_frame.pack(pady=15)

        ttk.Button(btn_combine_frame, text="Add Files",command=self.add_files, style='Action.TButton').pack(side=tk.LEFT, padx=10)
        ttk.Button(btn_combine_frame, text="Combine",command=self.combine_files, style='Action.TButton').pack(side=tk.LEFT, padx=10)
        ttk.Button(btn_combine_frame, text="Clear",command=self.clear_combine_list, style='Action.TButton').pack(side=tk.LEFT, padx=10)

    #create help tab
    def create_help_tab(self):
        tab = ttk.Frame(self.notebook)
        self.notebook.add(tab, text='Help')

        help_text = """
        FASTA Processor - Quick Guide

        1. PARSE & ANALYZE:
           • Browse and select a FASTA file
           • Choose what content to display (GC, AT, Both, None)
           • Click 'Parse & Analyze' to process

        2. FILE OPERATIONS:
           • Split: Save each sequence as separate file
           • Combine: Merge multiple FASTA files

        3. OUTPUT:
           • Files are saved in 'output_files/' folder
           • Click 'Download Selected' to save anywhere

        Supported Formats: .fasta, .fa, .fna
        """

        help_label = ttk.Label(tab, text=help_text,
                               font=('Segoe UI', 11),
                               justify=tk.LEFT, padding=20)
        help_label.pack(fill=tk.BOTH, expand=True)

    def browse_file(self):
        #open a file dialog for user to select a FASTA file
        #opens a system file selection dialog
        file_path = filedialog.askopenfilename(title="Select FASTA file",filetypes=[("FASTA Files","*.fasta *.fa *.fna"),('All files','*.*')])
        #if user selected a file (not canceled)
        if file_path:
            self.file_path.set(file_path)

    def parse_file(self):
        #process the selected FASTA file and display results
        #get the file path from the label
        file_path = self.file_path.get()
        #check if no file is selected
        if file_path=='No file selected':
            #show error message using messagebox
            messagebox.showerror("Error","No file selected")
            return #exit the method
        try:
            #-Process the file -
            #Parse the file
            self.sequences=Sequence.parse_fasta(file_path)

            #clean sequences after parsing
            for seq in self.sequences:
                if seq.type in ['DNA','RNA']:
                    seq.sequence=Sequence.clean_nucleotide_sequence(seq.sequence)
                elif seq.type=='Protein':
                    seq.sequence=Sequence.clean_protein_sequence(seq.sequence)
                #update length after cleaning
                seq.length=len(seq.sequence)

            self.display_results()
            # Update status
            messagebox.showinfo("Success",f"Successfully parsed {len(self.sequences)} sequence(s)")

        except FileNotFoundError:
            messagebox.showerror("Error", f"File not found: {file_path}")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to parse file:\n{str(e)}")

    #Display analysis results for all sequences
    def display_results(self):
        #enable widget for writing
        self.results_text.config(state='normal')
        self.results_text.delete('1.0', tk.END)
        if not self.sequences:
            self.results_text.insert(tk.END,'No sequences found')
            #disable again
            self.results_text.config(state='disabled')
            return

        self.results_text.insert(tk.END, f" FASTA FILE ANALYSIS\n")
        self.results_text.insert(tk.END, f"Total Sequences: {len(self.sequences)}\n")
        self.results_text.insert(tk.END, "=" * 207 + "\n\n")

        for i, seq in enumerate(self.sequences, 1):
            self.display_sequence(i, seq)
        #disable widget after writing
        self.results_text.config(state='disabled')

    #Display sequence information
    def display_sequence(self, index, seq):
        #enable widget for writting
        current_state=self.results_text.cget('state')
        if current_state == 'disabled':
            self.results_text.config(state='normal')

        self.results_text.insert(tk.END, f"Sequence #{index}\n")
        self.results_text.insert(tk.END, f"Header: {seq.header}\n")
        self.results_text.insert(tk.END, f"Type: {seq.type}\n")
        self.results_text.insert(tk.END, f"Length: {seq.length}\n")

        # Add content based on selection
        content_type = self.content_type.get()
        if content_type != "none" and seq.type in ['DNA', 'RNA']:
            if hasattr(seq, 'get_at_content'):
                at_content = seq.get_at_content()
                label = "AU" if seq.type == "RNA" else "AT"
                if content_type in ['AT', 'both']:
                    self.results_text.insert(tk.END, f"{label} Content: {at_content:.2f}%\n")

            gc_content = seq.get_gc_content()
            if gc_content is not None and content_type in ['GC', 'both']:
                self.results_text.insert(tk.END, f"GC Content: {gc_content:.2f}%\n")

        # Protein specific
        if seq.type == "Protein" and hasattr(seq, 'calculate_hydrophobicity'):
            hydrophobicity = seq.calculate_hydrophobicity()
            self.results_text.insert(tk.END, f"Hydrophobicity: {hydrophobicity:.2f} \n")

        self.results_text.insert(tk.END, "-" * 207 + "\n\n")

    #Clear result display
    def clear_results(self):
        self.results_text.config(state='normal')
        self.results_text.delete('1.0', tk.END)
        self.results_text.config(state='disabled')

    #split sequences into individual files
    def split_sequences(self):
        if not self.sequences:
            messagebox.showwarning("Warning", "Parse a file first!")
            return


        try:
            #use the split sequence from list method
            output_files=Sequence.split_sequences_from_list(self.sequences,self.output_dir)

            #refresh the file list display
            self.refresh_files()

            messagebox.showinfo("Success", f"Successfully split {len(output_files)} sequences")

        except Exception as e:
            messagebox.showerror("Error", f"Failed to split sequences :\n{str(e)}")


    #refresh file list display
    def refresh_files(self):
        self.files_listbox.delete(0, tk.END)

        if os.path.exists(self.output_dir):
            fasta_files=[]
            for f in os.listdir(self.output_dir):
                if f.endswith('.fasta'):
                    fasta_files.append(f)
            if fasta_files:
                for f in sorted(fasta_files):
                    self.files_listbox.insert(tk.END, f)
                print(f'Found {len(fasta_files)} fasta files in {self.output_dir}')

            else:
                self.files_listbox.insert(tk.END, "No FASTA files found")
                self.files_listbox.insert(tk.END, f"Check directory: {self.output_dir}")
        else:
            self.files_listbox.insert(tk.END, f"Output directory does not exist")
            self.files_listbox.insert(tk.END, f"Expected: {self.output_dir}")


    #download a selected file
    def download_file(self):
        selection = self.files_listbox.curselection()
        if not selection:
            messagebox.showwarning("Warning", "Select a file first!")
            return

        # Get the selected filename
        filename = self.files_listbox.get(selection[0])

        # Check if it's a message, not a file
        if filename in ["No FASTA files found", "Output directory does not exist", "Check directory:"]:
            messagebox.showwarning("Warning", "Please select a valid file!")
            return

        # Skip if it starts with "Check directory" or other messages
        if filename.startswith("Check directory") or filename.startswith("Expected:"):
            messagebox.showwarning("Warning", "No valid file selected!")
            return

        filepath = os.path.join(self.output_dir, filename)

        # Check if file exists
        if not os.path.exists(filepath):
            messagebox.showerror("Error", f"File not found:\n{filepath}")
            return

        # Ask where to save
        save_path = filedialog.asksaveasfilename(
            title="Save File",
            initialfile=filename,
            defaultextension=".fasta",
            filetypes=[("FASTA files", "*.fasta"), ("All files", "*.*")]
        )

        if save_path:
            import shutil
            shutil.copy(filepath, save_path)
            messagebox.showinfo("Success", f"Saved to {save_path}")
    #Add files to combine list
    def add_files(self):
        files = filedialog.askopenfilenames(title="Select FASTA files",filetypes=[("FASTA files", "*.fasta *.fa *.fna")])

        for f in files:
            if f not in self.files_to_combine:
                #add only the basename to the listbox for display
                self.combine_listbox.insert(tk.END, os.path.basename(f))
                #add the full path to the list
                self.files_to_combine.append(f)
                if not hasattr(self, 'files_to_combine'):
                    self.files_to_combine = []
                self.files_to_combine.append(f)

    #Combine selected files
    def combine_files(self):
        if not hasattr(self, 'files_to_combine') or len(self.files_to_combine) < 2:
            messagebox.showwarning("Warning", "Add at least 2 files!")
            return

        save_path = filedialog.asksaveasfilename(title="Save Combined File",defaultextension=".fasta")

        if save_path:
            Sequence.combine_files(self.files_to_combine, save_path)
            messagebox.showinfo("Success", f"Combined to {save_path}")
            self.clear_combine_list()

    #clear combine list
    def clear_combine_list(self):
        self.combine_listbox.delete(0, tk.END)
        if hasattr(self, 'files_to_combine'):
            self.files_to_combine.clear()

    def count_sequences(self):
        file_path=self.file_path.get()
        if file_path=='No file selected':
            messagebox.showwarning("Warning", "Select a file first!")
            return
        try:
            count = Sequence.count_sequences(file_path)
            messagebox.showinfo("Success", f"Successfully count {count} sequences")

        except Exception as e:
            messagebox.showerror("Error", f"Failed to count sequences :\n{str(e)}")

    def save_enhanced_file(self):
        if not self.sequences:
            messagebox.showwarning("Warning", "Parse a file first!")
            return
        try:
            output_file=filedialog.asksaveasfilename(title='Save enahnced FASTA file',defaultextension=".fasta",filetypes=[("FASTA files", "*.fasta *.fa *.fna")])
            if output_file:
                #use static method to create enhanced file
                Sequence.add_content_to_file(self.file_path.get(),output_file,self.content_type.get())
                messagebox.showinfo("Success", f"Saved to {output_file}")

        except Exception as e:
            messagebox.showerror("Error", f"Failed to save enhanced file :\n{str(e)}")

if __name__ == "__main__":
    root = tk.Tk()
    app = FastaProcessorGUI(root)
    root.mainloop()