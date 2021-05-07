#!/opt/local/bin/python3.8

import argparse
from pymol import cmd, stored

parser = argparse.ArgumentParser(description='Merge PyMol session files (.pse) to single file.')
parser.add_argument('sess', metavar='sessions_list.txt',
                    help='List of PyMol session files to merge and superimpose (1 per line).'
                         'Try using ls *.pse > sessions_list.txt in the relevant directory.')
parser.add_argument('out', metavar='output.pse', default='output.pse',
                    help='Output of script as a PyMol session file')
args = parser.parse_args()

sessions = open(args.sess, 'r')
stored.sess = []

for line in sessions.readlines():
    stored.sess.append(line.rstrip())

start_sess = stored.sess[0]
cmd.load(start_sess)

for pse_sess in stored.sess[1:len(stored.sess)]:
    cmd.load(pse_sess, partial=1)

objs = cmd.get_object_list()
for obj in objs[1:len(objs)]:
    cmd.super(objs[0], obj)

cmd.orient()
cmd.save(args.out)
