#!/usr/bin/env python3

import argparse
from random import choices

parser = argparse.ArgumentParser(description='Generate a random nucleotide or protein sequence.')
parser.add_argument('length', type=int, help="The desired length of DNA/RNA/Protein sequence. Start or end sequences detract from this total length, so total length is always equal to this number.")
parser.add_argument('-t', '--type', default='DNA', type=str, help='Desired sequence type. RNA, DNA, or Protein')
parser.add_argument('-g', '--content', default=50, type=int, help='GC percentage for generated sequence, does not account for start or end sequences.')
parser.add_argument('-s', '--start', default='', type=str, help='Desired prefix for randomized sequence.')
parser.add_argument('-e', '--end', default='', type=str, help='Desired suffix for randomize sequence.')

args = parser.parse_args()

length = args.length
seqType = args.type
gc = args.content
start = args.start
end = args.end

seq = ""
dnaRNA = "ATGC"
# Change to Uracil if RNA is desired.
if seqType == "RNA":
    dnaRNA = "AUGC"
# sequence generation, follows GC% provided, and appends start and end sequences if adaptors are desired.
if seqType == "DNA" or seqType == "RNA":
    for _ in range(max(0, length-len(start)-len(end))):
        seq += ''.join(choices("ATGC", weights=[(100-gc)/2, (100-gc)/2, gc/2, gc/2], k = 1))
    
elif seqType == "Protein":
    for _ in range(max(0,length-len(start)-len(end))):
        seq += ''.join(choices("ARNDCQEGHILKMFPSTWYV", k=1))

print(start + seq + end)