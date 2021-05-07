#!/opt/local/bin/python3.8

# COLOUR BY RESIDUE - PATRICK BRENNAN, UNIVERSITY OF OXFORD - AUGUST 2020
# Modified by TW

import sys
import argparse
from pymol import cmd, stored

# parse input
parser = argparse.ArgumentParser(description='Colour some residues automatically by residue type.')
parser.add_argument('protein', metavar='structure.pdb',
                    help='Structure to colour in PDB format')
parser.add_argument('list', metavar='residues.txt',
                    help='Text file containing residue numbers to colour.')
parser.add_argument('out', metavar='output.pse',
                    help='Output of script as a PyMol session file')
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

# specify chains
chains = cmd.get_chains('all')
if len(chains) == 1:
    chain = chains[0]
else:
    chain = args.chain

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
if chain not in chains:
    sys.exit("Error: Chain not found in this structure; check and try again.")
else:
    print("Input validation successful.")

# get residue names
unique_res = list(dict.fromkeys(res_ids))
stored.residues = []
if chain is '':
    res_select = ','.join(map(str, unique_res)) + "/CA"
else:
    res_select = chain + "/" + ','.join(map(str, unique_res)) + "/CA"


cmd.iterate(res_select, 'stored.residues.append(resn)')

# define dictionary

code = {'ALA': 'limegreen', 'VAL': 'palegreen', 'ILE': 'forest', 'LEU': 'smudge',
        'PHE': 'orange', 'TRP': 'lightorange', 'TYR': 'olive',
        'SER': 'magenta', 'THR': 'pink', 'ASN': 'purple', 'GLN': 'violet',
        'ARG': 'marine', 'HIS': 'slate', 'LYS': 'lightblue',
        'ASP': 'tv_red', 'GLU': 'ruby',
        'MET': 'yellow',
        'CYS': 'cyan',
        'PRO': 'purpleblue',
        'GLY': 'gray20'
        }

# colour residues by identity

cmd.color(args.bg, 'all')
for i in range(len(unique_res)):
    select = chain + '/' + unique_res[i] + '/'
    res_name = stored.residues[i]
    colour = code[res_name]
    cmd.color(colour, select)
    if args.rep != 'none':
        cmd.show(args.rep, select)

cmd.save(args.out)
