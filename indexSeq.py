#def indexSeq(text: str, k: int, rev=False) -> str:

import argparse

parser = argparse.ArgumentParser(description='A utility to construct an indexed dict from all k-mers of a seqeuence. Optionally includes k-mers of reverse strand.')

parser.add_argument('text')
parser.add_argument('k')
parser.add_argument('-s', '--skip', help='Number of characters to skip between k-mers') ##Work on this.
parser.add_argument('-r', '--reverse', action = 'store_true', help='Optionally include kmers of the reverse strand as well. Reverse strand coordinates are represented in the same output space as those of the forward strand, but as a series of negative numbers that index at 1.')

args = parser.parse_args()

text = str(args.text)
k = int(args.k)
rev = args.reverse

def indexKmers(text: int, k: int) -> dict:
    index = {}
    for i in range(len(text)-k+1):
        kmer = text[i:i+k]
        if kmer not in index:
            index.update({kmer: [i]})
        else:
            kmerValues = [k for k in index.get(kmer)]
            kmerValues.append(i)
            index.update({kmer: kmerValues})
    return index

fwdIndex = indexKmers(text, k)
if not rev: print(fwdIndex)
else:
    combinedIndex = fwdIndex
    complements = {"A":"T", "T":"A", "C":"G", "G":"C", "N":"N"} # dict for assignment of complement bases
    revText = ''
    revValues = []
    for char in text: revText = complements[char] + revText # generate reverse complement
    revIndex = indexKmers(revText, k)
    #print(fwdIndex)
    #print(revIndex)
    for key, values in revIndex.items():
        #print(f'Key: {key}, Type-Key: {type(key)}, Values: {values}, Type-Values: {type(values)}')
        revValues = [j+k-len(text)-1 for j in values]
        if key not in fwdIndex:
            combinedIndex.update({key: revValues})
        else:
            kmerValues = [i for i in fwdIndex.get(key)]
            kmerValues.extend(revValues)
            combinedIndex.update({key: kmerValues})
    print(combinedIndex)
