import collections
import os
import xarray as xr
import numpy as np
import pandas as pd
from typing import TextIO, Generator, Union  # Generator[str]
from pathlib import Path

# Execute subprocess functions
def run_get_igor_exec_path():
    """Return IGoR executable path"""
    import subprocess
    p1 = subprocess.run(["which", "igor"], capture_output=True, text=True)
    return p1.stdout.replace('\n', '')

def run_get_igor_datadir():
    """Return IGoR default data dir (default models and demo data) path"""
    import subprocess
    igor_exec_path = run_get_igor_exec_path()
    p2 = subprocess.run([igor_exec_path, "-getdatadir"], capture_output=True, text=True)
    return p2.stdout.replace('\n', '')

    """
    cmd = "which igor"
    p = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE)
    line = p.stdout.readline()
    igor_exec_path = line.decode("utf-8").replace('\n', '')
    p.wait()
    p.kill()

    cmd = igor_exec_path + " -getdatadir"
    p = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE)
    line = p.stdout.readline()
    igor_datadir = line.decode("utf-8").replace('\n', '')
    p.wait()
    p.kill()
    return igor_datadir
    """

    """
    # FIXME: ADD A WITH TO SUBPROCESS with subprocess.Popen(...) as p and a p.kill()
    p = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    # with subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT) as p:
    stdout = []
    # with p.stdout as p_stdout:
    while True:
        line = p.stdout.readline()
        line = line.decode("utf-8")
        stdout.append(line)
        # print (line, end='')
        if line == '' and p.poll() != None:
            break
    p.communicate()
    p.stdout.close()
    p.kill()
    return (''.join(stdout)).replace('\n','')
    """

def run_get_random_string():
    """
    Return random string using subprocess
    """
    # FIXME: CHANGE TO ANOTHER WAY WITHOUT USING SYSTEM OR SUBPROCESS.
    import subprocess
    p = subprocess.run("head /dev/urandom | tr -dc A-Za-z0-9 | head -c10", shell=True, capture_output=True, text=True)
    return p.stdout.replace('\n', '')

def run_get_igor_wd():
    """Return current directory, that can be use as default wd"""
    import subprocess
    p = subprocess.run("pwd", shell=True, capture_output=True, text=True)
    return p.stdout.replace('\n', '')


# Get default filenames functions
def get_default_fln_dict_ref_genomes_species_chain(IgorSpecie:str, IgorChain:str, modelspath=None, ref_genome_path=None):
    """
    Return a dictionary with the paths of the genomic references ref_genome files.
    :param IgorSpecie: Species directory name in IGoR's directory structure
    :param IgorChain: Chain directory name in IGoR's directory structure
    :return: dictionary with the default names and paths for IGoR.
    """
    if modelspath is None:
        try:
            modelspath = run_get_igor_datadir() + "/models"
            print("modelpath : ", modelspath)
        except Exception as e:
            print("ERROR: getting default igor datadir.", e)

    IgorModelPath = modelspath + "/" + IgorSpecie + "/" + IgorChain + "/"
    if ref_genome_path is None:
        ref_genome_path = IgorModelPath + "/" + "ref_genome"

    ref_genome_fln_dict = dict()
    # check if file exist then make the assignment
    ref_genome_path = ref_genome_path + "/"
    ref_genome_fln_dict['fln_genomicVs'] = ref_genome_path + "genomicVs.fasta"
    ref_genome_fln_dict['fln_genomicJs'] = ref_genome_path + "genomicJs.fasta"
    ref_genome_fln_dict['fln_genomicDs'] = ref_genome_path + "genomicDs.fasta"

    ref_genome_fln_dict['fln_V_gene_CDR3_anchors'] = ref_genome_path + "V_gene_CDR3_anchors.csv"
    ref_genome_fln_dict['fln_J_gene_CDR3_anchors'] = ref_genome_path + "J_gene_CDR3_anchors.csv"

    return ref_genome_fln_dict

def get_default_fln_names_for_model_dir(model_dir_path, ref_genome_path=None, models_path=None):
    """
    Return a dict with default names for files
    :param model_dir_path: Root of species chain directory. Example model_dir_path="human/tcr_beta/"
    """
    model_dir_path = model_dir_path + "/"
    if ref_genome_path is None:
        ref_genome_path = model_dir_path + "ref_genome"
    ref_genome_fln_dict = get_default_ref_genome_fln_paths(ref_genome_path=ref_genome_path)

    if models_path is None:
        models_path = model_dir_path + "models"
    models_fln_dict = get_default_models_fln_paths(models_path=models_path)

    return {**ref_genome_fln_dict, **models_fln_dict}

def get_default_ref_genome_fln_paths(ref_genome_path="ref_genome"):
    """
    Get default filenames for genome template references.
    :param ref_genome_path: Default ref_genome directory name
    """

    ref_genome_fln_dict = dict()
    ref_genome_path = ref_genome_path + "/"
    ref_genome_fln_dict['fln_genomicVs'] = ref_genome_path + "genomicVs.fasta"
    ref_genome_fln_dict['fln_genomicJs'] = ref_genome_path + "genomicJs.fasta"
    ref_genome_fln_dict['fln_genomicDs'] = ref_genome_path + "genomicDs.fasta"

    ref_genome_fln_dict['fln_V_gene_CDR3_anchors'] = ref_genome_path + "V_gene_CDR3_anchors.csv"
    ref_genome_fln_dict['fln_J_gene_CDR3_anchors'] = ref_genome_path + "J_gene_CDR3_anchors.csv"

    return ref_genome_fln_dict

def get_default_models_fln_paths(models_path="models"):
    """
    Get default filenames for models directory.
    :param models_path: models directory name
    """
    models_fln_dict = dict()
    models_path = models_path + "/"
    models_fln_dict['fln_model_parms'] = models_path + "model_parms.txt"
    models_fln_dict['fln_model_marginals'] = models_path + "model_marginals.txt"

    return models_fln_dict

def get_default_models_paths_species_chain(IgorSpecie, IgorChain, modelpath=None):  # rcParams['paths.igor_models']):
    """
    :return IgorModel loaded with the default location for specie and chain
    """
    # IGoR run parameters
    # IgorSpecie    = specie #"mouse"
    # IgorChain     = chain #"tcr_beta"
    if modelpath is None:
        try:
            modelpath = run_get_igor_datadir() + "/models"
            print("modelpath : ", modelpath)
        except Exception as e:
            print("ERROR: getting default igor datadir.", e)

    IgorModelPath = modelpath + "/" + IgorSpecie + "/" + IgorChain + "/"
    # print("Loading default IGoR model from path : ", IgorModelPath)
    # FIXME: FIND A WAY TO GENERALIZE THIS WITH SOMEKIND OF STANDARD NAME
    flnModelParms = IgorModelPath + "models/model_parms.txt"
    flnModelMargs = IgorModelPath + "models/model_marginals.txt"
    # print("Parms filename: ", flnModelParms)
    # print("Margs filename: ", flnModelMargs)
    # print("-" * 50)
    return flnModelParms, flnModelMargs

def make_igor_directories(gene: str, specie: str, modelspath=None):
    """
    Make directories for all models path root gene species
    :param gene: Gene name
    :param specie: species
    """
    if modelspath is None:
        modelspath = "models"

    os.system("mkdir -p " + modelspath)
    os.system("mkdir -p " + modelspath + "/" + specie)
    os.system("mkdir -p " + modelspath + "/" + specie + "/" + gene)
    os.system("mkdir -p " + modelspath + "/" + specie + "/" + gene + "/ref_genome")
    os.system("mkdir -p " + modelspath + "/" + specie + "/" + gene + "/ref_genome")
    os.system("mkdir -p " + modelspath + "/" + specie + "/" + gene + "/models")


# Write functions
def write_sequences_to_file(sequences: Union[pd.DataFrame, np.ndarray, list, str],
                            fln_sequences: Union[str, Path, TextIO], sep=';'):
    """
    Write sequence to csv file from a dataframe, numpy array, list or single sequence.
    :param sequences: Sequences to write in a csv file.
    :param fln_sequences: CSV filename to output sequences.
    """
    try:
        if type(sequences) == pd.DataFrame:
            sequences.to_csv(fln_sequences, sep=sep)

        elif type(sequences) == np.ndarray:
            # np.savetxt(fln_sequences, sequences, delimiter=sep, fmt="%s")
            np_output = np.dstack((np.arange(0, sequences.size), sequences))[0]
            np.savetxt(fln_sequences, np_output, "%d"+sep+"%s",
                       header="seq_index"+sep+"sequence")

        elif type(sequences) == list:  # or type(sequences)==type(Generator[str]):
            if isinstance(fln_sequences, (str, bytes, Path)):
                # open a file handler with "with"
                with open(fln_sequences, 'w') as ofile:
                    for ii, sequence in enumerate(sequences):
                        ofile.write("{:d}"+sep+"{}\n".format(ii, sequence))
            else:
                ofile = fln_sequences
                for ii, sequence in enumerate(sequences):
                    ofile.write("{:d}" + sep + "{}\n".format(ii, sequence))
        elif type(sequences) == str:
            # Use regex to generate sequences with that form
            sequence = sequences
            if isinstance(fln_sequences, (str, bytes, Path)):
                # open a file handler with "with"
                with open(fln_sequences, 'w') as ofile:
                    ofile.write("seq_index"+sep+"sequence"+"\n")
                    ofile.write("0"+sep+sequence+"\n")
            else:
                ofile = fln_sequences
                ofile.write("seq_index" + sep + "sequence" + "\n")
                ofile.write("0" + sep + sequence + "\n")


        else:
            print("Format not supported")

        return fln_sequences
    except Exception as e:
        raise e

def write_ref_genome_files_from_dataframe(df_Gene_ref_genome, fln_fasta, fln_anchor=None):
    try:
        write_genetemplate_dataframe_to_fasta(fln_fasta, df_Gene_ref_genome)
        try:
            if fln_anchor is not None:
                # write anchors if any
                write_geneanchors_dataframe_to_csv(fln_anchor, df_Gene_ref_genome)
        except Exception as e:
            print("ERROR: No anchors found in: ", df_Gene_ref_genome)
            raise e
    except Exception as e:
        raise e

def write_genetemplate_dataframe_to_fasta(fln_fasta:Union[str, Path, TextIO], df_genomic):
    """Write dataframe to fasta file
    :param fln_fasta: Fasta output filename.
    :param df_genomic: Pandas dataframe with columns 'name' for description and 'value' for sequence.
    """
    try:
        if df_genomic is not None:
            with open(fln_fasta, "w") as ofile:
                for idx, row in df_genomic.iterrows():
                    fasta_one_sequence = ">" + str(row['name']) + "\n" + str(row['value']) + "\n"
                    ofile.write(fasta_one_sequence)
    except Exception as e:
        print("fln_fasta: ", fln_fasta)
        print("df_genomic: ", df_genomic)
        raise e

def write_geneanchors_dataframe_to_csv(fln_anchor:Union[str, Path, TextIO], df_ref_genome, sep = ';'):
    """
    Write gene anchors in csv file from a ref_genome dataframe
    :param fln_anchor: csv output filename.
    :param df_genomic: Pandas dataframe with columns 'name' for description and 'value' for sequence.
    """
    try:
        not_na = ~df_ref_genome['anchor_index'].isna()
        df_anchors = df_ref_genome[not_na].copy()
        try:
            df_anchors.rename(columns={'name':'gene'}, inplace=True)
        except:
            pass
        df_tmp = df_anchors['anchor_index'].apply(lambda x: int(x))
        df_anchors['anchor_index'] = df_tmp.copy()
        anchors_cols = ['gene', 'anchor_index']
        try:
            if 'function' in df_anchors.columns:
                df_anchors['function'].fillna("", inplace=True)
                df_anchors.to_csv(fln_anchor, sep=sep, index=False, columns=anchors_cols + ['function'])
            elif 'gfunction' in df_anchors.columns:
                df_anchors['gfunction'].fillna("", inplace=True)
                df_anchors.to_csv(fln_anchor, sep=sep, index=False, columns=anchors_cols + ['gfunction'])
            else:
                df_anchors.to_csv(fln_anchor, sep=sep, index=False, columns=anchors_cols)
        except Exception as e:
            print("Not function in anchors file!")
            raise e
    except Exception as e:
        raise e

def get_dataframe_from_fln_generated_seqs_werr(igor_fln_generated_seqs_werr):
    df_seqs = pd.read_csv(igor_fln_generated_seqs_werr, delimiter=';').set_index('seq_index')
    return df_seqs
# Get Dataframes functions
def get_dataframe_from_fasta(fln_fasta):
    """Return dataframe from fasta file
    :param fln_fasta: Fasta filename.
    """
    from Bio import SeqIO
    import pandas as pd
    genes_name_list = list()
    genes_value_list = list()
    for gene_record in SeqIO.parse(fln_fasta, "fasta"):
        genes_name_list.append(gene_record.description)
        genes_value_list.append(str(gene_record.seq))
    df_genes = pd.DataFrame.from_dict({'name': genes_name_list, 'value': genes_value_list})
    df_genes.index.name = 'id'
    return df_genes

def get_anchors_dataframe_from_csv(fln_csv, sep=';'):
    try:
        # FIXME: gene could it be gene_name or simple name?
        df_anchors = pd.read_csv(fln_csv, sep=sep, index_col='gene')
        df_anchors['anchor_index']
        return df_anchors
    except Exception as e:
        raise e

def get_ref_genome_dataframe_from(df_genomic:pd.DataFrame, df_anchors:pd.DataFrame=None, sep=';'):
    df_genomic_copy = df_genomic.copy()
    df_anchors_copy = df_anchors.copy()
    if df_anchors_copy is not None:
        try:
            # 1. save values of index
            df_genomic_copy['id'] = df_genomic_copy.index.get_level_values('id')
            # 2. Change index to gene name
            if not df_genomic_copy.index.name == 'name':
                df_genomic_copy.set_index('name', inplace=True)
                df_genomic_copy['name'] = df_genomic_copy.index.get_level_values('name')
            # 3. Change index
            if not df_anchors_copy.index.name == 'gene':
                df_anchors_copy.set_index('gene', inplace=True)
            # 4. Join dataframes by gene name
            df_ref_genome = df_genomic_copy.join(df_anchors_copy)
            # 5. Finally recover the original indexes
            df_ref_genome.set_index('id', inplace=True)
            get_df_order_cols_ref_genome(df_ref_genome)
        except Exception as e:
            raise e
    else:
        df_ref_genome = df_genomic#.copy()
    return df_ref_genome

def get_dataframe_from_fasta_and_csv_anchors(fln_fasta, fln_anchor_csv=None, sep=';'):
    import pandas as pd
    df_genomic = get_dataframe_from_fasta(fln_fasta)
    if fln_anchor_csv is not None:
        df_anchors = pd.read_csv(fln_anchor_csv, sep=sep)
        df_ref_genome = get_ref_genome_dataframe_from(df_genomic, df_anchors)
    else:
        df_ref_genome = df_genomic
    return df_ref_genome


def get_join_genomics_anchors_dataframes(df_genes_templates, df_genes_anchors):
    df_genetemplates = df_genes_templates.copy()
    df_genetemplates['id'] = df_genetemplates.index.get_level_values('id')
    df_genetemplates.set_index('name', inplace=True) # gene name for GeneChoice events
    df_geneanchors = df_genes_anchors.copy() #.set_index('gene').copy()

    df_all = df_genetemplates.join(df_geneanchors)

    df_all['name'] = df_all.index.get_level_values('name')
    df_all.set_index('id', inplace=True)

    columnas = df_all.columns.to_list()
    ini_cols = ['name', 'value', 'anchor_index']
    other_cols = list()
    for col in columnas:
        if not col in ini_cols:
            other_cols.append(col)
    new_order = ini_cols + other_cols
    df_all = df_all[new_order]

    return df_all.copy()

def get_df_order_cols_ref_genome(df_all:pd.DataFrame):
    columnas = df_all.columns.to_list()
    if 'anchor_index' in columnas:
        ini_cols = ['name', 'value', 'anchor_index']
    else:
        ini_cols = ['name', 'value']
    other_cols = list()
    for col in columnas:
        if not col in ini_cols:
            other_cols.append(col)
    new_order = ini_cols + other_cols
    return df_all[new_order].copy()


def get_dataframe_with_ref_genome_column_names(df_ref_genome:pd.DataFrame):
    df = df_ref_genome.copy()
    old_index = df.index.name
    df = df.rename(index={old_index: 'id'})
    gene_name_cols = ['gene_name', 'gene']
    for str_name in gene_name_cols:
        if str_name in df.columns:
            df = df.rename(columns={str_name: 'name'})
            break
    gene_name_cols = ['sequence']
    for str_name in gene_name_cols:
        if str_name in df.columns:
            df = df.rename(columns={str_name: 'value'})
            break

    return df
    # change it to


def get_df_anchors_from_df_ref_genome(df_ref_genome):
    sequences_cols = ['value']
    # remove sequence value
    df_tmp_ref_genome = df_ref_genome.copy()
    try:
        df_tmp_ref_genome = df_tmp_ref_genome.drop(columns=sequences_cols)
    except KeyError as e:
        print(e)
        pass
    except Exception as e:
        raise e
    # set change colname of name to gene and set it as index
    try:
        df_tmp_ref_genome = df_tmp_ref_genome.set_index('name')
        df_tmp_ref_genome.index.name = 'gene'
    except KeyError as e:
        print(e)
        pass
    except Exception as e:
        raise e

    return df_tmp_ref_genome.copy()

# // A, C, G, T, R, Y, K, M, S, W, B, D, H, V, N
heavy_pen_nuc44_vect = [
5, -14, -14, -14, -14, 2, -14, 2, 2, -14, -14, 1, 1, 1, 0,
-14, 5, -14, -14, -14, 2, 2, -14, -14, 2, 1, -14, 1, 1, 0,
-14, -14, 5, -14, 2, -14, 2, -14, 2, -14, 1, 1, -14, 1, 0,
-14, -14, -14, 5, 2, -14, -14, 2, -14, 2, 1, 1, 1, -14, 0,
-14, -14, 2, 2, 1.5, -14, -12, -12, -12, -12, 1, 1, -13, -13, 0,
2, 2, -14, -14, -14, 1.5, -12, -12, -12, -12, -13, -13, 1, 1, 0,
-14, 2, 2, -14, -12, -12, 1.5, -14, -12, -12, 1, -13, -13, 1, 0,
2, -14, -14, 2, -12, -12, -14, 1.5, -12, -12, -13, 1, 1, -13, 0,
2, -14, 2, -14, -12, -12, -12, -12, 1.5, -14, -13, 1, -13, 1, 0,
-14, 2, -14, 2, -12, -12, -12, -12, -14, 1.5, 1, -13, 1, -13, 0,
-14, 1, 1, 1, 1, -13, 1, -13, -13, 1, 0.5, -12, -12, -12, 0,
1, -14, 1, 1, 1, -13, -13, 1, 1, -13, -12, 0.5, -12, -12, 0,
1, 1, -14, 1, -13, 1, -13, 1, -13, 1, -12, -12, 0.5, -12, 0,
1, 1, 1, -14, -13, 1, 1, -13, 1, -13, -12, -12, -12, 0.5, 0,
0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]

list_nt_lbl = ['A', 'C', 'G', 'T', 'R', 'Y', 'K', 'M', 'S', 'W', 'B', 'D', 'H', 'V', 'N']
da_heavy_pen_nuc44_vect = xr.DataArray(np.array(heavy_pen_nuc44_vect).reshape(15, 15), \
                               dims=('x', 'y'))
# print(len(list_nt_lbl))
strDim = 'x'
da_heavy_pen_nuc44_vect[strDim] = range(len(list_nt_lbl))
strCoord = 'lbl__' + strDim
da_heavy_pen_nuc44_vect[strCoord] = (strDim, list_nt_lbl)

strDim = 'y'
da_heavy_pen_nuc44_vect[strDim] = range(len(list_nt_lbl))
strCoord = 'lbl__' + strDim
da_heavy_pen_nuc44_vect[strCoord] = (strDim, list_nt_lbl)



#####################################################
########## PLOTTING SEQUENCES  #################
#####################################################
# Functions copied from :
# Reference: https://dmnfarrell.github.io/bioinformatics/bokeh-sequence-aligner

# FIXME: PLEASE MAKE IT MORE MATPLOTLIB-ISH
try:
    from Bio import AlignIO, SeqIO
    import numpy as np
    from bokeh.plotting import figure, output_file, save, show
    from bokeh.models import ColumnDataSource, Plot, Grid, Range1d
    from bokeh.models.glyphs import Text, Rect
    from bokeh.layouts import gridplot

    def get_colors(seqs):
        """make colors for bases in sequence"""
        text = [i for s in list(seqs) for i in s]
        clrs = {'A': 'red', 'T': 'green', 'G': 'orange', 'C': 'blue', '-': 'white',
                'a': 'red', 't': 'green', 'g': 'orange', 'c': 'blue'}
        colors = [clrs[i] for i in text]
        return colors


    def view_alignment(aln, fontsize="9pt", plot_width=800):
        """Bokeh sequence alignment view"""
        # make sequence and id lists from the aln object
        seqs = [rec.seq for rec in (aln)]
        ids = [rec.id for rec in aln]
        text = [i for s in list(seqs) for i in s]

        colors = get_colors(seqs)
        N = len(seqs[0])
        S = len(seqs)
        width = .4
        x = np.arange(1, N + 1)
        y = np.arange(0, S, 1)
        # creates a 2D grid of coords from the 1D arrays
        xx, yy = np.meshgrid(x, y)
        # flattens the arrays
        gx = xx.ravel()
        gy = yy.flatten()
        # use recty for rect coords with an offset
        recty = gy + .5
        h = 1 / S
        # now we can create the ColumnDataSource with all the arrays
        source = ColumnDataSource(dict(x=gx, y=gy, recty=recty, text=text, colors=colors))
        plot_height = len(seqs) * 15 + 50
        x_range = Range1d(0, N + 1, bounds='auto')
        if N > 100:
            viewlen = 100
        else:
            viewlen = N
        # view_range is for the close up view
        view_range = (0, viewlen)
        tools = "xpan, xwheel_zoom, reset, save"

        # entire sequence view (no text, with zoom)
        p = figure(title=None, plot_width=plot_width, plot_height=50,
                   x_range=x_range, y_range=(0, S), tools=tools,
                   min_border=0, toolbar_location='below')
        rects = Rect(x="x", y="recty", width=1, height=1, fill_color="colors",
                     line_color=None, fill_alpha=0.6)
        p.add_glyph(source, rects)
        p.yaxis.visible = False
        p.grid.visible = False

        # sequence text view with ability to scroll along x axis
        p1 = figure(title=None, plot_width=plot_width, plot_height=plot_height,
                    x_range=view_range, y_range=ids, tools="xpan,reset",
                    min_border=0, toolbar_location='below')  # , lod_factor=1)
        glyph = Text(x="x", y="y", text="text", text_align='center', text_color="black",
                     text_font="monospace", text_font_size=fontsize)
        rects = Rect(x="x", y="recty", width=1, height=1, fill_color="colors",
                     line_color=None, fill_alpha=0.4)
        p1.add_glyph(source, glyph)
        p1.add_glyph(source, rects)

        p1.grid.visible = False
        p1.xaxis.major_label_text_font_style = "bold"
        p1.yaxis.minor_tick_line_width = 0
        p1.yaxis.major_tick_line_width = 0

        p = gridplot([[p], [p1]], toolbar_location='below')
        show(p)
        return p


except ImportError as error:
    # Output expected ImportErrors.
    # print(error.__class__.__name__ + ": " + error.message)
    # FIXME: no error printing for autocomplete
    # print(error)
    pass
except Exception as exception:
    # Output unexpected Exceptions.
    print(exception, False)
    print(exception.__class__.__name__ + ": " + exception.message)




class GeneSegment:
    def __int__(self, gene_type=None):
        self.gene_type = gene_type
        self.palindrome_5_end = None
        self.gene_ini = None
        self.gene_end = None
        self.gene_cut = None
        self.palindrome_3_end = None
        self.gene_segment = None

class InsertSegment:
    def __int__(self, gene_type=None):
        self.gene_type = gene_type
        self.palindrome_5_end = None
        self.gene_ini = None
        self.gene_end = None
        self.gene_cut = None
        self.palindrome_3_end = None
        self.gene_segment = None

def get_gene_segment(str_gene_template, int_gene_5_del=None, int_gene_3_del=None):
    if int_gene_5_del is None:
        int_gene_5_del = 0
    if int_gene_3_del is None:
        int_gene_3_del = 0

    # print(str_gene_template, int_gene_5_del, int_gene_3_del)

    int_ini = 0
    int_end = len(str_gene_template)
    str_gene_3_palindrome = ""
    str_gene_5_palindrome = ""

    if int_gene_5_del < 0:
        int_ini = 0
        str_gene_5_palindrome = dna_complementary( (str_gene_template[:-int_gene_5_del])[::-1] )
    else:
        int_ini = int_gene_5_del
        str_gene_5_palindrome = ""

    if int_gene_3_del < 0:
        int_end = len(str_gene_template)
        str_gene_3_palindrome = dna_complementary( (str_gene_template[int_gene_3_del:])[::-1] )
    else:
        int_end = len(str_gene_template) - int_gene_3_del
        str_gene_3_palindrome = ""

    segment_dict = collections.OrderedDict()
    segment_dict['palindrome_5_end'] = str_gene_5_palindrome
    segment_dict['gene_ini'] = int_ini
    segment_dict['gene_end'] = int_end
    segment_dict['gene_cut'] = str_gene_template[int_ini:int_end]
    segment_dict['palindrome_3_end'] = str_gene_3_palindrome
    segment_dict['gene_segment'] = str_gene_5_palindrome + str_gene_template[int_ini:int_end] + str_gene_3_palindrome
    return segment_dict
    # str_gene_segment = str_gene_5_palindrome + str_gene_template[int_ini:int_end] + str_gene_3_palindrome
    # return str_gene_segment


def dna_complementary(str_seq):
    from Bio.Seq import Seq
    return str(Seq(str_seq).complement())
