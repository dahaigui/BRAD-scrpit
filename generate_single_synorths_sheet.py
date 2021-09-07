#sys.argv[1] -> the species you want to get subgenome(such as BOL20)
#sys.argv[2] -> subgenome_AKBr_Brapa15.txt
#sys.argv[3] -> result file name

import sys
import os
import re

def single_synorths_sheet(species, filename1):
    outfile = open(sys.argv[3], 'w')
    #Ath10_Brapa15_dict = {}
    fr1 = open(filename1, 'r')
    lines1 = fr1.readlines()
    #for line1 in lines1:
        #for i in line1.strip().split('\t')[3 : 6]:
            #if i != '-':
                #Ath10_Brapa15_dict[i] = 1
    # to delete same gene in Brapa15_species_dict
    Ath10_species_dict = {}
    # to fill in species list
    Ath10_species_list_dict = {}
    fr2 = open('single_subgenome/' + species + '.subgenome.txt', 'r')
    lines2 = fr2.readlines()
    for line2 in lines2:
        list2 = line2.strip().split('\t')
        Ath10_species_list_dict[list2[0]] = list2[3 : 6]
        for i in list2[3 : 6]:
            if i != '-':
                Ath10_species_dict[i] = 1
    #print(len(Ath10_species_dict))
    Brapa15_species_dict = {}
    num1 = 0
    num2 = 0
    fr3 = open('results/' + species + '_to_Brapa15.sheet', 'r')
    lines3 = fr3.readlines()
    for line3 in lines3:
        list3 = line3.strip().split('\t')
        if list3[1] != '.':
            #print(list3[1])
            try:
                if Ath10_species_dict[list3[1]]:
                    num1 += 1
            except KeyError:
                num2 += 1
                Brapa15_species_dict[list3[0]] = list3[1]
    #print(Ath10_species_dict['BjuA037623'])
    #print(Brapa15_species_dict)
    print(num1)
    print(num2)
    for line1 in lines1:
        list1 = line1.strip().split('\t') + ['-', '-', '-']
        if list1[0] == '-':
            for i in range(3, 6):
                if list1[i] != '-':
                    try:
                        list1[i + 3] = Brapa15_species_dict[list1[i]]
                    except KeyError:
                        pass
        else:
            try:
                list1[6 : 9] = Ath10_species_list_dict[list1[0]]
            except KeyError:
                pass
        outfile.write('\t'.join(list1) + '\n')
    outfile.close()
    fr1.close()
    fr2.close()
    fr3.close()

single_synorths_sheet(sys.argv[1], sys.argv[2])
