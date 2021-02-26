# PyMol-Scripts
 
 A collection of useful PyMol scripts for annotating or retrieving information from biological structures that can be automated through the command line.

## Available Scripts

`SatMut_Colour.py` - A script for colouring residues according to some external data set (e.g. saturation mutagenesis, predicted pathogenicity, experimental data) on a spectrum.
* Call script through command line with 3 arguments:
    1. "structure_name.pdb" (PDB file with structure coordinates)
    2. "colour_values.txt" (Text file, single column, no header, with values to use to colour model)
    3. "output_name.pse" (PyMol session file, output written here, viewable in PyMol)
* Optional arguments: [chain] (specify chain to colour e.g. "A")
* __Important:__ Ensure that your text file contains the same number of values as there are residues in the chain/protein you wish to colour!

`Measure_Dist.py` - A script for measuring the distance between the alpha carbon atoms of residues in two separate chains in a PDB file.
* Call script through command line with 3 arguments:
    1. "structure_name.pdb" (PDB file with structure coordinates)
    2. "output_values.txt" (Text file, 3 columns, output written here)
* Optional arguments: [chain A] [chain B] (if more than 2 chains in your PDB, specify here)
* __Important:__ This script computes the distances between all possible pairings of residues on different chains. May take a long time to run on large proteins.

## Requirements

You will need a working version of Python 3 with command line access and an associated version of PyMol. We recommend downloading the latest version of [Open Source Anaconda](https://www.anaconda.com/) and using `conda install` to get the open-source version of PyMol.

In order to use these scripts through the command line, you will need to have a build of PyMol that includes the extensions that enable the import of PyMol commands into Python. This should come as standard when downloaded through Conda/MacPorts/etc, but may be absent in some evaluation versions.

## Usage

To use, run script on the command line with the appropriate arguments (see above):

    `python /path/to/pymol_script [arguments]`

You may find it necessary to alter access permissions for this file to execute.

If for whatever reason you cannot use Python through the command line, you can instead try pasting and running the individual lines of code in PyMol's command line, with the variables set to the files you wish to input rather than system arguments. However, this may run into problems and is not recommended.

## Script Modifications

Certain elements of the script may be modified to suit user preferences.

* If running scripts directly through PyMol's command line, you can alter system arguments to direct filenames to achieve the same outcome, e.g. `cmd.load(sys.argv[1])` to `cmd.load(/path/to/structure.pdb)`
* If you have multiple versions of python and wish to specify a version, you can add the full path to the first line of the script (e.g. `#!/usr/bin/python`) and then run on the command line as a standalone (e.g. `./pymol_script [arguments]`)
* If you want to use a subset of atoms within a chain or chains for calculation or annotation, you can alter the selection macros of the script where the residues are selected. 
    *  Define selections explicitly. For example, `A//CA` selects all of the alpha carbon atoms in chain A, and `B/1-10/` selects all atoms in residues between residue 1 and 10 (inclusive) in chain B.
    * Explicit selections may be necessary for correct function if your PDB file has more than 1 object in it.
    * Refer to [selection macro syntax](https://pymolwiki.org/index.php/Selection_Macros) for more information.
* For residue recolouring scripts, you may wish to change the spectrum of colours that PyMol uses. The default is `red_yellow_green`; this may be changed to any combination of colours that PyMol permits.
