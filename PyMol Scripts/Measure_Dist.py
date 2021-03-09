#!/opt/local/bin/python3.8

import sys
import argparse
from pymol import cmd, stored

# parse input
parser = argparse.ArgumentParser(description='A script for measuring the pairwise distances between the alpha'
                                             'carbon atoms of residues in two separate chains in a PDB file.')
parser.add_argument('protein', metavar='structure.pdb',
                    help='Structure to measure distances from in PDB format')
parser.add_argument('out', metavar='output.txt',
                    help='Output of script as a space-separated text file')
parser.add_argument('--chainA', default='A',
                    help='Specify first chain to use for distance measurements [default: A]')
parser.add_argument('--chainB', default='B',
                    help='Specify second chain to use for distance measurements [default: B]')
parser.add_argument('--rangeA', nargs=2, default=['start', 'end'],
                    help='Range of residues in first chain to use for distance measurements [default: (all)]')
parser.add_argument('--rangeB', nargs=2, default=['start', 'end'],
                    help='Range of residues in second chain to use for distance measurements [default: (all)]')
args = parser.parse_args()

# To use script, call this script with two arguments:
#   "structure_name.pdb" (PDB protein structure file with 2+ chains)
#   "output_values.txt" (Text file, output to write distances to, 3 columns)
# Optional arguments: [chain A] [chain B] [range A] [range B]
# You can enter the chains as arguments, or leave blank. If there are more than two chains in your
# PDB file, you will be prompted to select two chains.

# WARNING: script may take a long time to run if you have very large proteins
#   e.g. 1.5hrs for two chains of ~1000 residues

# load protein into PyMol
cmd.load(args.protein)

# open dist.txt for writing
f = open(args.out, 'w')
f.write("chain1 chain2 distance\n")

# define chains to calculate from
chains = cmd.get_chains('all')

A = args.chainA
B = args.chainB

if A not in chains and B not in chains:
    if len(chains) < 2:
        sys.exit("Fewer than 2 chains detected in PDB structure. Check PDB and try again.")
    else:
        print("Specified chains not recognised. Trying manual input.")
        A = input("Select chain 1:")
        B = input("Select chain 2:")
        if A not in chains and B not in chains:
            sys.exit("Specified chains not recognised. Check PDB and try again.")

resA = A + "//CA"
resB = B + "//CA"

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

# get range of residues
stored.resA = []
stored.resB = []

if args.rangeA == ['start', 'end']:
    cmd.iterate(resA, 'stored.resA.append(resi)')
else:
    start = int(args.rangeA[0])
    end = int(args.rangeA[1])
    for i in range(start, end+1):
        stored.resA.append(i)
    stored.range = []
    rangeA = A + "/" + str(start) + "-" + str(end) + "/CA"
    cmd.iterate(rangeA, 'stored.range.append(resi)')
    if len(stored.resA) != len(stored.range):
        sys.exit("Error: Selected range out of bounds, check and try again.")
    else:
        print("Residues selected in chain " + A + ": " + str(start) + "-" + str(end))

if args.rangeB == ['start', 'end']:
    cmd.iterate(resB, 'stored.resA.append(resi)')
else:
    start = int(args.rangeB[0])
    end = int(args.rangeB[1])
    for i in range(start, end+1):
        stored.resB.append(i)
    stored.range = []
    rangeB = B + "/" + str(start) + "-" + str(end) + "/CA"
    cmd.iterate(rangeB, 'stored.range.append(resi)')
    if len(stored.resB) != len(stored.range):
        sys.exit("Error: Selected range out of bounds, check and try again.")
    else:
        print("Residues selected in chain " + B + ": " + str(start) + "-" + str(end))

print("Input validation successful.")

# calculate the distance and store it in dst
for i in stored.resA:
    for j in stored.resB:
        res1 = A + "/" + str(i) + "/CA"
        res2 = B + "/" + str(j) + "/CA"
        dst = (res1, res2, cmd.get_distance(res1, res2))
        f.write("%s %s %8.3f\n" % dst)

# close the output file.
f.close()
