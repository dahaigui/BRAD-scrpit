#!/bin/bash

#hisat2-build ../reference_genome/Brapa30.fa ../reference_genome/Brapa30

samples=$(cat $1);

for sample in ${samples}

do

hisat2 -p 20 --dta -x ../reference_genome/Brapa30 -1 ../GSE106444_fastq/${sample}_1.fastq.gz -2 ../GSE106444_fastq/${sample}_2.fastq.gz -S ${sample}.sam
samtools view -Sb ${sample}.sam -@ 20 > ${sample}.bam
samtools sort ${sample}.bam -@ 20 ${sample}.sort
featureCounts -T 10 -a ../reference_genome/Brapa30.gtf -o ${sample}.txt -p -B -C -f -t gene ${sample}.sort.bam
rm ${sample}.sam ${sample}.bam

done
