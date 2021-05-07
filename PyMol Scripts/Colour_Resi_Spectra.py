#!/opt/local/bin/python3.8

import sys
import argparse
from pymol import cmd, stored

# parse input
parser = argparse.ArgumentParser(description='Colour some residues according to user-defined categories and with'
                                             'colour spectra based on associated data.')
parser.add_argument('protein', metavar='structure.pdb',
                    help='Structure to colour in PDB format')
parser.add_argument('list', metavar='residues.txt',
                    help='Text file containing residue numbers to colour. Separate the categories with #[title].'
                         'Each category list should have two columns, space-separated; e.g. "[residue] [value]"')
parser.add_argument('out', metavar='output.pse',
                    help='Output of script as a PyMol session file')
parser.add_argument('-n', '--num', type=int, default='3',
                    help='Number of categories in residues.txt [default: 3]')
parser.add_argument('-s', '--spectra', nargs='*', default=['red_green', 'yellow_blue', 'cyan_magenta'],
                    help='Spectra to apply to each residue category, in the order that they appear in residues.txt'
                         ' [default: red_green yellow_blue cyan_magenta]')
parser.add_argument('--chain', default='',
                    help='Specify chain if >1 in the structure file [default: none]')
parser.add_argument('--bg', default='white',
                    help='Specify colour for unselected residues [default: white]')
parser.add_argument('--rep', default='none', choices=['dots', 'licorice', 'lines', 'mesh', 'spheres',
                                                      'sticks', 'surface', 'volume', 'wire'],
                    help='Include visualisation of highlighted residues as sticks, spheres etc. [default: none]')
parser.add_argument('--custom_range', action='store_true',
                    help='Call to input range for spectrum colours manually [default: min 0.0, max 1.0]')
parser.add_argument('--na', default='gray40',
                    help='Default colour for NA/missing values [default: dark grey]')
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
elif len(index) != len(args.spectra):
    sys.exit("Error: Number of categories and/or colours not equal; check and try again")
elif chain not in chains:
    sys.exit("Error: Chain not found in this structure; check and try again")
else:
    print("Input validation successful.")

# Go through list and find categories
cmd.color(args.bg, 'all')
for i in range(len(index)):
    start = index[i]+1
    if i < len(index)-1:
        end = index[i+1]
    else:
        end = len(res_ids)
    to_colour = res_ids[start:end]

    # specify spectrum range
    if args.custom_range:
        print("Input numerical ranges for spectrum "+str(i+1)+".")
        minimum = input("Minimum:")
        maximum = input("Maximum:")
    else:
        minimum = 0
        maximum = 1

    # Colour every residue in that category
    for j in range(len(to_colour)):
        if to_colour[j] != '':
            select = chain + '/' + to_colour[j].split()[0] + '/'
            stored.value = to_colour[j].split()[1]
            if stored.value == 'NA':
                cmd.color(args.na, select)
            else:
                cmd.alter(select, 'b = stored.value')
                cmd.spectrum('b', palette=args.spectra[i], selection=select, minimum=minimum, maximum=maximum)
            if args.rep != 'none':
                cmd.show(args.rep, select)

# Output as session file
cmd.save(args.out)
