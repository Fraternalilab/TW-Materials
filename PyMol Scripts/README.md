# PyMol-Scripts
 
 A collection of useful PyMol scripts for annotating or retrieving information from biological structures that can be automated through the command line.

## Available Scripts

### `SatMut_Colour.py`
A script for colouring residues according to some external data set (e.g. saturation mutagenesis, predicted pathogenicity, experimental data) on a spectrum.
* Call script through command line with 3 arguments:
    1. "structure_name.pdb" (PDB file with structure coordinates)
    2. "colour_values.txt" (Text file, single column, no header, with values to use to colour model)
            * See: `input_colour-satmut.txt`
    3. "output_name.pse" (PyMol session file, output written here, viewable in PyMol)
* Optional arguments:
    1. [--chain] (specify chain to colour [default: automatic])
    2. [--palette] (specify colours for the spectrum palette, from minimum colour to maximum; can use either PyMol palette name or space-separated list of colours. [default: `red_yellow_green`])
    3. [--min] (specify minimum value for spectrum range [default: `-3.5`])
    4. [--max] (specify maximum value for spectrum range [default: `3.5`])
    5. [--bg] (Specify colour for unselected residues [default: `white`])

* __Important:__ Ensure that your text file contains the same number of values as there are residues in the chain/protein you wish to colour!

### `Measure_Dist.py`
A script for measuring the distance between the alpha carbon atoms of residues in two separate chains in a PDB file.
* Call script through command line with 2 arguments:
    1. "structure_name.pdb" (PDB file with structure coordinates)
    2. "output_values.txt" (Text file, 3 columns, output written here)
* Optional arguments:
    1. [--chain A]
    2. [--chain B] (if more than 2 chains in your PDB, specify here; will prompt if left blank) [default to 'A' and 'B']
    3. [--range A]
    4. [--range B] (specify range of residues for distance measurements; e.g. for residues 1-10 for chain E, give arguments `--chainA E --rangeA 1 10`) [default to all residues]

* __Important:__ By default, this script computes the distances between all possible pairings of residues on different chains. This may take a long time to run on large proteins.

### `Colour_Resi.py`
A script for colouring residues by reading from a formatted text file.
* Call script through command line with 5 arguments:
    1. "structure_name.pdb" (PDB file with structure coordinates)
    2. "colour_residues.txt" (Text file, single column, containing residue numbers/ranges to colour)
        * Separate the categories with #[title]
        * See: `input_colour-resi.txt`
    3. "output_name.pse" (PyMol session file, output written here, viewable in PyMol)
    4. [-n] (number of categories in colour_residues.txt [default: 3])
    5. [-c] (colours to apply to each residue category in colour_residues.txt [default: yellow magenta cyan])
* Optional arguments:
    1. [--chain] (specify chain to colour [default: automatic])
    2. [--bg] (specify colour for unselected residues [default: `white`])
    3. [--rep] (visualise all selected residues as sticks, spheres etc. [default: none])

### `Colour_Resi_Name.py`
A modification of `Colour_Resi.py` that colours a specified list of residues in the system according to their name and chemical properties.
* Call script through command line with 3 arguments:
    1. "structure_name.pdb" (PDB file with structure coordinates)
    2. "residues.txt" (Text file, single column, containing residue numbers/ranges to colour)
        * Separate the categories with #[title]
        * See: `input_colour-name.txt`
    3. "output_name.pse" (PyMol session file, output written here, viewable in PyMol)
* Optional arguments:
    1. [--chain] (specify chain to colour [default: automatic])
    2. [--bg] (specify colour for unselected residues [default: `white`])
    3. [--rep] (visualise all selected residues as sticks, spheres etc. [default: none])

* __Important:__ The colouring for different residues is defined in the script itself; see `20_NATAA_colourscheme.pse` for a visual representation of the different colours. These can be changed at any time by modifying the script (see below).

### `Colour_Resi_Spectra.py`
A modification of `Colour_Resi.py` and `SatMut_Colour.py` that colours residues according to different colour spectra by reading from a formatted text file.
* Call script through command line with 5 arguments:
    1. "structure_name.pdb" (PDB file with structure coordinates)
    2. "colour_residues.txt" (Text file, two columns, space-separated)
        * Field 1 contains residue numbers/ranges to colour
        * Field 2 contains numerical value associated with that position used to colour according to respective spectrum; separate the categories with #[title])
        * Separate the categories with #[title]
        * See: `input_colour-spectra.txt`
    3. "output_name.pse" (PyMol session file, output written here, viewable in PyMol)
    4. [-n] (number of categories in colour_residues.txt [default: 3])
    5. [-s] (spectra to apply to each residue category in colour_residues.txt [default: red_green, yellow_blue, cyan_magenta])
* Optional arguments:
    1. [--chain] (specify chain to colour [default: automatic])
    2. [--bg] (specify colour for unselected residues [default: `white`])
    3. [--rep] (visualise all selected residues as sticks, spheres etc. [default: none])
    4. [--na] (set colour for NA/missing values, if present in the data)
    5. [--custom_range] (if range of values differs between spectra, set this flag to input minimum and maximum values for each category's range directly [default: min 0, max 1])
    
### `Merge_Sessions.py`
A script for merging large numbers of separate PyMol sessions into a single file and superimposing homologous regions atop one another.
* Call script through command line with 2 arguments:
    1. "input_sessions_list.txt" (Text file, single column, containing file names of PyMol session files [*.pse] to merge and align.
        * See: `input_merge_sessions.txt`
    2. "output_session.pse" (PyMol session file, output written here, viewable in PyMol)

## Requirements

You will need a working version of Python 3 with command line access and an associated version of PyMol. We recommend downloading the latest version of [Open Source Anaconda](https://www.anaconda.com/) and using `conda install` to get the open-source version of PyMol.

In order to use these scripts through the command line, you will need to have a build of PyMol that includes the extensions that enable the import of PyMol commands into Python. This should come as standard when downloaded through Conda/MacPorts/etc, but may be absent in some evaluation versions.

## Usage

To use, run script on the command line with the appropriate arguments (see above):

    `python /path/to/pymol_script [arguments]`

You may find it necessary to alter access permissions for the script to execute it.

If for whatever reason you cannot use Python through the command line, you can instead try pasting and running the individual lines of code in PyMol's command line, with the variables set to the files you wish to input rather than system arguments. However, this may run into problems and is not recommended.

## Run Examples

Navigate to the `examples` folder and run the following commands:

    `python ../SatMut_Colour.py example_structure.pdb input_colour-satmut.txt output_colour-satmut.pse --chain O --palette rainbow --min -5 --max 5 --bg white`
    
    `python ../Measure_Dist.py example_structure.pdb output_measure-dist.txt --chainA O --chainB T --rangeA 86 100 --rangeB 16 31`
    
    `python ../Colour_Resi.py example_structure.pdb input_colour-resi.txt output_colour-resi.pse -n 3 -c red blue green --chain O --rep licorice --bg white`
    
    `python ../Colour_Resi_Name.py example_structure2.pdb input_colour-name.txt output_colour-name.pse --rep licorice`
    
    `python ../Colour_Resi_Spectra.py example_structure2.pdb input_colour-spectra.txt output_colour-spectra.pse -n 3 --rep licorice --bg white`
    
    `python ../Merge_Sessions.py input_merge_sessions.txt output_merge_sessions.pse`

## Script Modifications

Certain elements of the script may be modified to suit user preferences.

* If running scripts directly through PyMol's command line, you can alter system arguments to direct filenames to achieve the same outcome, e.g. `cmd.load(args.protein)` to `cmd.load(/path/to/structure.pdb)`
* If you have multiple versions of python and wish to specify a version, you can add the full path to the first line of the script (e.g. `#!/usr/bin/python`) and then run on the command line as a standalone (e.g. `./pymol_script.py [arguments]`)
* If you want to use a subset of atoms within a chain or chains for calculation or annotation, you can alter the selection macros of the script where the residues are selected. 
    *  Define selections explicitly. For example, `A//CA` selects all of the alpha carbon atoms in chain A, and `B/1-10/` selects all atoms in residues between residue 1 and 10 (inclusive) in chain B.
        * Explicit selections may be necessary for correct function if your PDB file has more than 1 object in it.
    * Refer to the [selection macro syntax](https://pymolwiki.org/index.php/Selection_Macros) help page for more information.
* For residue recolouring scripts, you may wish to change the spectrum of colours that PyMol uses. The default is `red_yellow_green`; PyMol has a selection of colour palettes available, or you can specify the individual colours as space-separated arguments (e.g. `--palette red yellow green`)
    * Refer to the [Spectrum](https://pymolwiki.org/index.php/Spectrum) function help page for more information.
* The residue colouring for `Colour_Resi_Name.py` is defined by a dictionary that maps the three-letter code for a particular residue to a corresponding colour.
    * Aliphatic hydrocarbon residues are coloured in shades of green
    * Large aromatic residues are coloured in shades of orange
    * Basic charged residues are coloured in shades of blue
    * Acidic charged residues are coloured in shades of red
    * Polar residues are coloured in shades of magenta
    * Glycine is grey, cysteine is cyan, proline is purple and methionine is yellow
    * These can be readily changed if desired; consult the available colours for your PyMol version.
