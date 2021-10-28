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
#print(sequences)
# loop over every sequence
for i in seq_dict.keys(): 
    print("Processing...", i.rstrip(), len(seq_dict[i])) #, seq_dict[i])
    
    all_proper = []
    # while seqrow contains a lowercase letter
    letter_idx = 0
    # see how many "improper" lowercase letters we need to process from this sequence 
    num_lowers= 0
    for idx in range(len(seq_dict[i])):
        is_proper = True
        if seq_dict[i][idx].islower():
            for j in seq_dict.keys():
                if j != i:
                    if seq_dict[j][idx] != '-':
                        is_proper = False
            if not is_proper:
                num_lowers += 1
             
    #num_lowers = sum([sum([seq_dict[j][letter_idx] == '-' for j in seq_dict.keys() if j != i]) == (len(seq_dict.keys()) - 1) for x in range(len(seq_dict[i]))])
    print("num improper lowers", num_lowers, "/", len(seq_dict[i]))

    og_len = int(num_lowers + len(seq_dict[i]) - 1)
    while letter_idx < og_len:
        #print(letter_idx, "<", og_len)
        z = seq_dict[i][letter_idx]
        if z.islower():
            is_proper = sum([seq_dict[j][letter_idx] == '-' for j in seq_dict.keys() if j != i]) == (len(seq_dict.keys()) - 1)
            if not is_proper: 
                lower_letter = seq_dict[i][letter_idx]
                seq_dict[i][letter_idx] = '-'
                # insert empty columns
                for j in seq_dict.keys():
                    seq_dict[j] = np.array(seq_dict[j])
                    seq_dict[j] = np.insert(seq_dict[j], letter_idx, '-')
                # copy in lower letter
                seq_dict[i][letter_idx] = lower_letter
                all_proper.append(True)
                all_proper.append(True)
            else:
                all_proper.append(True)
        else:
            all_proper.append(True)
            
        letter_idx += 1
    print("all_proper noted", len(all_proper), "/", len(seq_dict[i]))

new_seq_lens = []
with open(args[1], "w+") as w:
    for key in seq_dict.keys():
        #print(key, seq_dict[key])
        w.write(key + "\n")
        w.write(''.join(list(seq_dict[key])) + "\n")
        new_seq_lens.append(len(seq_dict[key]))
print("Avg post seq len:", np.mean(new_seq_lens))
print("Done, written to", args[1])
