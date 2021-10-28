#!/usr/bin/python

import sys, getopt
import numpy as np

args = sys.argv[1:]
print(args)
#in_aln = np.loadtxt(args[0], dtype=str)
in_aln = open(args[0], "r").readlines()
#print("in_aln", in_aln)
seq_dict = dict()
name = ''
seq = ''

#print(in_aln)
og_aln_len = len(list(in_aln[1]))
checked = np.zeros((og_aln_len))
seq_dict = dict()
name = ''
seq = ''

for v in in_aln:
    if v[0] == '>':
        name = v.rstrip()
    else:
        v = v.rstrip()
        if name in seq_dict.keys():
            seq_dict[name].extend(list(v))
        else:
            seq_dict[name] = list(v)

sequences = np.array([np.array(list(seq_dict[x]), dtype=object) for x in seq_dict], dtype=object)
numseq = len(sequences)
aln_ln = len(sequences[0])
for i in range(aln_ln):
#    print(sequences[:,i])
#    print(sequences[:,i] == "-")
    if np.count_nonzero(sequences[:,i]=="-") != (numseq - 1):
        # check if they're uppercase letters
        for j in sequences[:,i]:
            if j.islower():
                print(i)

print("Done!")
