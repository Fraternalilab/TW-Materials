#!/opt/local/bin/python3.8

import sys
import argparse
from pymol import cmd

# parse input
parser = argparse.ArgumentParser(description='Colour some residues.')
parser.add_argument('protein', metavar='structure.pdb',
                    help='Structure to colour in PDB format')
parser.add_argument('list', metavar='residues.txt',
                    help='Text file containing residue numbers to colour. Separate the categories with #[title].')
parser.add_argument('out', metavar='output.pse',
                    help='Output of script as a PyMol session file')
parser.add_argument('-n', '--num', type=int, default='3',
                    help='Number of categories in residues.txt [default: 3]')
parser.add_argument('-c', '--coh', nargs='*', default=['yellow', 'magenta', 'cyan'],
                    help='Colours to apply to each residue category, in the order that they appear in residues.txt'
                         ' [default: yellow magenta cyan]')
parser.add_argument('--chain', default='',
                    help='Specify chain if >1 in the structure file [default: none]')
parser.add_argument('--bg', default='white',
                    help='Specify colour for unselected residues [default: white]')
parser.add_argument('--rep', default='none', choices=['dots', 'licorice', 'lines', 'mesh', 'spheres',
                                                      'sticks', 'surface', 'volume', 'wire'],
                    help='Include visualisation of highlighted residues as sticks, spheres etc. [default: none]')
args = parser.parse_args()

# load the protein and residue list
cmd.load(args.protein)

with open(args.list, 'r') as infile:
    res_ids = infile.read().splitlines()

# index the categories in residues.txt
index = [x for x in range(len(res_ids)) if res_ids[x].startswith('#')]

# specify chains
chains = cmd.get_chains('all')
if len(chains) == 1:
    chain = chains[0]
else:
    chain = args.chain

# error catching
print("Validating inputs...")
if len(index) != args.num:
    sys.exit("Error: Number of categories and/or colours not equal; check and try again")
elif len(index) != len(args.coh):
    sys.exit("Error: Number of categories and/or colours not equal; check and try again")
elif chain not in chains:
    sys.exit("Error: Chain not found in this structure; check and try again")
else:
    print("Input validation successful.")

# Go through list and colour appropriately
cmd.color(args.bg, 'all')
for i in range(len(index)):
    start = index[i]+1
    if i < len(index)-1:
        end = index[i+1]
    else:
        end = len(res_ids)
    to_colour = res_ids[start:end]
    for j in range(len(to_colour)):
        select = chain + '/' + to_colour[j] + '/'
        if to_colour[j] != '':
            cmd.color(args.coh[i], select)
            if args.rep != 'none':
                cmd.show(args.rep, select)

# Output as session file
cmd.save(args.out)
