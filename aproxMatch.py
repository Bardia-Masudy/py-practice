### 

import argparse

parser = argparse.ArgumentParser(description = "Aproximate matching algorithm for sequences using dynamic coding approach. computationally inefficient for long queries unleass paired with an indexing algorith.")
parser.add_argument('q')
parser.add_argument('t')
parser.add_argument('-v', '--visualize', action='store_true')
parser.add_argument('-t', '--trace', action='store_true')

args = parser.parse_args()

q = args.q
t = args.t
vis = args.visualize
trace = args.trace

#def aproxMatch(q, t, vis=False, trace=False):
#### Construction of Match Matrix:
# The matrix can be visualized as a table of numbers corresponding to edit distances between each substring of the query and the reference text.
#    CATATG
# ---------
# G| 111111
# T| 222121
# A| 332212
#
# Here the query text (q) is shown along the vertical (y) axis, and the reference text (t) is shown along the horizontal (x) axis. This program is computationally inneficient for large matching, and should/would/could/will be implemented to utilize indexing to shorten processing times.
# vis=True generates an identical graph to the above, otherwise only a matrix is returned
# trace=True appends a visualization for tracebacks of the fits with the lowest edit distance to the visualization, and (WIP, provides sequences of matches)

## Scoring Matrix:
# purine/pyramidine penalized, indel heavily penalized
bases = ['A','C','G','T']
score = [[0 , 2 , 1 , 2 , 4],\
         [2 , 0 , 2 , 1 , 4],\
         [1 , 2 , 0 , 2 , 4],\
         [2 , 1 , 2 , 0 , 4],\
         [4 , 4 , 4 , 4 , 4]]

matrix = []
for x in range(len(t)+1): ### this could be more elegant, maybe in one loop
    matrix.append([0]*(len(q)+1))
    
for y in range(len(q)+1):
    matrix[0][y] = y*score[-1][-1]
    

    
for x in range(1, len(t)+1): # function to construct matrix map of edit distances.
    for y in range(1,len(q)+1):
        horiDist = matrix[x-1][y] + score[-1][bases.index(t[x-1])]
        vertDist = matrix[x][y-1] + score[bases.index(q[y-1])][-1] ## TO DO: add references to scoring matrix, publication?
        diagDist = matrix[x-1][y-1]
        
        if q[y-1] != t[x-1]: diagDist += score[bases.index(t[x-1])][bases.index(q[y-1])]
        
        matrix[x][y] = min(horiDist, vertDist, diagDist)
    
    
#### Optional Matrix Traceback: 
if trace: # optional function for tracing indeces of best edit distances.
    occurences = []
    traceback = []
    dists = []
    for x in range(1, len(t)+1): # construct a list of edit distances for traceback.
        dists.append(matrix[x][len(q)])

    for i, editDist in enumerate(dists): # find all lowest edit distances
        minDist = min(dists)
        if editDist <= minDist:
            occurences.append(i+1)
        
    # find lowest edit distance difference and traceback from [occurences]
    for i in occurences:
        x, y = i, len(q)
        qTrace = ''
        tTrace = ''
        qTraces = []
        tTraces = []
        while y >= 1:

            # edit distances of adjacent coordinates on the matrix
            # diagDist | vertDist
            # --------------------
            # horiDist | "cursor"
            diagDist = matrix[x-1][y-1]
            vertDist = matrix[x][y-1]
            horiDist = matrix[x-1][y]
                
            traceback.append((x, y)) # add path for traceback
                
            if min(diagDist, vertDist, horiDist) ==  diagDist:
                x, y = x-1, y-1
                qTrace = q[y] + qTrace
                tTrace = t[x] + tTrace
            elif min(diagDist, vertDist, horiDist) == vertDist:
                x, y = x, y-1
                qTrace = q[y] + qTrace
                tTrace = '-' + tTrace
            elif min(diagDist, vertDist, horiDist) == horiDist:
                x, y = x-1, y
                qTrace = '-' + qTrace
                tTrace = t[x] + tTrace
            
        qTraces.append(qTrace)
        tTraces.append(tTrace)
        
    # generate sequences with gaps for visualization
    # optimally in a form that has metadata in a fasta-like format

    print(qTraces)
    print(tTraces)
            
    if vis: # append traceback path to visulaization
        for x, y in traceback: ### visualize traceback
            #matrix[x][y] = "█"
            matrix[x][y] = "0"
    
#### Visualization of Matrix:
if vis: # optional handling for table visualization of edit distances
    print('   ' + t)
    print('_'*(len(t)+3))
    for y in range(1, len(q)+1):

        print(q[y-1], end='|')
        for x in range(len(t)+1):
            if x == len(t):
                print(chr(int(matrix[x][y])+48))
            else:
                print(chr(int(matrix[x][y])+48), end='')
else:
    print(matrix)


### Known issues:
# - Haven't implemented use of the scoring matrix yet, maybe find a publication for BLOSUM or NCBI BLASTN for an accurate one?
#       - Need a way to visualize edit distances in ASCII for >9 numbers. 
#         Maybe some way similar to Phred, or based off of "opacity" of symbols?