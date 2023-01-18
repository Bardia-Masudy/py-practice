#def indexSeq(text: str, k: int, rev=False) -> str:

import argparse

parser = argparse.ArgumentParser(description='A utility to construct an indexed dict from all k-mers of a seqeuence. Optionally includes k-mers of reverse strand.')

parser.add_argument('query')
parser.add_argument('text')
parser.add_argument('k')
parser.add_argument('-s', '--skip', help='Number of characters to skip between k-mers') ##Work on this.
parser.add_argument('-r', '--reverse', action = 'store_true', help='Optionally include kmers of the reverse strand as well. Reverse strand coordinates are represented in the same output space as those of the forward strand, but as a series of negative numbers that index at 1.')
# parser.add_argument('text') This is for the indexed kmers, not the actual genome
#parser.add_argument('-v', '--visualize', action='store_true') Maybe add, may be better to add option for file export.
# parser.add_argument('-t', '--trace', action='store_true') Unsure if traceback is needed.

args = parser.parse_args()

query = args.q
text = str(args.text)
k = int(args.k)
rev = args.reverse

### Function for taking a sequence and generating a dict with indexed sequences of forward and optionally reverse strand.
def indexSeq(text: str, k: int, rev=False) -> dict:
    def indexKmers(text: str, k: int) -> dict:
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
        return combinedIndex

### Function for aproximate matching a substring within a string, and returning a list of matches with lowest edit distance, and their edit distance.
def aproxMatch(query: str, text: str, trace=False) -> list:
    #### Construction of Match Matrix:
    # The matrix can be visualized as a table of numbers corresponding to edit distances between each substring of the query and the reference text.
    #    CATATG
    # ---------
    # G| 111111
    # T| 222121
    # A| 332212
    #
    # Here the query text (q) is shown along the vertical (y) axis, and the reference text (t) is shown along the horizontal (x) axis. This program is computationally inneficient for large matching, and should/would/could/will be implemented to utilize indexing to shorten processing times.

    #### Scoring Matrix Construction: ####
    # purine/pyramidine penalized, indel heavily penalized
    bases = ['A','C','G','T']
    score = [[0 , 2 , 1 , 2 , 4],\
            [2 , 0 , 2 , 1 , 4],\
            [1 , 2 , 0 , 2 , 4],\
            [2 , 1 , 2 , 0 , 4],\
            [4 , 4 , 4 , 4 , 4]]

    matrix = []
    for x in range(len(text)+1): ### this could be more elegant, maybe in one loop
        matrix.append([0]*(len(query)+1))
        
    for y in range(len(query)+1):
        matrix[0][y] = y*score[-1][-1]
        
    for x in range(1, len(text)+1): # function to construct matrix map of edit distances.
        for y in range(1,len(query)+1):
            horiDist = matrix[x-1][y] + score[-1][bases.index(text[x-1])]
            vertDist = matrix[x][y-1] + score[bases.index(query[y-1])][-1]
            diagDist = matrix[x-1][y-1]
            
            if query[y-1] != text[x-1]: diagDist += score[bases.index(text[x-1])][bases.index(query[y-1])]
            
            matrix[x][y] = min(horiDist, vertDist, diagDist)
    
    #### Matrix Traceback: #### Needs to be rewritten to output a list of matches with their positions. 
    lowestEditDistances = []
    editDistanceMatrix = []
    
    # construct a list of terminal edit distances meant for traceback.
    for x in range(1, len(text)+1): 
        editDistanceMatrix.append(matrix[x][len(query)])

    # find all lowest edit distances
    for i, editDist in enumerate(editDistanceMatrix): 
        minDist = min(editDistanceMatrix)
        if editDist <= minDist:
            lowestEditDistances.append(i+1) 

    if trace:    
        # find lowest edit distance difference and traceback from [lowestEditDistances]
        for item in lowestEditDistances:
            x, y = item, len(query) # x is the coordinate on the text, y the coordinate on the query.
            qTrace = ''
            tTrace = ''
            qMatches = []
            tMatches = []
            while y >= 1: # scan through characters from the query in reverse order.

                # edit distances of adjacent coordinates on the matrix
                # diagDist | vertDist
                # --------------------
                # horiDist | "cursor"
                diagDist = matrix[x-1][y-1]
                vertDist = matrix[x][y-1]
                horiDist = matrix[x-1][y]
                    
                #maybe use a match case?
                if min(diagDist, vertDist, horiDist) ==  diagDist:
                    x, y = x-1, y-1
                    qTrace = query[y] + qTrace
                    tTrace = text[x] + tTrace
                elif min(diagDist, vertDist, horiDist) == vertDist:
                    x, y = x, y-1
                    qTrace = query[y] + qTrace
                    tTrace = '-' + tTrace
                elif min(diagDist, vertDist, horiDist) == horiDist:
                    x, y = x-1, y
                    qTrace = '-' + qTrace
                    tTrace = text[x] + tTrace
                
            qMatches.append([qTrace, x])
            tMatches.append([tTrace, x]) # need to output coordinate of trace.

    if not trace: return min(editDistanceMatrix)
    else:
        return qMatches
        return tMatches

# Take sequence, index forward and reverse strand, and generate a dict with sequences.
# Take that dict, loop over it with a sequence, and find kmers that match somewhere in the query.
# Take kmers that match, and do further aproximate matching to see how well they match the query.