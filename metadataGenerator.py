# Author: Michael Shamash, McGill University
# Script to generate metadata file using output from various tools

import csv
import argparse
import os

# Construct the argument parser
ap = argparse.ArgumentParser()

# Add the arguments to the parser
ap.add_argument("-vibrant", required=True, help="Input VIBRANT genome quality file location")
ap.add_argument("-demovir", required=True, help="Input Demovir file location")
ap.add_argument("-vcontact", required=True, help="Input vConTACT2 genome_by_genome file location")
ap.add_argument("-crassphage", required=True, help="Input crAssphage BLAST summary file location")
ap.add_argument("-crispr", required=True, help="Input CRISPR spacer matching summary file location")
args = vars(ap.parse_args())

vibrantContigs = {}
demovirContigs = {}
vcontactContigs = {}
crassContigs = []
crisprContigs = {}

contigNames = []

processedContigs = []
line_count = 0

with open(args['vibrant']) as csv_file:
    csv_reader = csv.reader(csv_file, delimiter='\t')
    for row in csv_reader:
        if line_count == 0:
            line_count += 1
        else:
            if row[2] != "complete circular":
                contigName = row[0]
                contigLifeCycle = row[1]

                vibrantContigs[contigName] = contigLifeCycle
                contigNames.append(contigName)

                line_count += 1
    print(f'Processed {line_count-1} VIBRANT contigs.')

line_count = 0

with open(args['demovir']) as csv_file:
    csv_reader = csv.reader(csv_file, delimiter='\t')
    for row in csv_reader:
        if line_count == 0:
            line_count += 1
        else:
            contigName = row[0]
            contigOrder = row[1]
            contigFamily = row[3]

            demovirContigs[contigName] = [contigOrder,contigFamily]

            line_count += 1
    print(f'Processed {line_count-1} Demovir contigs.')

line_count = 0

with open(args['vcontact']) as csv_file:
    csv_reader = csv.reader(csv_file, delimiter=',')
    for row in csv_reader:
        if line_count == 0:
            line_count += 1
        else:
            if "VIRSorter" in row[1]:
                contigName = row[1]
                contigCluster = row[5]

                if row[5] == "":
                    contigCluster = row[6]
                if contigCluster.startswith("Overlap"):
                    contigCluster = "Overlap"

                vcontactContigs[contigName] = contigCluster

                line_count += 1
    print(f'Processed {line_count-1} vConTACT2 contigs.')

line_count = 0

with open(args['crassphage']) as csv_file:
    csv_reader = csv.reader(csv_file, delimiter='\t')
    for row in csv_reader:
        contigName = row[0]

        crassContigs.append(contigName)

        line_count += 1
    print(f'Processed {line_count} crAssphage contigs.')

with open(args['crispr']) as csv_file:
    csv_reader = csv.reader(csv_file, delimiter=',')
    for row in csv_reader:
        contigName = row[0]
        if "No hits found. Sorry" in row[1] or "UNKNOWN" in row[1]:
            crisprContigs[contigName] = "NA"
        else:
            crisprContigs[contigName] = row[1]

        line_count += 1
    print(f'Processed {line_count} CRISPR spacers.')

for contig in contigNames:
    contigName = contig
    defaultTaxonomy = ["Unassigned","Unassigned"]
    contigOrder = demovirContigs.get(contigName,defaultTaxonomy)[0]
    contigCrAssphage = "Y" if contigName in crassContigs else "N"
    contigFamily = "crAssphage" if contigCrAssphage == "Y" else demovirContigs.get(contigName,defaultTaxonomy)[1]
    contigLifeCycle = vibrantContigs[contigName]
    contigCluster = vcontactContigs.get(contigName,"NA")
    contigCRISPR = crisprContigs[contigName]
    processedContigs.append({"ContigName":contigName,"Order":contigOrder,"Family":contigFamily,"crAssphage":contigCrAssphage,"LifeCycle":contigLifeCycle,"ViralCluster":contigCluster,"CRISPRHost":contigCRISPR})

csv_columns = ['ContigName','Order','Family','crAssphage','LifeCycle','ViralCluster','CRISPRHost']

with open("metadata.csv", 'w') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=csv_columns)
        writer.writeheader()
        for contig in processedContigs:    
            writer.writerow(contig)