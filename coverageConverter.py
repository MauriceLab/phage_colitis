# Author: Michael Shamash, McGill University

import csv
import argparse
import os

# Construct the argument parser
ap = argparse.ArgumentParser()

# Add the arguments to the parser
ap.add_argument("-i", required=True, help="Input CSV file location")
ap.add_argument("-m", required=True, help="Input metadata CSV file location")
ap.add_argument("-outfmt", required=True, help="Output format can be 'merged' or 'sample'")
args = vars(ap.parse_args())

class Contig(object):
    name = ""
    date = ""
    cov = 0.0
    reads = 0

    def __init__(self, name, date, cov, reads):
        self.name = name
        self.date = date
        self.cov = cov
        self.reads = reads

def make_contig(name, date, cov, reads):
    contig = Contig(name, date, cov, reads)
    return contig

contigs = []
datesCov = {}
line_count = 0

with open(args['i']) as csv_file:
    csv_reader = csv.reader(csv_file, delimiter=',')
    for row in csv_reader:
        if line_count == 0:
            line_count += 1
        else:
            date = row[0].split(" - ")[0]
            contigName = row[0].split(" - ")[1]
            contigReads = row[1]
            contigCov = row[4]

            datesCov[date] = float(row[4]) + float(datesCov.get(date,0))

            contigs.append(make_contig(contigName, date, contigCov, contigReads))

            line_count += 1
    print(f'Processed {line_count-1} lines.')

processedContigs = {}

metadataDict = {}
line_count = 0

with open(args['m']) as csv_file:
    csv_reader = csv.reader(csv_file, delimiter=',')
    for row in csv_reader:
        if line_count == 0:
            line_count += 1
        else:
            metadataDict[row[0]] = [row[1], row[2], row[3], row[4], row[5], row[6]]
            line_count += 1
    print(f'Processed {line_count-1} taxa.')

for contig in contigs:
    contigAbundance = float(contig.cov) / datesCov[contig.date]

    processedContigsOnDate = processedContigs.get(contig.date, {})

    #Make contigs which don't exist "Unassigned"
    metadataObject = metadataDict.get(contig.name, ["Unassigned","Unassigned","Unassigned","Unassigned","Unassigned","Unassigned"])

    #Make Caudovirales(Unassigned) into Caudovirales(Caudovirales); easier to process visually in R
    if metadataObject[0] == "Caudovirales" and metadataObject[1] == "Unassigned":
        metadataObject[1] = "Caudovirales"

    processedContigsOnDate[contig.name] = [contigAbundance,metadataObject[0],metadataObject[1],metadataObject[2],metadataObject[3],metadataObject[4],metadataObject[5],contig.reads]

    processedContigs[contig.date] = processedContigsOnDate


csv_columns = ['Sample','ContigName','RelAbundance','Order','Family','crAssphage','LifeCycle','ViralCluster','CRISPRMatch','Reads']

if args['outfmt'] == "merged":
    filePath = ""
    path, file = os.path.split(args['i'])
    
    if path != "" :
        filePath = path + "/merged-" + file
    else:
        filePath = "merged-" + file

    with open(filePath, 'w') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=csv_columns)
        writer.writeheader()
        for date in processedContigs:    
            for key, value in processedContigs[date].items():
                writer.writerow({"Sample":date, "ContigName":key, "RelAbundance":value[0], "Order":value[1], "Family":value[2], "crAssphage":value[3], "LifeCycle":value[4], "ViralCluster":value[5], "CRISPRMatch": value[6], "Reads":value[7]})

elif args['outfmt'] == "sample":
    for date in processedContigs:
        with open(date+'.csv', 'w') as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=csv_columns)
            writer.writeheader()
            for key, value in processedContigs[date].items():
                writer.writerow({"Sample":date, "ContigName":key, "RelAbundance":value[0], "Order":value[1], "Family":value[2], "crAssphage":value[3], "LifeCycle":value[4], "ViralCluster":value[5], "CRISPRMatch": value[6], "Reads":value[7]})
