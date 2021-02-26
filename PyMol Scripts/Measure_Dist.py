import sys
from pymol import cmd, stored

if len(sys.argv) == 3:
    chain = False
elif len(sys.argv) == 5:
    chain = True
else:
    sys.exit("Usage: Measure_Dist.py structure_name.pdb output_values.txt [chain A] [chain B]")

# To use script, call this script with two arguments:
#   "structure_name.pdb" (PDB protein structure file with 2+ chains)
#   "output_values.txt" (Text file, output to write distances to, 3 columns)
# Optional arguments: [chain A] [chain B]
# You can enter the chains as arguments, or leave blank. If there are more than two chains in your
# PDB file, you will be prompted to select two chains.

# WARNING: script may take a long time to run if you have very large proteins
#   e.g. 1.5hrs for two chains of ~1000 residues

name = sys.argv[1]
out = sys.argv[2]

# load protein into PyMol
cmd.load(name)

# open dist.txt for writing
f = open(out, 'w')

# define chains to calculate from
chains = cmd.get_chains('all')

if len(chains) == 2:
    A = chains[0]
    B = chains[1]
else:
    if chain:
        print("More than 2 chains detected.")
        A = sys.argv[3]
        B = sys.argv[4]
    elif len(chains) > 2:
        print("More than 2 chains detected.")
        A = input("Select chain 1:")
        B = input("Select chain 2:")
    else:
        sys.exit("Fewer than 2 chains detected in PDB structure. Check and try again.")

resA = A + "//CA"
resB = B + "//CA"

# get range of residues
stored.resA = []
stored.resB = []

cmd.iterate(resA, 'stored.resA.append(resi)')
cmd.iterate(resB, 'stored.resB.append(resi)')

# calculate the distance and store it in dst
for i in stored.resA:
    for j in stored.resB:
        res1 = str(A) + "/" + str(i) + "/CA"
        res2 = str(B) + "/" + str(j) + "/CA"
        dst = (res1, res2, cmd.get_distance(res1, res2))
        f.write("%s %s %8.3f\n" % dst)

# close the output file.
f.close()
