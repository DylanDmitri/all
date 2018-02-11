# Python 3.5.2 with anaconda-numpy

import numpy as np
import os
import shutil

try: shutil.rmtree('compressed_matrices/')
except OSError: print('making new folder')
os.mkdir('compressed_matrices')

f = open('control.txt', 'r')
imagename = next(f).split()[-1].strip()
terms = tuple(next(f).split(':')[-1].strip().split(', '))


def diagonal_insertion(vector, dim):
    cols, rows = dim

    result = []
    blank_vector = [0 for _ in range(cols)]
    for i in range(rows):
        sigma_vector = blank_vector[:]
        if i < cols:
            sigma_vector[i] = vector[i]
        result.append(sigma_vector)
    return np.matrix(result, dtype='int')

def compress(filename, terms=10):

    file = open('uncompressed/{}'.format(filename), 'r').read()[:-2]    # strips trailing ';\n'

    A = np.matrix(file)

    n, M = A.shape
    globals()['dimensions'] = n, M

    u, sigma_vals, v = np.linalg.svd(A)

    assert n >= terms
    # sigma_vals[terms:] = [0 for _ in range(n-terms)]
    # sigma = diagonal_insertion(sigma_vals, (M, n))

    new_vals = [0 for _ in range(n)]
    new_vals[terms] = sigma_vals[terms]

    sigma = diagonal_insertion(new_vals,(M,n))

    return u @ sigma @ v

def compress_all_layers(terms):

    folder = 'compressed_matrices/' + str(terms) + '/'

    try:
        os.mkdir(folder)
    except FileExistsError:
        pass

    for filename in ('red.txt', 'blue.txt', 'green.txt'):
        result = compress(filename, terms=terms)

        outfile = open(folder+filename, 'w')
        for line in result.tolist():
            for v in line:
                v = min(255, max(0, int(v+.5))) # whole number 0 to 255
                outfile.write(str(v).ljust(4))
            outfile.write('\n')


    n,M = globals()['dimensions']
    open(folder+'info', 'w').write('''picture is {}x{} pixels

    {} of {} possible terms used
    {} bytes needed for this representation.
    compared to {} bytes needed for the non-compressed image
    a total savings of {:.2f}%
    '''.format(M, n, terms, min(M, n), terms + terms * (n + M), n*M,
               100*(1- (terms + terms * (n + M))/(n*M)))
    )

for t in terms:
    print('compressing with {} terms'.format(t))
    compress_all_layers(int(t))

print('all images compressed to matrices, run <python2.7 image_writer.py> to begin png generation')