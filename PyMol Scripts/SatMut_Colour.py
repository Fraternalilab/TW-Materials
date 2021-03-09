#!/opt/local/bin/python3.8

import sys
import argparse
from pymol import cmd, stored

# parse input
parser = argparse.ArgumentParser(description='A script for colouring the residues of a PDB structure'
                                             'according to a spectrum of values provided by the user.')
parser.add_argument('protein', metavar='structure.pdb',
                    help='Structure to colour in PDB format')
parser.add_argument('list', metavar='values.txt',
                    help='Text file containing values corresponding to colour values of that residue.'
                         'This file should have the same number of lines as residues in the structure.')
parser.add_argument('out', metavar='output.pse',
                    help='Output of script as a PyMol session file')
parser.add_argument('--chain', default='',
                    help='Specify chain if >1 in the structure file [default: none]')
parser.add_argument('--palette', nargs='*', default='red_yellow_green',
                    help='Specify colours for spectrum palette, from minimum colour to maximum.'
                         'Can use either PyMol palette name or space-separated list of colours.'
                         '[default: red_yellow_green]')
parser.add_argument('--min', default='-3.5',
                    help='Specify minimum value for spectrum range [default: -3.5]')
parser.add_argument('--max', default='3.5',
                    help='Specify maximum value for spectrum range [default: 3.5]')
parser.add_argument('--bg', default='white',
                    help='Specify colour for unselected residues [default: white]')
args = parser.parse_args()

# To use script, call this script with three arguments:
#   "structure_name.pdb" (PDB file with structure coordinates)
#   "colour_values.txt" (Text file, single column, no header, with values to use to colour model)
#   "output_name.pse" (PyMol session file, output written here, viewable in PyMol)
# Optional arguments: [chain] [palette] [min] [max] [bg]

# IMPORTANT: Ensure that your text file contains the same number of values as residues in the chain/protein!

# load the protein
cmd.load(args.protein)

# open the file of new values (just 1 column of numbers, one for each alpha carbon)
inFile = open(args.list, 'r')

# create the global, stored array
stored.newB = []

# read the new B factors from file
for line in inFile.readlines():
    stored.newB.append(float(line))

# close the input file
inFile.close()

# specify chains
chains = cmd.get_chains('all')
if len(chains) == 1:
    chain = chains[0]
else:
    chain = args.chain

# specify key variables
name = "chain " + chain
select = chain + '//CA'
if isinstance(args.palette, type([])):
    palette = ' '.join(args.palette)
else:
    palette = args.palette
minimum = args.min
maximum = args.max

# error catching
print("Validating inputs...")
stored.alt = []
cmd.iterate('not alt ""', 'stored.alt.append(resi)')
if len(stored.alt) > 0:
    print("Alternate atom locations detected.")
    print("Removing alternate locations...")
    cmd.remove('not (alt ''+A)')
else:
    print("No alternate atom locations detected.")
stored.res = []
cmd.iterate(select, 'stored.res.append(resi)')
print("Residues in chain " + str(chain) + ": " + str(len(stored.res)))
print("Values in file " + str(args.list) + ": " + str(len(stored.newB)))
if chain not in chains:
    sys.exit("Error: Chain not found in this structure; check and try again.")
elif len(stored.newB) != len(stored.res):
    sys.exit("Error: Number of residues and/or values not equal; check and try again.")
else:
    print("Input validation successful.")

# clear out the old B Factors
cmd.alter(name, 'b = 0.0')

# update the B Factors with new properties
cmd.alter(select, 'b=stored.newB.pop(0)')

# color the protein based on the new B Factors of the alpha carbons
cmd.color(args.bg, 'all')
cmd.spectrum('b', palette=palette, selection=name, minimum=minimum, maximum=maximum)

# save
cmd.save(args.out)
