import sys
from pymol import cmd, stored

if len(sys.argv) == 4:
    chain = False
elif len(sys.argv) == 5:
    chain = True
else:
    sys.exit("Usage: SatMut_Colour.py structure_name.pdb colour_values.txt output_name.pse [chain]")

# To use script, call this script with three arguments:
#   "structure_name.pdb" (PDB file with structure coordinates)
#   "colour_values.txt" (Text file, single column, no header, with values to use to colour model)
#   "output_name.pse" (PyMol session file, output written here, viewable in PyMol)
# Optional arguments: [chain]

# IMPORTANT: Ensure that your text file contains the same number of values as residues in the chain/protein!

protein = sys.argv[1]
values = sys.argv[2]
output = sys.argv[3]

if chain:
    name = "chain " + sys.argv[4]
    select = sys.argv[4] + '//CA'
else:
    name = "all"
    select = 'n. CA'

# load the protein
cmd.load(protein)

# open the file of new values (just 1 column of numbers, one for each alpha carbon)
inFile = open(values, 'r')

# create the global, stored array
stored.newB = []

# read the new B factors from file
for line in inFile.readlines():
    stored.newB.append(float(line))

# close the input file
inFile.close()

# check residue count

stored.res = []
cmd.iterate(select, 'stored.res.append(resi)')
if len(stored.newB) != len(stored.res):
    sys.exit("Length of selection and length of text file are not equal. Check and try again.")

# clear out the old B Factors
cmd.alter(name, 'b = 0.0')

# update the B Factors with new properties

cmd.alter(select, 'b=stored.newB.pop(0)')

# color the protein based on the new B Factors of the alpha carbons
cmd.spectrum('b', 'red_yellow_green', selection=name, minimum=-4.5, maximum=4.5)

# save

cmd.save(output)
