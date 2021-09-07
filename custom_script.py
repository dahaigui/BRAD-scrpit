from Bio import SeqIO
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from scipy.stats import chi2_contingency
import numpy as np
import os
import linecache
import datetime

def complementary_chain(string1):
    RULE = {'A':'T' , 'T':'A' , 'C':'G' , 'G':'C' , 'N':'N' , 'a':'t' , 't':'a' , 'c':'g' , 'g':'c' , 'n':'n'}
    list1 = ''
    list2 = list1.join(map(lambda x:RULE[x] , string1))
    string1 = list2[::-1]
    return string1

def get_MSA_and_cluster_tree(filename1):
    midfile1 = filename1 + '.a'
    midfile2 = filename1 + 'ply'
    os.system('muscle -in ' + filename1 + ' -out ' + midfile1)
    os.system('muscle -maketree -in ' + midfile1 + ' -out ' + midfile2)
    MSA = {}
    for seq_record in SeqIO.parse(midfile1, "fasta"):
        MSA[seq_record.id] = str(seq_record.seq)
    cluster_fr1 = open(midfile2, 'r')
    cluster_lines1 = cluster_fr1.readlines()
    newick_str = ''
    for cluster_line1 in cluster_lines1:
        newick_str += cluster_line1.strip()
    cluster_fr1.close()
    result = [MSA, newick_str]
    os.system('rm ' + filename1)
    os.system('rm ' + midfile1)
    os.system('rm ' + midfile2)
    return result

def search_seq(genome, chromosome, startPos, endPos):
    genome_dict = {}
    for seq_record in SeqIO.parse(genome + ".fa", "fasta"):
        genome_dict[seq_record.id] = seq_record.seq
    sequence = genome_dict[chromosome][int(startPos) - 1: int(endPos)]
    return str(sequence)

def get_species_text():
    All_species = GenomeSpecies.objects.all()
    dict1 = {}
    for i in All_species:
        dict1[i.display_text] = i.text
    return dict1

species_text_dict1 = get_species_text()

def get_species_display_text():
    All_species = GenomeSpecies.objects.all()
    dict1 = {}
    for i in All_species:
        dict1[i.text] = i.display_text
    return dict1

species_display_dict1 = get_species_display_text()

def get_synorths_text():
    All_synorths = SynorthsShow.objects.all()
    dict1 = {}
    for i in All_synorths:
        dict1[i.display_text] = i.synorths_show
    return dict1

def get_synorths_display_text():
    All_synorths = SynorthsShow.objects.all()
    dict1 = {}
    for i in All_synorths:
        dict1[i.synorths_show] = i.display_text
    return dict1

def searchMSASeq(request):
    search_type = request.GET['search_type']
    search_gene_str = request.GET['search_gene_str']
    search_gene_list = search_gene_str.split(';')
    dt_ms = datetime.datetime.now().strftime('%Y%m%d%H%M%S%f')
    # print(dt_ms)
    seq_midfile = open(dt_ms + '.fasta', 'w')
    isError = 0
    seq = ''
    for i in search_gene_list[ : -1]:
        # print(i)
        if i != '-':
            if search_type == 'Gene':
                seq_tuple = GeneSequence.objects.filter(geneID=i.strip())
                if len(seq_tuple) == 1:
                    seq = seq_tuple[0].geneSeq
                    seq_midfile.write('>' + i + '\n' + seq + '\n')
                    seq += '>' + i + '\n' + seq + '\n'
                else:
                    isError = 1
            else:
                gene_id = TotalJBrowseGene.objects.filter(geneID=i.strip())
                if len(gene_id) == 1:
                    if search_type == 'CDS':
                        seq = GeneCdsSequence.objects.get(id=gene_id[0].id).cdsSeq
                    else:
                        seq = GeneProteinSequence.objects.get(id=gene_id[0].id).proteinSeq
                    seq_midfile.write('>' + i + '\n' + seq + '\n')
                    seq += '>' + i + '\n' + seq + '\n'
                else:
                    isError = 1
    seq_midfile.close()
    if isError == 1:
        os.system('rm ' + dt_ms + '.fasta')
    data = []
    MSA_and_cluster_tree = get_MSA_and_cluster_tree(dt_ms + '.fasta')
    for key1, value1 in MSA_and_cluster_tree[0].items():
        data_item = {
            'seq': value1,
            'name': key1,
        }
        data.append(data_item)
    data.append(seq)
    return Response(data)

@api_view(['GET'])
def searchMSACompare(request):
    search_seq0 = request.GET['search_seq0']
    search_seq1 = request.GET['search_seq1']
    dt_ms = datetime.datetime.now().strftime('%Y%m%d%H%M%S%f')
    search_seq0_list = search_seq0.strip().split('_')
    search_seq1_list = search_seq1.strip().split('_')
    genome0 = '_'.join(search_seq0_list[0 : -3])
    genome1 = '_'.join(search_seq1_list[0 : -3])
    if int(search_seq0_list[-2]) < int(search_seq0_list[-1]):
        seq_0_strand = '+'
        seq0 = search_seq(species_text_dict1[genome0], search_seq0_list[-3], search_seq0_list[-2], search_seq0_list[-1])
    else:
        seq_0_strand = '-'
        seq0 = search_seq(species_text_dict1[genome0], search_seq0_list[-3], search_seq0_list[-2], search_seq0_list[-1])
        seq0 = complementary_chain(seq0)

    if search_seq1_list[-2] < search_seq1_list[-1]:
        seq_1_strand = '+'
        seq1 = search_seq(species_text_dict1[genome1], search_seq1_list[-3], search_seq1_list[-2], search_seq1_list[-1])
    else:
        seq_1_strand = '-'
        seq1 = search_seq(species_text_dict1[genome1], search_seq1_list[-3], search_seq1_list[-2], search_seq1_list[-1])
        seq1 = complementary_chain(seq1)
    seq_midfile = open(dt_ms + '.fasta', 'w')
    seq_midfile.write('>' + search_seq0 + '_' + seq_0_strand + '\n' + seq0 + '\n')
    seq_midfile.write('>' + search_seq1 + '_' + seq_1_strand + '\n' + seq1 + '\n')
    seq_midfile.close()
    seq = '>' + search_seq0 + '_' + seq_0_strand + '\n' + seq0 + '\n>' + search_seq1 + '_' + seq_1_strand + '\n' + seq1 + '\n'
    data = []
    MSA_and_cluster_tree = get_MSA_and_cluster_tree(dt_ms + '.fasta')
    for key1, value1 in MSA_and_cluster_tree[0].items():
        data_item = {
            'seq': value1,
            'name': key1,
        }
        data.append(data_item)
    data.append(seq)
    return Response(data)

@api_view(['GET'])
def searchETASeq(request):
    search_type = request.GET['search_type']
    search_gene_str = request.GET['search_gene_str']
    search_gene_list = search_gene_str.split(';')
    dt_ms = datetime.datetime.now().strftime('%Y%m%d%H%M%S%f')
    # print(dt_ms)
    seq_midfile = open(dt_ms + '.fasta', 'w')
    isError = 0
    seq = ''
    for i in search_gene_list[ : -1]:
        # print(i)
        if i != '-':
            if search_type == 'Gene':
                seq_tuple = GeneSequence.objects.filter(geneID=i.strip())
                if len(seq_tuple) == 1:
                    seq = seq_tuple[0].geneSeq
                    seq_midfile.write('>' + i + '\n' + seq + '\n')
                    seq += '>' + i + '\n' + seq + '\n'
                else:
                    isError = 1
            else:
                gene_id = TotalJBrowseGene.objects.filter(geneID=i.strip())
                if len(gene_id) == 1:
                    if search_type == 'CDS':
                        seq = GeneCdsSequence.objects.get(id=gene_id[0].id).cdsSeq
                    else:
                        seq = GeneProteinSequence.objects.get(id=gene_id[0].id).proteinSeq
                    seq_midfile.write('>' + i + '\n' + seq + '\n')
                    seq += '>' + i + '\n' + seq + '\n'
                else:
                    isError = 1
    seq_midfile.close()
    if isError == 1:
        os.system('rm ' + dt_ms + '.fasta')
    data = []
    MSA_and_cluster_tree = get_MSA_and_cluster_tree(dt_ms + '.fasta')
    data.append(MSA_and_cluster_tree[1])
    data.append(seq)
    return Response(data)

def searchFragment(request):
    search_chromosome = request.GET['search_chromosome']
    startPos = request.GET['startPos']
    endPos = request.GET['endPos']
    strand = request.GET['strand']
    search_genome = request.GET['search_genome']
    search_genome1 = species_text_dict1[search_genome]
    if int(startPos) > int(endPos):
        mid_Pos = startPos
        startPos = endPos
        endPos = mid_Pos
    data = []
    fragment = search_seq(search_genome1, search_chromosome, startPos, endPos)
    if strand == '+':
        fragment = str(fragment)
    else:
        fragment = complementary_chain(str(fragment))
    sequence = {
        'gene_ID': '>' + search_genome + '_' + search_chromosome + '_' + startPos + '_' + endPos + '_' + strand,
        'Seq': fragment,
        'download': '>' + search_genome + '_' + search_chromosome + '_' + startPos + '_' + endPos + '_' + strand + '\n' + fragment,
    }
    data.append(sequence)
    return Response(data)