
import argparse

parser = argparse.ArgumentParser(description="Utility to generate a indexed list of k-mers for the forward and optionally the reverse strand of a sequence.")

parser.add_argument('text')
parser.add_argument('k')
parser.add_argument('-r', '--reverse', action='store_true', help="Optional switch to also produce the reverse strand k-mers.")

args = parser.parse_args()

text = str(args.text)
k = int(args.k)
rev = args.reverse

fwdIndex = {}
revIndex = {}
complements = {"A":"T", "T":"A", "C":"G", "G":"C", "N":"N"} # dict for assignment of complement bases

fwdIndex = {}
revIndex = {}
complements = {"A":"T", "T":"A", "C":"G", "G":"C", "N":"N"} # dict for assignment of complement bases
for i in range(len(text)-k+1): #loop through text and get each kmer
    kmer = text[i:i+k]
    if kmer not in fwdIndex:
        fwdIndex.update({kmer: [i]})
    else:
        kmerValues = [k for k in fwdIndex.get(kmer)]
        kmerValues.append(i)
        fwdIndex.update({kmer: kmerValues})
if rev: #if reverse, additionally return a list of locations
    ### To Do: currently returns location on forward strand where kmer occurs, maybe return negative number in fwdIndex as well?
    for key, values in fwdIndex.items():
        revKey = ''
        revI = []
        for char in key:
            revKey = complements[char] + revKey
        for i in values: revI.append(i + k)
        revIndex.update({revKey: revI})
print(fwdIndex)
print(revIndex)