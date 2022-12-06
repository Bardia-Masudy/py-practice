#!/usr/bin/env python3
# Simple commandline utilitile for generating reverse complement of a standard DNA sequence, taking into account ambiguous bases.

import re
import argparse

#def revComp(seq = '', vis = False):

parser = argparse.ArgumentParser(description="Simple commandline utilitile for generating reverse complement of a standard DNA sequence, taking into account ambiguous bases.")

parser.add_argument('seq', help="The DNA sequence meant to be reverse complemented.")
parser.add_argument('-v', '--vis', default=False, help="Whether or not to visualize the forward and reverse sequences.")

args = parser.parse_args()

seq = str(args.seq)
vis = args.vis

if not re.findall(r"[^ATCGNSWKMRYBVDH\s]+", seq):
    #try:
    dict = {"A":"T", "T":"A", "C":"G", "G":"C", "N":"N", "S":"S", "W":"W", "K":"M", "M":"K", "R":"Y", "Y":"R", "B":"V", "V":"B", "D":"H", "H":"D"} # dictionary for base complements
        
    revC = '' 
    seq = seq.upper()
    # Contruct reverse complement
    for i in range(len(seq)):
        revC = dict[seq[i]] + revC
        
    # Optionally visualize forward and reverse strand.
    if vis:
        print(f"5'-{seq.upper()}-3'")
        print(" " * 3 + "|"*len(seq))
        print(f"3'-{revC}-5'")
    else:
        print(revC)
else:
    print("Please enter in a valid sequence containing only GATC and ambiguous bases")