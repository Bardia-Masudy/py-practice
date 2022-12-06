import argparse

parser = argparse.ArgumentParser(description = "A simple commandline tool for finding exact matches between a string and a query.")
parser.add_argument('query')
parser.add_argument('text')

args = parser.parse_args()

query = args.query
text = args.text

### Naive Search Algorithm

occurences = []
for i in range(len(text) - len(query) + 1): # loop through range of string
    match = True
    for j in range(len(query)): # compare consecutive numbers of query until mismatch
        if not text[i+j] == query[j]:
            match = False
            break
    if match:
        occurences.append(i) # if no mismatches occur, append to list of matches
print(occurences)