# Author: Michael Shamash, McGill University
# Script to generate abundance matrix (feature table) file with either reads or relative abundances

import csv
import argparse

# Construct the argument parser
ap = argparse.ArgumentParser()

ap.add_argument("-i", required=True, help="Input CSV file location")
ap.add_argument("--binary", action = "store_true", help="Use this flag to output a binary matrix (instead of normal relative abundance matrix), useful for calculating a Jaccard index")
ap.add_argument("--reads", action = "store_true", help="Use this flag to output a read count matrix (instead of normal relative abundance matrix), useful for rarefaction curves")

args = vars(ap.parse_args())

class Contig(object):
    name = ""
    date = ""
    abund = 0.0
    reads = 0

    def __init__(self, name, date, abund, reads):
        self.name = name
        self.date = date
        self.abund = abund
        self.reads = reads

def make_contig(name, date, abund, reads):
    contig = Contig(name, date, abund, reads)
    return contig

contigs = []
samples = {}
line_count = 0

with open(args['i']) as csv_file:
    csv_reader = csv.reader(csv_file, delimiter=',')
    for row in csv_reader:
        if line_count == 0:
            line_count += 1
        else:
            date = row[0]
            contigName = row[1]
            contigAbund = row[2]
            numberReads = row[8]

            contigs.append(make_contig(contigName, date, contigAbund, numberReads))
            samples[date] = {}          

            line_count += 1
    print(f'Processed {line_count-1} contigs.')

contigNames = ["Sample"]

for contig in contigs:
    if args['binary']:
        if float(contig.abund) > 0:
            samples[contig.date][contig.name] = 1
        else:
            samples[contig.date][contig.name] = 0
    elif args['reads']:
        samples[contig.date][contig.name] = contig.reads
    else:
        samples[contig.date][contig.name] = contig.abund
    if contig.name not in contigNames:
        contigNames.append(contig.name)

with open('matrix.csv', 'w') as csvfile:
    writer = csv.DictWriter(csvfile, fieldnames=contigNames)
    writer.writeheader()
    for sample in samples:
        row = {}
        for contig in contigNames:
            currentSample = samples[sample]
            if contig == "Sample":
                row["Sample"] = sample
            else:
                row[contig] = currentSample.get(contig,0)
            
        writer.writerow(row)
