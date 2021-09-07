#sys.argv[1] -> the species you want to get subgenome(such as BOL20)
#sys.argv[2] -> 3genomes_full_tandem_AKBr_v1.5.txt.filtered
#sys.argv[3] -> final.txt
#sys.argv[4] -> result file name

import linecache
import sys
import os
import re

def get_subgenome(filename1, filename2, filename3):
    outfile = open(sys.argv[4], 'w')
    final_list = []
    fr3 = open(filename3, 'r')
    lines3 = fr3.readlines()
    for line3 in lines3:
        final_list.append(line3.strip())
    if filename1 in final_list:
        coords_filename = 'final_coords/' + filename1 + '.gff.coords.final'
    else:
        coords_filename = 'coords/' + filename1 + '.gff.coords'
    fr2 = open(filename2, 'r')
    lines2 = fr2.readlines()
    LF_str = ''
    MF1_str = ''
    MF2_str = ''
    # Ath10_dict1 => AKBr and block information
    Ath10_dict1 = {}
    # Ath10_dict2 => the subgenome gene of every Ath10 gene
    Ath10_dict2 = {}
    for line2 in lines2:
        list2 = line2.strip().split('\t')
        Ath10_dict1[list2[1]] = list2[1 : 7]
        Ath10_dict2[list2[1]] = ['-' , '-' , '-']
        if list2[4] != '-':
            LF_str += list2[4] + ';'
        if list2[5] != '-':
            MF1_str += list2[5] + ';'
        if list2[6] != '-':
            MF2_str += list2[6] + ';'
    # print(Ath10_dict1)
    Brapa15_fr1 = open('Brapa15.final/' + filename1 + '_to_Brapa15.SynOrths', 'r')
    Brapa15_lines1 = Brapa15_fr1.readlines()
    Brapa15_dict = {}
    for Brapa15_line1 in Brapa15_lines1:
        Brapa15_dict[Brapa15_line1.strip().split('\t')[0]] = Brapa15_line1.strip().split('\t')[4]

    subgenome_index = 0
    Ath10_fr1 = open('Ath10.final/' + filename1 + '_to_Ath10.SynOrths', 'r')
    Ath10_lines1 = Ath10_fr1.readlines()
    for Ath10_line1 in Ath10_lines1:
        Ath10_list1 =  Ath10_line1.strip().split('\t')
        # start to judge
        try:
            # have syntenic gene with Brapa15, Brapa15_synorths => Brapa15 synorths gene with aim species
            Brapa15_synorths = Brapa15_dict[Ath10_list1[0]]
            if re.search(Brapa15_synorths, LF_str):
                subgenome_index = 1
            elif re.search(Brapa15_synorths, MF1_str):
                subgenome_index = 2
            elif re.search(Brapa15_synorths, MF2_str):
                subgenome_index = 3
            else:
                row_num = int(os.popen("cat " + coords_filename + " | grep -n " + Ath10_list1[0] + " | awk -F: '{print $1}'").read())
        except KeyError:
            row_num = int(os.popen("cat " + coords_filename + " | grep -n " + Ath10_list1[0] + " | awk -F: '{print $1}'").read())
        if subgenome_index == 0:
            if row_num > 10:
                for i in range(row_num , row_num - 10, -1):
                    candidate_gene = linecache.getline(coords_filename, i).strip().split('\t')[0]
                    try:
                        Brapa15_synorths = Brapa15_dict[candidate_gene]
                        if re.search(Brapa15_synorths, LF_str):
                            subgenome_index = 1
                        elif re.search(Brapa15_synorths, MF1_str):
                            subgenome_index = 2
                        elif re.search(Brapa15_synorths, MF2_str):
                            subgenome_index = 3
                        else:
                            subgenome_index = 0
                    except KeyError:
                        continue
            else:
                for i in range(row_num , row_num + 30):
                    candidate_gene = linecache.getline(coords_filename, i).strip().split('\t')[0]
                    try:
                        Brapa15_synorths = Brapa15_dict[candidate_gene]
                        if re.search(Brapa15_synorths, LF_str):
                            subgenome_index = 1
                        elif re.search(Brapa15_synorths, MF1_str):
                            subgenome_index = 2
                        elif re.search(Brapa15_synorths, MF2_str):
                            subgenome_index = 3
                        else:
                            subgenome_index = 0
                    except KeyError:
                        continue
        if subgenome_index == 1:
            try:
                Ath10_dict2[Ath10_list1[4]][0] = Ath10_list1[0]
            except KeyError:
                pass
        elif subgenome_index == 2:
            try:
                Ath10_dict2[Ath10_list1[4]][1] = Ath10_list1[0]
            except KeyError:
                pass
        elif subgenome_index == 3:
            try:
                Ath10_dict2[Ath10_list1[4]][2] = Ath10_list1[0]
            except KeyError:
                pass
        # print(Ath10_list1[4])
        # print(subgenome_index)
    for key1, value1 in Ath10_dict1.items():
        outfile.write('\t'.join(value1[0 : 3]) + '\t' + '\t'.join(Ath10_dict2[key1]) + '\n')
    outfile.close()
    fr2.close()
    fr3.close()
    Brapa15_fr1.close()
    Ath10_fr1.close()

get_subgenome(sys.argv[1], sys.argv[2], sys.argv[3])
