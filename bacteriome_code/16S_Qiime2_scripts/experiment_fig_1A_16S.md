```bash
source activate qiime2-2020.6

```

    bash: activate: No such file or directory





```bash
cd /Users/anshulsinha/Desktop/Sequencing_analyses/16S_ali_experiment_2018_cross_infect/fastq
```


```bash
qiime tools import \
    --type 'SampleData[PairedEndSequencesWithQuality]'\
    --input-path /Users/anshulsinha/Desktop/Sequencing_analyses/16S_ali_experiment_2018_cross_infect/fastq/rainin_manifest_ali_2018.csv \
    --output-path paired-end-demux-aliseq.qza \
    --input-format PairedEndFastqManifestPhred33
#Importing data from fastq files

```

    
    Aborted!



```bash
qiime cutadapt trim-paired \
--i-demultiplexed-sequences paired-end-demux-aliseq.qza \
--p-cores 4 \
--p-front-f GTGCCAGCMGCCGCGGTAA \
--p-front-r  GGACTACHVGGGTWTCTAAT \
--o-trimmed-sequences paired-end-demux-trimmed-ali-seq.qza
#Trimming forward and reverse primers + tag sequences
#This command will cut everything before the forward or reverse sequence
#type zless and then copy your file path to see if sequences are removed 
```

    [32mSaved SampleData[PairedEndSequencesWithQuality] to: paired-end-demux-trimmed-ali-seq.qza[0m
    (qiime2-2020.6) 




```bash
qiime demux summarize \
--i-data paired-end-demux-trimmed-ali-seq.qza \
--o-visualization paired-end-demux-trimmed-ali-seq.qzv 
```

    [32mSaved Visualization to: paired-end-demux-trimmed-ali-seq.qzv[0m
    (qiime2-2020.6) 




```bash
qiime tools view paired-end-demux-trimmed-ali-seq.qzv 
```

    Press the 'q' key, Control-C, or Control-D to quit. This view may no longer be accessible or work correctly after quitting.(qiime2-2020.6) 


```bash
qiime dada2 denoise-paired \
--i-demultiplexed-seqs paired-end-demux-trimmed-ali-seq.qza \
--o-table table.qza \
--o-representative-sequences rep-seqs-trimmed.qza \
--p-min-fold-parent-over-abundance 5 \
--p-trunc-len-f 220 \
--p-trunc-len-r 220 \
--p-n-threads 0 \
--o-denoising-stats stats-dada2-trimmed.qza
#trimming seqs based on quality and running dada2
#originally had a high proportion of chimeras, even after trimming primers off
#changed chimera stringency in dada2 using the p-min fold over abundance to 5 from default 2 
```

    [32mSaved FeatureTable[Frequency] to: table.qza[0m
    [32mSaved FeatureData[Sequence] to: rep-seqs-trimmed.qza[0m
    [32mSaved SampleData[DADA2Stats] to: stats-dada2-trimmed.qza[0m



```bash
qiime metadata tabulate \
--m-input-file stats-dada2-trimmed.qza \
--o-visualization stats-dada2-trimmed.qzv
# how many reads passed through each dada2 step per sample.

```

    [32mSaved Visualization to: stats-dada2-trimmed.qzv[0m



```bash
qiime feature-table summarize \
--i-table table.qza \
--o-visualization table.qzv \
--m-sample-metadata-file /Users/anshulsinha/Desktop/Sequencing_analyses/16S_ali_experiment_2018_cross_infect/fastq/rainin_metadata_ali_2018.txt \

#creating a visual summary of the data
#inputting the metadata file here- associating a time point, treatment group to a sample
```

    [32mSaved Visualization to: table.qzv[0m



```bash
qiime feature-table filter-features \
  --i-table table.qza \
  --p-min-samples 2 \
  --o-filtered-table table-f1.qza
  
  qiime feature-table filter-features \
  --i-table table-f1.qza \
  --p-min-frequency 10 \
  --o-filtered-table table-f2.qza
  
  #Removing features with less than 10 reads per sample and those only found in a single sample
```

    [32mSaved FeatureTable[Frequency] to: table-f1.qza[0m
    [32mSaved FeatureTable[Frequency] to: table-f2.qza[0m



```bash
qiime feature-table summarize \
--i-table table-f2.qza \
--o-visualization table-f2.qzv \
--m-sample-metadata-file /Users/anshulsinha/Desktop/Sequencing_analyses/16S_ali_experiment_2018_cross_infect/fastq/rainin_metadata_ali_2018.txt 

```

    [32mSaved Visualization to: table-f2.qzv[0m



```bash
qiime feature-table tabulate-seqs \
    --i-data rep-seqs-trimmed.qza \
    --o-visualization rep-seqs-trimmed.qzv
```

    
    Aborted!



```bash
qiime feature-table filter-samples \
--i-table table-f2.qza \
--m-metadata-file /Users/anshulsinha/Desktop/Sequencing_analyses/16S_ali_experiment_2018_cross_infect/fastq/rainin_metadata_ali_2018.txt \
--p-where "bac_treatment = 'UC'" \
--o-filtered-table UCB-filtered-table.qza
#filtering table based on bacterial community
```

    [32mSaved FeatureTable[Frequency] to: UCB-filtered-table.qza[0m



```bash
qiime feature-table filter-samples \
--i-table UCB-filtered-table.qza \
--m-metadata-file /Users/anshulsinha/Desktop/Sequencing_analyses/16S_ali_experiment_2018_cross_infect/fastq/rainin_metadata_ali_2018.txt \
--p-where "period = 'Colonization'" \
--o-filtered-table UCB-col-filtered-table.qza
#Because groups were split after phage gavage in the experiment, based on the metadata, some groups only have samples belonging to phage gavage and DSS period
#Filtering the UC and healthy for just the colonization period so that these can be later merged with the groups that do not have baseline values 
```

    [32mSaved FeatureTable[Frequency] to: UCB-col-filtered-table.qza[0m



```bash
qiime feature-table filter-samples \
--i-table table-f2.qza \
--m-metadata-file /Users/anshulsinha/Desktop/Sequencing_analyses/16S_ali_experiment_2018_cross_infect/fastq/rainin_metadata_ali_2018.txt \
--p-where "bac_treatment = 'Healthy'" \
--o-filtered-table HB-filtered-table.qza
#filtering table based on bacterial community 
```

    [32mSaved FeatureTable[Frequency] to: HB-filtered-table.qza[0m



```bash
qiime feature-table filter-samples \
--i-table HB-filtered-table.qza \
--m-metadata-file /Users/anshulsinha/Desktop/Sequencing_analyses/16S_ali_experiment_2018_cross_infect/fastq/rainin_metadata_ali_2018.txt \
--p-where "period = 'Colonization'" \
--o-filtered-table HB-col-filtered-table.qza
#Because groups were split after phage gavage in the experiment, based on the metadata some groups only have samples belonging to phage gavage and DSS period
#Filtering the UC and healthy for just the colonization period so that these can be later merged with the groups that do not have baseline values 
```

    [32mSaved FeatureTable[Frequency] to: HB-col-filtered-table.qza[0m



```bash
qiime feature-table filter-samples \
--i-table table-f2.qza \
--m-metadata-file /Users/anshulsinha/Desktop/Sequencing_analyses/16S_ali_experiment_2018_cross_infect/fastq/rainin_metadata_ali_2018.txt \
--p-where "phage_treatment = 'UCB_HP'" \
--o-filtered-table UCB_HP-filtered-table.qza
```

    [32mSaved FeatureTable[Frequency] to: UCB_HP-filtered-table.qza[0m



```bash
qiime feature-table filter-samples \
--i-table table-f2.qza \
--m-metadata-file /Users/anshulsinha/Desktop/Sequencing_analyses/16S_ali_experiment_2018_cross_infect/fastq/rainin_metadata_ali_2018.txt \
--p-where "phage_treatment = 'HB_UCP'" \
--o-filtered-table HB_UCP-filtered-table.qza
```

    [32mSaved FeatureTable[Frequency] to: HB_UCP-filtered-table.qza[0m



```bash
qiime feature-table filter-samples \
--i-table table-f2.qza \
--m-metadata-file /Users/anshulsinha/Desktop/Sequencing_analyses/16S_ali_experiment_2018_cross_infect/fastq/rainin_metadata_ali_2018.txt \
--p-where "phage_treatment = 'UCB_UCP'" \
--o-filtered-table UCB_UCP-filtered-table1.qza
```

    [32mSaved FeatureTable[Frequency] to: UCB_UCP-filtered-table1.qza[0m



```bash
qiime feature-table merge \
--i-tables UCB_UCP-filtered-table1.qza \
--i-tables  UCB-col-filtered-table.qza \
--o-merged-table UCB-UCP-table.qza
#Merging the UCB-UCP group so that it has the  baseline values
```

    [32mSaved FeatureTable[Frequency] to: UCB-UCP-table.qza[0m



```bash
qiime feature-table merge \
--i-tables HB-col-filtered-table.qza \
--i-tables  HB_HP-filtered-table1.qza \
--o-merged-table HB-HP-table.qza
#Merging the HB-HP group so that it has the  baseline values
```

    [32mSaved FeatureTable[Frequency] to: HB-HP-table.qza[0m



```bash
qiime feature-table filter-samples \
--i-table table-f2.qza \
--m-metadata-file /Users/anshulsinha/Desktop/Sequencing_analyses/16S_ali_experiment_2018_cross_infect/fastq/rainin_metadata_ali_2018.txt \
--p-where "phage_treatment = 'HB_HP'" \
--o-filtered-table HB_HP-filtered-table1.qza
#Filtering for Healty bacteria + Healthy phage treatment
```

    [32mSaved FeatureTable[Frequency] to: HB_HP-filtered-table1.qza[0m



```bash
qiime feature-table filter-samples \
--i-table table-f2.qza \
--m-metadata-file /Users/anshulsinha/Desktop/Sequencing_analyses/16S_ali_experiment_2018_cross_infect/fastq/rainin_metadata_ali_2018.txt \
--p-where "Period = 'Colonization'" \
--o-filtered-table colonization-filtered-table.qza
#Filtering for samples only in the bacterial colonization period 
```

    [32mSaved FeatureTable[Frequency] to: colonization-filtered-table.qza[0m



```bash
qiime feature-table filter-samples \
--i-table table-f2.qza \
--m-metadata-file /Users/anshulsinha/Desktop/Sequencing_analyses/16S_ali_experiment_2018_cross_infect/fastq/rainin_metadata_ali_2018.txt \
--p-where "Period = 'Gavage'" \
--o-filtered-table gav-filtered-table.qza
#Filtering for samples only in the phage gavage period 
```

    [32mSaved FeatureTable[Frequency] to: gav-filtered-table.qza[0m



```bash
#for ANCOM comparison of each phage treatment during phage gavage period
qiime feature-table filter-samples \
--i-table gav-filtered-table.qza \
--m-metadata-file /Users/anshulsinha/Desktop/Sequencing_analyses/16S_ali_experiment_2018_cross_infect/fastq/rainin_metadata_ali_2018.txt \
--p-where "bac_treatment = 'Healthy'" \
--o-filtered-table Hbacgav-filtered-table.qza
```

    [32mSaved FeatureTable[Frequency] to: Hbacgav-filtered-table.qza[0m



```bash
#for ANCOM comparison of each phage treatment during phage gavage period
qiime feature-table filter-samples \
--i-table gav-filtered-table.qza \
--m-metadata-file /Users/anshulsinha/Desktop/Sequencing_analyses/16S_ali_experiment_2018_cross_infect/fastq/rainin_metadata_ali_2018.txt \
--p-where "bac_treatment = 'UC'" \
--o-filtered-table UCbacgav-filtered-table.qza
```

    [32mSaved FeatureTable[Frequency] to: UCbacgav-filtered-table.qza[0m



```bash
qiime feature-table filter-samples \
--i-table table-f2.qza \
--m-metadata-file /Users/anshulsinha/Desktop/Sequencing_analyses/16S_ali_experiment_2018_cross_infect/fastq/rainin_metadata_ali_2018.txt \
--p-where "Period = 'DSS+Washout'" \
--o-filtered-table Dss-filtered-table.qza
##Filtering for samples only in the DSS/washout period 
```

    [32mSaved FeatureTable[Frequency] to: Dss-filtered-table.qza[0m



```bash
#for ANCOM comparison of each phage treatment during DSS/Washout period
qiime feature-table filter-samples \
--i-table Dss-filtered-table.qza \
--m-metadata-file /Users/anshulsinha/Desktop/Sequencing_analyses/16S_ali_experiment_2018_cross_infect/fastq/rainin_metadata_ali_2018.txt \
--p-where "bac_treatment = 'Healthy'" \
--o-filtered-table HbacDss-filtered-table.qza
```

    [32mSaved FeatureTable[Frequency] to: HbacDss-filtered-table.qza[0m



```bash
#for ANCOM comparison of each phage treatment during DSS/Washout period
qiime feature-table filter-samples \
--i-table Dss-filtered-table.qza \
--m-metadata-file /Users/anshulsinha/Desktop/Sequencing_analyses/16S_ali_experiment_2018_cross_infect/fastq/rainin_metadata_ali_2018.txt \
--p-where "bac_treatment = 'UC'" \
--o-filtered-table UCDss-filtered-table.qza
```

    [32mSaved FeatureTable[Frequency] to: UCDss-filtered-table.qza[0m



```bash
qiime phylogeny align-to-tree-mafft-fasttree \
    --i-sequences rep-seqs-trimmed.qza \
    --o-alignment aligned-rep-seqs-trimmed.qza \
    --o-masked-alignment masked-aligned-rep-seqs-trimmed.qza \
    --o-tree unrooted-tree-trimmed.qza \
    --o-rooted-tree rooted-tree-trimmed.qza 
#For the diversity metrics that rely on phylogeny ie. UniFrac, maaft performs a multiple alignment
    
```

    [32mSaved FeatureData[AlignedSequence] to: aligned-rep-seqs-trimmed.qza[0m
    [32mSaved FeatureData[AlignedSequence] to: masked-aligned-rep-seqs-trimmed.qza[0m
    [32mSaved Phylogeny[Unrooted] to: unrooted-tree-trimmed.qza[0m
    [32mSaved Phylogeny[Rooted] to: rooted-tree-trimmed.qza[0m



```bash
qiime diversity core-metrics-phylogenetic \
--i-phylogeny rooted-tree-trimmed.qza \
--i-table table-f2.qza \
--p-sampling-depth 39900 \
--m-metadata-file /Users/anshulsinha/Desktop/Sequencing_analyses/16S_ali_experiment_2018_cross_infect/fastq/rainin_metadata_ali_2018.txt \
  --o-rarefied-table rarefied-table-trimmed.qza \
  --o-faith-pd-vector faith-pd-trimmed.qza \
  --o-observed-features-vector observed-otus-trimmed.qza \
  --o-shannon-vector shannon-vector-trimmed.qza \
  --o-evenness-vector evenness-vector-trimmed.qza \
  --o-unweighted-unifrac-distance-matrix unweighted-unifrac-distance-matrix-trimmed.qza \
  --o-weighted-unifrac-distance-matrix weighted-unifrac-distance-matrix-trimmed.qza \
  --o-jaccard-distance-matrix jaccard-distance-matrix-trimmed.qza \
  --o-bray-curtis-distance-matrix bray-curtis-distance-matrix-trimmed.qza \
  --o-unweighted-unifrac-pcoa-results unweighted-unifrac-pca-results-trimmed.qza \
  --o-weighted-unifrac-pcoa-results weighted-unifrac-pcoa-results-trimmed.qza \
  --o-jaccard-pcoa-results jaccard-pcoa-results-trimmed-trimmed.qza \
  --o-bray-curtis-pcoa-results trimmed-bray-curtis-pcoa-results-trimmed.qza \
  --o-unweighted-unifrac-emperor unweighted-unifrac-emperor-trimmed.qzv \
  --o-weighted-unifrac-emperor weighted-unifrac-emperor-trimmed.qzv \
  --o-jaccard-emperor jaccard-emperor-trimmed.qzv \
  --o-bray-curtis-emperor bray-curtis-emperor-trimmed.qzv
  #Diversity analyses including ALL samples
```

    [32mSaved FeatureTable[Frequency] to: rarefied-table-trimmed.qza[0m
    [32mSaved SampleData[AlphaDiversity] to: faith-pd-trimmed.qza[0m
    [32mSaved SampleData[AlphaDiversity] to: observed-otus-trimmed.qza[0m
    [32mSaved SampleData[AlphaDiversity] to: shannon-vector-trimmed.qza[0m
    [32mSaved SampleData[AlphaDiversity] to: evenness-vector-trimmed.qza[0m
    [32mSaved DistanceMatrix to: unweighted-unifrac-distance-matrix-trimmed.qza[0m
    [32mSaved DistanceMatrix to: weighted-unifrac-distance-matrix-trimmed.qza[0m
    [32mSaved DistanceMatrix to: jaccard-distance-matrix-trimmed.qza[0m
    [32mSaved DistanceMatrix to: bray-curtis-distance-matrix-trimmed.qza[0m
    [32mSaved PCoAResults to: unweighted-unifrac-pca-results-trimmed.qza[0m
    [32mSaved PCoAResults to: weighted-unifrac-pcoa-results-trimmed.qza[0m
    [32mSaved PCoAResults to: jaccard-pcoa-results-trimmed-trimmed.qza[0m
    [32mSaved PCoAResults to: trimmed-bray-curtis-pcoa-results-trimmed.qza[0m
    [32mSaved Visualization to: unweighted-unifrac-emperor-trimmed.qzv[0m
    [32mSaved Visualization to: weighted-unifrac-emperor-trimmed.qzv[0m
    [32mSaved Visualization to: jaccard-emperor-trimmed.qzv[0m
    [32mSaved Visualization to: bray-curtis-emperor-trimmed.qzv[0m



```bash
qiime diversity beta-group-significance \
--i-distance-matrix  weighted-unifrac-emperor-trimmed.qzv \
--m-metadata-file  /Users/anshulsinha/Desktop/Sequencing_analyses/16S_ali_experiment_2018_cross_infect/fastq/rainin_metadata_ali_2018.txt \
--m-metadata-column bac_treatment \
--o-visualization wunifracbac-treatment-filtered-betasig-trimmed.qzv \
--p-pairwise
#PERMANOVA including all samples (unifrac)
```

    [32mSaved Visualization to: wunifracbac-treatment-filtered-betasig-trimmed.qzv[0m



```bash
qiime diversity beta-group-significance \
--i-distance-matrix bray-curtis-distance-matrix-trimmed.qza \
--m-metadata-file  /Users/anshulsinha/Desktop/Sequencing_analyses/16S_ali_experiment_2018_cross_infect/fastq/rainin_metadata_ali_2018.txt \
--m-metadata-column bac_treatment \
--o-visualization bcbactreat-treatment-filtered-betasig-trimmed.qzv 
#PERMANOVA including all samples (bray-curtis)
```

    [32mSaved Visualization to: bcbactreat-treatment-filtered-betasig-trimmed.qzv[0m



```bash
qiime diversity alpha-group-significance \
--i-alpha-diversity shannon-vector-trimmed.qza \
--m-metadata-file /Users/anshulsinha/Desktop/Sequencing_analyses/16S_ali_experiment_2018_cross_infect/fastq/rainin_metadata_ali_2018.txt \
--o-visualization shannon-bac-treatment-filtered-betasig-trimmed.qzv 

#Shannon diversity comparison between groups
```

    [32mSaved Visualization to: shannon-bac-treatment-filtered-betasig-trimmed.qzv[0m



```bash
qiime diversity core-metrics-phylogenetic \
--i-phylogeny rooted-tree-trimmed.qza \
--i-table UCB-filtered-table.qza \
--p-sampling-depth 39900 \
--m-metadata-file /Users/anshulsinha/Desktop/Sequencing_analyses/16S_ali_experiment_2018_cross_infect/fastq/rainin_metadata_ali_2018.txt \
  --o-rarefied-table UCBrarefied-table-trimmed.qza \
  --o-faith-pd-vector UCBfaith-pd-trimmed.qza \
  --o-observed-features-vector UCBobserved-otus-trimmed.qza \
  --o-shannon-vector UCBshannon-vector-trimmed.qza \
  --o-evenness-vector UCBevenness-vector-trimmed.qza \
  --o-unweighted-unifrac-distance-matrix UCBunweighted-unifrac-distance-matrix-trimmed.qza \
  --o-weighted-unifrac-distance-matrix UCBweighted-unifrac-distance-matrix-trimmed.qza \
  --o-jaccard-distance-matrix UCBjaccard-distance-matrix-trimmed.qza \
  --o-bray-curtis-distance-matrix UCBbray-curtis-distance-matrix-trimmed.qza \
  --o-unweighted-unifrac-pcoa-results UCBunweighted-unifrac-pca-results-trimmed.qza \
  --o-weighted-unifrac-pcoa-results UCBweighted-unifrac-pcoa-results-trimmed.qza \
  --o-jaccard-pcoa-results UCBjaccard-pcoa-results-trimmed-trimmed.qza \
  --o-bray-curtis-pcoa-results UCBtrimmed-bray-curtis-pcoa-results-trimmed.qza \
  --o-unweighted-unifrac-emperor UCBunweighted-unifrac-emperor-trimmed.qzv \
  --o-weighted-unifrac-emperor UCBweighted-unifrac-emperor-trimmed.qzv \
  --o-jaccard-emperor UCBjaccard-emperor-trimmed.qzv \
  --o-bray-curtis-emperor UCBbray-curtis-emperor-trimmed.qzv
  #Diversity analyses on UC bacterial group
```

    [32mSaved FeatureTable[Frequency] to: UCBrarefied-table-trimmed.qza[0m
    [32mSaved SampleData[AlphaDiversity] to: UCBfaith-pd-trimmed.qza[0m
    [32mSaved SampleData[AlphaDiversity] to: UCBobserved-otus-trimmed.qza[0m
    [32mSaved SampleData[AlphaDiversity] to: UCBshannon-vector-trimmed.qza[0m
    [32mSaved SampleData[AlphaDiversity] to: UCBevenness-vector-trimmed.qza[0m
    [32mSaved DistanceMatrix to: UCBunweighted-unifrac-distance-matrix-trimmed.qza[0m
    [32mSaved DistanceMatrix to: UCBweighted-unifrac-distance-matrix-trimmed.qza[0m
    [32mSaved DistanceMatrix to: UCBjaccard-distance-matrix-trimmed.qza[0m
    [32mSaved DistanceMatrix to: UCBbray-curtis-distance-matrix-trimmed.qza[0m
    [32mSaved PCoAResults to: UCBunweighted-unifrac-pca-results-trimmed.qza[0m
    [32mSaved PCoAResults to: UCBweighted-unifrac-pcoa-results-trimmed.qza[0m
    [32mSaved PCoAResults to: UCBjaccard-pcoa-results-trimmed-trimmed.qza[0m
    [32mSaved PCoAResults to: UCBtrimmed-bray-curtis-pcoa-results-trimmed.qza[0m
    [32mSaved Visualization to: UCBunweighted-unifrac-emperor-trimmed.qzv[0m
    [32mSaved Visualization to: UCBweighted-unifrac-emperor-trimmed.qzv[0m
    [32mSaved Visualization to: UCBjaccard-emperor-trimmed.qzv[0m
    [32mSaved Visualization to: UCBbray-curtis-emperor-trimmed.qzv[0m



```bash
qiime diversity beta-group-significance \
--i-distance-matrix  UCBweighted-unifrac-distance-matrix-trimmed.qza \
--m-metadata-file  /Users/anshulsinha/Desktop/Sequencing_analyses/16S_ali_experiment_2018_cross_infect/fastq/rainin_metadata_ali_2018.txt \
--m-metadata-column Period \
--o-visualization wunifracUCB-time-treatment-filtered-betasig-trimmed.qzv \
--p-pairwise
#PERMANOVA- UC bacteria over time (unifrac)
```

    [32mSaved Visualization to: wunifracUCB-time-treatment-filtered-betasig-trimmed.qzv[0m



```bash
qiime diversity beta-group-significance \
--i-distance-matrix  UCBbray-curtis-distance-matrix-trimmed.qza \
--m-metadata-file  /Users/anshulsinha/Desktop/Sequencing_analyses/16S_ali_experiment_2018_cross_infect/fastq/rainin_metadata_ali_2018.txt \
--m-metadata-column Period \
--o-visualization bcUCB-time-treatment-filtered-betasig-trimmed.qzv \
--p-pairwise
#PERMANOVA- UC bacteria over time (bray-curtis)
```

    [32mSaved Visualization to: bcUCB-time-treatment-filtered-betasig-trimmed.qzv[0m



```bash
qiime diversity alpha-group-significance \
--i-alpha-diversity UCBshannon-vector-trimmed.qza \
--m-metadata-file /Users/anshulsinha/Desktop/Sequencing_analyses/16S_ali_experiment_2018_cross_infect/fastq/rainin_metadata_ali_2018.txt \
--o-visualization ucbshannon--treatment-filtered-betasig-trimmed.qzv 

#shannon diversity- UC bacteria over time (bray-curtis)

```

    [32mSaved Visualization to: ucbshannon--treatment-filtered-betasig-trimmed.qzv[0m



```bash
qiime tools view ucbshannon--treatment-filtered-betasig-trimmed.qzv 
```


```bash
qiime diversity core-metrics-phylogenetic \
--i-phylogeny rooted-tree-trimmed.qza \
--i-table HB-filtered-table.qza \
--p-sampling-depth 39900 \
--m-metadata-file /Users/anshulsinha/Desktop/Sequencing_analyses/16S_ali_experiment_2018_cross_infect/fastq/rainin_metadata_ali_2018.txt \
  --o-rarefied-table HBrarefied-table-trimmed.qza \
  --o-faith-pd-vector HBfaith-pd-trimmed.qza \
  --o-observed-features-vector HBobserved-otus-trimmed.qza \
  --o-shannon-vector HBshannon-vector-trimmed.qza \
  --o-evenness-vector HBevenness-vector-trimmed.qza \
  --o-unweighted-unifrac-distance-matrix HBunweighted-unifrac-distance-matrix-trimmed.qza \
  --o-weighted-unifrac-distance-matrix HBweighted-unifrac-distance-matrix-trimmed.qza \
  --o-jaccard-distance-matrix HBjaccard-distance-matrix-trimmed.qza \
  --o-bray-curtis-distance-matrix HBbray-curtis-distance-matrix-trimmed.qza \
  --o-unweighted-unifrac-pcoa-results HBunweighted-unifrac-pca-results-trimmed.qza \
  --o-weighted-unifrac-pcoa-results HBweighted-unifrac-pcoa-results-trimmed.qza \
  --o-jaccard-pcoa-results HBjaccard-pcoa-results-trimmed-trimmed.qza \
  --o-bray-curtis-pcoa-results HBtrimmed-bray-curtis-pcoa-results-trimmed.qza \
  --o-unweighted-unifrac-emperor HBunweighted-unifrac-emperor-trimmed.qzv \
  --o-weighted-unifrac-emperor HBweighted-unifrac-emperor-trimmed.qzv \
  --o-jaccard-emperor HBjaccard-emperor-trimmed.qzv \
  --o-bray-curtis-emperor HBbray-curtis-emperor-trimmed.qzv
  #diversity analyses on healthy bacteria 
```

    [32mSaved FeatureTable[Frequency] to: HBrarefied-table-trimmed.qza[0m
    [32mSaved SampleData[AlphaDiversity] to: HBfaith-pd-trimmed.qza[0m
    [32mSaved SampleData[AlphaDiversity] to: HBobserved-otus-trimmed.qza[0m
    [32mSaved SampleData[AlphaDiversity] to: HBshannon-vector-trimmed.qza[0m
    [32mSaved SampleData[AlphaDiversity] to: HBevenness-vector-trimmed.qza[0m
    [32mSaved DistanceMatrix to: HBunweighted-unifrac-distance-matrix-trimmed.qza[0m
    [32mSaved DistanceMatrix to: HBweighted-unifrac-distance-matrix-trimmed.qza[0m
    [32mSaved DistanceMatrix to: HBjaccard-distance-matrix-trimmed.qza[0m
    [32mSaved DistanceMatrix to: HBbray-curtis-distance-matrix-trimmed.qza[0m
    [32mSaved PCoAResults to: HBunweighted-unifrac-pca-results-trimmed.qza[0m
    [32mSaved PCoAResults to: HBweighted-unifrac-pcoa-results-trimmed.qza[0m
    [32mSaved PCoAResults to: HBjaccard-pcoa-results-trimmed-trimmed.qza[0m
    [32mSaved PCoAResults to: HBtrimmed-bray-curtis-pcoa-results-trimmed.qza[0m
    [32mSaved Visualization to: HBunweighted-unifrac-emperor-trimmed.qzv[0m
    [32mSaved Visualization to: HBweighted-unifrac-emperor-trimmed.qzv[0m
    [32mSaved Visualization to: HBjaccard-emperor-trimmed.qzv[0m
    [32mSaved Visualization to: HBbray-curtis-emperor-trimmed.qzv[0m



```bash
qiime tools view HBweighted-unifrac-emperor-trimmed.qzv
```

    Press the 'q' key, Control-C, or Control-D to quit. This view may no longer be accessible or work correctly after quitting.


```bash
qiime diversity beta-group-significance \
--i-distance-matrix  HBweighted-unifrac-distance-matrix-trimmed.qza \
--m-metadata-file  /Users/anshulsinha/Desktop/Sequencing_analyses/16S_ali_experiment_2018_cross_infect/fastq/rainin_metadata_ali_2018.txt \
--m-metadata-column Period \
--o-visualization wunifracHB-time-treatment-filtered-betasig-trimmed.qzv \
--p-pairwise
#weighted unifrac - healthy bacteria over time 
```

    [32mSaved Visualization to: wunifracHB-time-treatment-filtered-betasig-trimmed.qzv[0m



```bash
qiime diversity beta-group-significance \
--i-distance-matrix HBbray-curtis-distance-matrix-trimmed.qza \
--m-metadata-file  /Users/anshulsinha/Desktop/Sequencing_analyses/16S_ali_experiment_2018_cross_infect/fastq/rainin_metadata_ali_2018.txt \
--m-metadata-column Period \
--o-visualization bcHB-time-treatment-filtered-betasig-trimmed.qzv \
--p-pairwise
#bray-curtis - healthy bacteria over time
```

    [32mSaved Visualization to: bcHB-time-treatment-filtered-betasig-trimmed.qzv[0m



```bash
qiime diversity alpha-group-significance \
--i-alpha-diversity HBshannon-vector-trimmed.qza \
--m-metadata-file /Users/anshulsinha/Desktop/Sequencing_analyses/16S_ali_experiment_2018_cross_infect/fastq/rainin_metadata_ali_2018.txt \
--o-visualization  hbshannon--treatment-filtered-betasig-trimmed.qzv
#Shannon diversity - healthy bacteria
```

    [32mSaved Visualization to: hbshannon--treatment-filtered-betasig-trimmed.qzv[0m



```bash
qiime tools view   hbshannon--treatment-filtered-betasig-trimmed.qzv
```

    Press the 'q' key, Control-C, or Control-D to quit. This view may no longer be accessible or work correctly after quitting.


```bash
qiime diversity core-metrics-phylogenetic \
--i-phylogeny rooted-tree-trimmed.qza \
--i-table UCB_HP-filtered-table.qza \
--p-sampling-depth 39900 \
--m-metadata-file /Users/anshulsinha/Desktop/Sequencing_analyses/16S_ali_experiment_2018_cross_infect/fastq/rainin_metadata_ali_2018.txt \
  --o-rarefied-table UCBHPrarefied-table-trimmed.qza \
  --o-faith-pd-vector UCBHPfaith-pd-trimmed.qza \
  --o-observed-features-vector UCBHPobserved-otus-trimmed.qza \
  --o-shannon-vector UCBHPshannon-vector-trimmed.qza \
  --o-evenness-vector UCBHPevenness-vector-trimmed.qza \
  --o-unweighted-unifrac-distance-matrix UCBHPunweighted-unifrac-distance-matrix-trimmed.qza \
  --o-weighted-unifrac-distance-matrix UCBHPweighted-unifrac-distance-matrix-trimmed.qza \
  --o-jaccard-distance-matrix UCBHPjaccard-distance-matrix-trimmed.qza \
  --o-bray-curtis-distance-matrix UCBHPbray-curtis-distance-matrix-trimmed.qza \
  --o-unweighted-unifrac-pcoa-results UCBHPunweighted-unifrac-pca-results-trimmed.qza \
  --o-weighted-unifrac-pcoa-results UCBHPweighted-unifrac-pcoa-results-trimmed.qza \
  --o-jaccard-pcoa-results UCBHPjaccard-pcoa-results-trimmed-trimmed.qza \
  --o-bray-curtis-pcoa-results UCBHPtrimmed-bray-curtis-pcoa-results-trimmed.qza \
  --o-unweighted-unifrac-emperor UCBHPunweighted-unifrac-emperor-trimmed.qzv \
  --o-weighted-unifrac-emperor UCBHPweighted-unifrac-emperor-trimmed.qzv \
  --o-jaccard-emperor UCBHPjaccard-emperor-trimmed.qzv \
  --o-bray-curtis-emperor UCBHPbray-curtis-emperor-trimmed.qzv
  #UC bac + healthy phage treatment diversity analyses
```

    [32mSaved FeatureTable[Frequency] to: UCBHPrarefied-table-trimmed.qza[0m
    [32mSaved SampleData[AlphaDiversity] to: UCBHPfaith-pd-trimmed.qza[0m
    [32mSaved SampleData[AlphaDiversity] to: UCBHPobserved-otus-trimmed.qza[0m
    [32mSaved SampleData[AlphaDiversity] to: UCBHPshannon-vector-trimmed.qza[0m
    [32mSaved SampleData[AlphaDiversity] to: UCBHPevenness-vector-trimmed.qza[0m
    [32mSaved DistanceMatrix to: UCBHPunweighted-unifrac-distance-matrix-trimmed.qza[0m
    [32mSaved DistanceMatrix to: UCBHPweighted-unifrac-distance-matrix-trimmed.qza[0m
    [32mSaved DistanceMatrix to: UCBHPjaccard-distance-matrix-trimmed.qza[0m
    [32mSaved DistanceMatrix to: UCBHPbray-curtis-distance-matrix-trimmed.qza[0m
    [32mSaved PCoAResults to: UCBHPunweighted-unifrac-pca-results-trimmed.qza[0m
    [32mSaved PCoAResults to: UCBHPweighted-unifrac-pcoa-results-trimmed.qza[0m
    [32mSaved PCoAResults to: UCBHPjaccard-pcoa-results-trimmed-trimmed.qza[0m
    [32mSaved PCoAResults to: UCBHPtrimmed-bray-curtis-pcoa-results-trimmed.qza[0m
    [32mSaved Visualization to: UCBHPunweighted-unifrac-emperor-trimmed.qzv[0m
    [32mSaved Visualization to: UCBHPweighted-unifrac-emperor-trimmed.qzv[0m
    [32mSaved Visualization to: UCBHPjaccard-emperor-trimmed.qzv[0m
    [32mSaved Visualization to: UCBHPbray-curtis-emperor-trimmed.qzv[0m



```bash
qiime diversity beta-group-significance \
--i-distance-matrix  UCBHPweighted-unifrac-distance-matrix-trimmed.qza  \
--m-metadata-file  /Users/anshulsinha/Desktop/Sequencing_analyses/16S_ali_experiment_2018_cross_infect/fastq/rainin_metadata_ali_2018.txt \
--m-metadata-column Period \
--o-visualization wunifracbacUCBHP-time-filtered-betasig-trimmed.qzv \
--p-pairwise
```

    [32mSaved Visualization to: wunifracbacUCBHP-time-filtered-betasig-trimmed.qzv[0m



```bash
qiime diversity beta-group-significance \
--i-distance-matrix  UCBHPbray-curtis-distance-matrix-trimmed.qza  \
--m-metadata-file  /Users/anshulsinha/Desktop/Sequencing_analyses/16S_ali_experiment_2018_cross_infect/fastq/rainin_metadata_ali_2018.txt \
--m-metadata-column Period \
--o-visualization bcUCBHP-time-filtered-betasig-trimmed.qzv \
--p-pairwise
```

    [32mSaved Visualization to: bcUCBHP-time-filtered-betasig-trimmed.qzv[0m



```bash
qiime diversity core-metrics-phylogenetic \
--i-phylogeny rooted-tree-trimmed.qza \
--i-table HB_UCP-filtered-table.qza \
--p-sampling-depth 39900 \
--m-metadata-file /Users/anshulsinha/Desktop/Sequencing_analyses/16S_ali_experiment_2018_cross_infect/fastq/rainin_metadata_ali_2018.txt \
  --o-rarefied-table HB_UCPrarefied-table-trimmed.qza \
  --o-faith-pd-vector HB_UCPPfaith-pd-trimmed.qza \
  --o-observed-features-vector HB_UCPobserved-otus-trimmed.qza \
  --o-shannon-vector HB_UCPshannon-vector-trimmed.qza \
  --o-evenness-vector HB_UCPevenness-vector-trimmed.qza \
  --o-unweighted-unifrac-distance-matrix HB_UCPunweighted-unifrac-distance-matrix-trimmed.qza \
  --o-weighted-unifrac-distance-matrix HB_UCPweighted-unifrac-distance-matrix-trimmed.qza \
  --o-jaccard-distance-matrix HB_UCPjaccard-distance-matrix-trimmed.qza \
  --o-bray-curtis-distance-matrix HB_UCPbray-curtis-distance-matrix-trimmed.qza \
  --o-unweighted-unifrac-pcoa-results HB_UCPunweighted-unifrac-pca-results-trimmed.qza \
  --o-weighted-unifrac-pcoa-results HB_UCPweighted-unifrac-pcoa-results-trimmed.qza \
  --o-jaccard-pcoa-results HB_UCPjaccard-pcoa-results-trimmed-trimmed.qza \
  --o-bray-curtis-pcoa-results HB_UCPtrimmed-bray-curtis-pcoa-results-trimmed.qza \
  --o-unweighted-unifrac-emperor HB_UCPunweighted-unifrac-emperor-trimmed.qzv \
  --o-weighted-unifrac-emperor HB_UCPweighted-unifrac-emperor-trimmed.qzv \
  --o-jaccard-emperor HB_UCPjaccard-emperor-trimmed.qzv \
  --o-bray-curtis-emperor HB_UCPbray-curtis-emperor-trimmed.qzv
    #healthy bac + UC phage treatment diversity analyses
```

    [32mSaved FeatureTable[Frequency] to: HB_UCPrarefied-table-trimmed.qza[0m
    [32mSaved SampleData[AlphaDiversity] to: HB_UCPPfaith-pd-trimmed.qza[0m
    [32mSaved SampleData[AlphaDiversity] to: HB_UCPobserved-otus-trimmed.qza[0m
    [32mSaved SampleData[AlphaDiversity] to: HB_UCPshannon-vector-trimmed.qza[0m
    [32mSaved SampleData[AlphaDiversity] to: HB_UCPevenness-vector-trimmed.qza[0m
    [32mSaved DistanceMatrix to: HB_UCPunweighted-unifrac-distance-matrix-trimmed.qza[0m
    [32mSaved DistanceMatrix to: HB_UCPweighted-unifrac-distance-matrix-trimmed.qza[0m
    [32mSaved DistanceMatrix to: HB_UCPjaccard-distance-matrix-trimmed.qza[0m
    [32mSaved DistanceMatrix to: HB_UCPbray-curtis-distance-matrix-trimmed.qza[0m
    [32mSaved PCoAResults to: HB_UCPunweighted-unifrac-pca-results-trimmed.qza[0m
    [32mSaved PCoAResults to: HB_UCPweighted-unifrac-pcoa-results-trimmed.qza[0m
    [32mSaved PCoAResults to: HB_UCPjaccard-pcoa-results-trimmed-trimmed.qza[0m
    [32mSaved PCoAResults to: HB_UCPtrimmed-bray-curtis-pcoa-results-trimmed.qza[0m
    [32mSaved Visualization to: HB_UCPunweighted-unifrac-emperor-trimmed.qzv[0m
    [32mSaved Visualization to: HB_UCPweighted-unifrac-emperor-trimmed.qzv[0m
    [32mSaved Visualization to: HB_UCPjaccard-emperor-trimmed.qzv[0m
    [32mSaved Visualization to: HB_UCPbray-curtis-emperor-trimmed.qzv[0m



```bash
qiime diversity beta-group-significance \
--i-distance-matrix HB_UCPweighted-unifrac-distance-matrix-trimmed.qza  \
--m-metadata-file  /Users/anshulsinha/Desktop/Sequencing_analyses/16S_ali_experiment_2018_cross_infect/fastq/rainin_metadata_ali_2018.txt \
--m-metadata-column Period \
--o-visualization wunifracbacHBUCP-time-filtered-betasig-trimmed.qzv \
--p-pairwise
```

    [32mSaved Visualization to: wunifracbacHBUCP-time-filtered-betasig-trimmed.qzv[0m



```bash
qiime diversity beta-group-significance \
--i-distance-matrix  HB_UCPweighted-unifrac-distance-matrix-trimmed.qza \
--m-metadata-file  /Users/anshulsinha/Desktop/Sequencing_analyses/16S_ali_experiment_2018_cross_infect/fastq/rainin_metadata_ali_2018.txt \
--m-metadata-column Period \
--o-visualization bcHBUCP-time-filtered-betasig-trimmed.qzv \
--p-pairwise
```

    [32mSaved Visualization to: bcHBUCP-time-filtered-betasig-trimmed.qzv[0m



```bash
qiime diversity core-metrics-phylogenetic \
--i-phylogeny rooted-tree-trimmed.qza \
--i-table UCB-UCP-table.qza \
--p-sampling-depth 39900 \
--m-metadata-file /Users/anshulsinha/Desktop/Sequencing_analyses/16S_ali_experiment_2018_cross_infect/fastq/rainin_metadata_ali_2018.txt \
  --o-rarefied-table UCB_UCPrarefied-table-trimmed.qza \
  --o-faith-pd-vector UCB_UCPfaith-pd-trimmed.qza \
  --o-observed-features-vector UCB_UCPobserved-otus-trimmed.qza \
  --o-shannon-vector UCB_UCPshannon-vector-trimmed.qza \
  --o-evenness-vector UCB_UCPevenness-vector-trimmed.qza \
  --o-unweighted-unifrac-distance-matrix UCB_UCPunweighted-unifrac-distance-matrix-trimmed.qza \
  --o-weighted-unifrac-distance-matrix UCB_UCPweighted-unifrac-distance-matrix-trimmed.qza \
  --o-jaccard-distance-matrix UCB_UCPjaccard-distance-matrix-trimmed.qza \
  --o-bray-curtis-distance-matrix UCB_UCPbray-curtis-distance-matrix-trimmed.qza \
  --o-unweighted-unifrac-pcoa-results UCB_UCPunweighted-unifrac-pca-results-trimmed.qza \
  --o-weighted-unifrac-pcoa-results UCB_UCPweighted-unifrac-pcoa-results-trimmed.qza \
  --o-jaccard-pcoa-results UCB_UCPjaccard-pcoa-results-trimmed-trimmed.qza \
  --o-bray-curtis-pcoa-results UCB_UCPtrimmed-bray-curtis-pcoa-results-trimmed.qza \
  --o-unweighted-unifrac-emperor UCB_UCPunweighted-unifrac-emperor-trimmed.qzv \
  --o-weighted-unifrac-emperor UCB_UCPweighted-unifrac-emperor-trimmed.qzv \
  --o-jaccard-emperor UCB_UCPjaccard-emperor-trimmed.qzv \
  --o-bray-curtis-emperor UCB_UCPbray-curtis-emperor-trimmed.qzv
      #UC bac + UC phage treatment diversity analyses
```

    [32mSaved FeatureTable[Frequency] to: UCB_UCPrarefied-table-trimmed.qza[0m
    [32mSaved SampleData[AlphaDiversity] to: UCB_UCPfaith-pd-trimmed.qza[0m
    [32mSaved SampleData[AlphaDiversity] to: UCB_UCPobserved-otus-trimmed.qza[0m
    [32mSaved SampleData[AlphaDiversity] to: UCB_UCPshannon-vector-trimmed.qza[0m
    [32mSaved SampleData[AlphaDiversity] to: UCB_UCPevenness-vector-trimmed.qza[0m
    [32mSaved DistanceMatrix to: UCB_UCPunweighted-unifrac-distance-matrix-trimmed.qza[0m
    [32mSaved DistanceMatrix to: UCB_UCPweighted-unifrac-distance-matrix-trimmed.qza[0m
    [32mSaved DistanceMatrix to: UCB_UCPjaccard-distance-matrix-trimmed.qza[0m
    [32mSaved DistanceMatrix to: UCB_UCPbray-curtis-distance-matrix-trimmed.qza[0m
    [32mSaved PCoAResults to: UCB_UCPunweighted-unifrac-pca-results-trimmed.qza[0m
    [32mSaved PCoAResults to: UCB_UCPweighted-unifrac-pcoa-results-trimmed.qza[0m
    [32mSaved PCoAResults to: UCB_UCPjaccard-pcoa-results-trimmed-trimmed.qza[0m
    [32mSaved PCoAResults to: UCB_UCPtrimmed-bray-curtis-pcoa-results-trimmed.qza[0m
    [32mSaved Visualization to: UCB_UCPunweighted-unifrac-emperor-trimmed.qzv[0m
    [32mSaved Visualization to: UCB_UCPweighted-unifrac-emperor-trimmed.qzv[0m
    [32mSaved Visualization to: UCB_UCPjaccard-emperor-trimmed.qzv[0m
    [32mSaved Visualization to: UCB_UCPbray-curtis-emperor-trimmed.qzv[0m



```bash
qiime diversity beta-group-significance \
--i-distance-matrix UCB_UCPweighted-unifrac-distance-matrix-trimmed.qza \
--m-metadata-file  /Users/anshulsinha/Desktop/Sequencing_analyses/16S_ali_experiment_2018_cross_infect/fastq/rainin_metadata_ali_2018.txt \
--m-metadata-column Period \
--o-visualization wunifracbacUCBUCP-time-filtered-betasig-trimmed.qzv \
--p-pairwise
```

    [32mSaved Visualization to: wunifracbacUCBUCP-time-filtered-betasig-trimmed.qzv[0m



```bash
qiime diversity beta-group-significance \
--i-distance-matrix UCB_UCPweighted-unifrac-distance-matrix-trimmed.qza \
--m-metadata-file  /Users/anshulsinha/Desktop/Sequencing_analyses/16S_ali_experiment_2018_cross_infect/fastq/rainin_metadata_ali_2018.txt \
--m-metadata-column Period \
--o-visualization bcbacUCBUCP-time-filtered-betasig-trimmed.qzv \
--p-pairwise
```

    [32mSaved Visualization to: bcbacUCBUCP-time-filtered-betasig-trimmed.qzv[0m



```bash
qiime tools view bcbacUCBUCP-time-filtered-betasig-trimmed.qzv 
```

    Press the 'q' key, Control-C, or Control-D to quit. This view may no longer be accessible or work correctly after quitting.


```bash
qiime diversity core-metrics-phylogenetic \
--i-phylogeny rooted-tree-trimmed.qza \
--i-table  HB-HP-table.qza \
--p-sampling-depth 39900 \
--m-metadata-file /Users/anshulsinha/Desktop/Sequencing_analyses/16S_ali_experiment_2018_cross_infect/fastq/rainin_metadata_ali_2018.txt \
  --o-rarefied-table HB_HPrarefied-table-trimmed.qza \
  --o-faith-pd-vector HB_HPfaith-pd-trimmed.qza \
  --o-observed-features-vector HB_HPobserved-otus-trimmed.qza \
  --o-shannon-vector HB_HPshannon-vector-trimmed.qza \
  --o-evenness-vector HB_HPevenness-vector-trimmed.qza \
  --o-unweighted-unifrac-distance-matrix HB_HPunweighted-unifrac-distance-matrix-trimmed.qza \
  --o-weighted-unifrac-distance-matrix HB_HPweighted-unifrac-distance-matrix-trimmed.qza \
  --o-jaccard-distance-matrix HB_HPjaccard-distance-matrix-trimmed.qza \
  --o-bray-curtis-distance-matrix HB_HPbray-curtis-distance-matrix-trimmed.qza \
  --o-unweighted-unifrac-pcoa-results HB_HPunweighted-unifrac-pca-results-trimmed.qza \
  --o-weighted-unifrac-pcoa-results HB_HPweighted-unifrac-pcoa-results-trimmed.qza \
  --o-jaccard-pcoa-results HB_HPjaccard-pcoa-results-trimmed-trimmed.qza \
  --o-bray-curtis-pcoa-results HB_HPtrimmed-bray-curtis-pcoa-results-trimmed.qza \
  --o-unweighted-unifrac-emperor HB_HPunweighted-unifrac-emperor-trimmed.qzv \
  --o-weighted-unifrac-emperor HB_HPweighted-unifrac-emperor-trimmed.qzv \
  --o-jaccard-emperor HB_HPjaccard-emperor-trimmed.qzv \
  --o-bray-curtis-emperor HB_HPbray-curtis-emperor-trimmed.qzv
        #healthy bac + healthy phage treatment diversity analyses
```

    [32mSaved FeatureTable[Frequency] to: HB_HPrarefied-table-trimmed.qza[0m
    [32mSaved SampleData[AlphaDiversity] to: HB_HPfaith-pd-trimmed.qza[0m
    [32mSaved SampleData[AlphaDiversity] to: HB_HPobserved-otus-trimmed.qza[0m
    [32mSaved SampleData[AlphaDiversity] to: HB_HPshannon-vector-trimmed.qza[0m
    [32mSaved SampleData[AlphaDiversity] to: HB_HPevenness-vector-trimmed.qza[0m
    [32mSaved DistanceMatrix to: HB_HPunweighted-unifrac-distance-matrix-trimmed.qza[0m
    [32mSaved DistanceMatrix to: HB_HPweighted-unifrac-distance-matrix-trimmed.qza[0m
    [32mSaved DistanceMatrix to: HB_HPjaccard-distance-matrix-trimmed.qza[0m
    [32mSaved DistanceMatrix to: HB_HPbray-curtis-distance-matrix-trimmed.qza[0m
    [32mSaved PCoAResults to: HB_HPunweighted-unifrac-pca-results-trimmed.qza[0m
    [32mSaved PCoAResults to: HB_HPweighted-unifrac-pcoa-results-trimmed.qza[0m
    [32mSaved PCoAResults to: HB_HPjaccard-pcoa-results-trimmed-trimmed.qza[0m
    [32mSaved PCoAResults to: HB_HPtrimmed-bray-curtis-pcoa-results-trimmed.qza[0m
    [32mSaved Visualization to: HB_HPunweighted-unifrac-emperor-trimmed.qzv[0m
    [32mSaved Visualization to: HB_HPweighted-unifrac-emperor-trimmed.qzv[0m
    [32mSaved Visualization to: HB_HPjaccard-emperor-trimmed.qzv[0m
    [32mSaved Visualization to: HB_HPbray-curtis-emperor-trimmed.qzv[0m



```bash
qiime diversity beta-group-significance \
--i-distance-matrix HB_HPweighted-unifrac-distance-matrix-trimmed.qza \
--m-metadata-file  /Users/anshulsinha/Desktop/Sequencing_analyses/16S_ali_experiment_2018_cross_infect/fastq/rainin_metadata_ali_2018.txt \
--m-metadata-column Period \
--o-visualization wunifracbacHBHP-time-filtered-betasig-trimmed.qzv \
--p-pairwise
```

    [32mSaved Visualization to: wunifracbacHBHP-time-filtered-betasig-trimmed.qzv[0m



```bash
qiime diversity beta-group-significance \
--i-distance-matrix HB_HPbray-curtis-distance-matrix-trimmed.qza \
--m-metadata-file  /Users/anshulsinha/Desktop/Sequencing_analyses/16S_ali_experiment_2018_cross_infect/fastq/rainin_metadata_ali_2018.txt \
--m-metadata-column Period \
--o-visualization bcHBHP-time-filtered-betasig-trimmed.qzv \
--p-pairwise
```

    [32mSaved Visualization to: bcHBHP-time-filtered-betasig-trimmed.qzv[0m



```bash
qiime tools view bcHBHP-time-filtered-betasig-trimmed.qzv
```

    Press the 'q' key, Control-C, or Control-D to quit. This view may no longer be accessible or work correctly after quitting.


```bash
qiime diversity core-metrics-phylogenetic \
--i-phylogeny rooted-tree-trimmed.qza \
--i-table colonization-filtered-table.qza \
--p-sampling-depth 39900 \
--m-metadata-file /Users/anshulsinha/Desktop/Sequencing_analyses/16S_ali_experiment_2018_cross_infect/fastq/rainin_metadata_ali_2018.txt \
  --o-rarefied-table colrarefied-table-trimmed.qza \
  --o-faith-pd-vector colfaith-pd-trimmed.qza \
  --o-observed-features-vector colobserved-otus-trimmed.qza \
  --o-shannon-vector colshannon-vector-trimmed.qza \
  --o-evenness-vector colevenness-vector-trimmed.qza \
  --o-unweighted-unifrac-distance-matrix colunweighted-unifrac-distance-matrix-trimmed.qza \
  --o-weighted-unifrac-distance-matrix colweighted-unifrac-distance-matrix-trimmed.qza \
  --o-jaccard-distance-matrix coljaccard-distance-matrix-trimmed.qza \
  --o-bray-curtis-distance-matrix colbray-curtis-distance-matrix-trimmed.qza \
  --o-unweighted-unifrac-pcoa-results colunweighted-unifrac-pca-results-trimmed.qza \
  --o-weighted-unifrac-pcoa-results colweighted-unifrac-pcoa-results-trimmed.qza \
  --o-jaccard-pcoa-results coljaccard-pcoa-results-trimmed-trimmed.qza \
  --o-bray-curtis-pcoa-results coltrimmed-bray-curtis-pcoa-results-trimmed.qza \
  --o-unweighted-unifrac-emperor colunweighted-unifrac-emperor-trimmed.qzv \
  --o-weighted-unifrac-emperor colweighted-unifrac-emperor-trimmed.qzv \
  --o-jaccard-emperor coljaccard-emperor-trimmed.qzv \
  --o-bray-curtis-emperor colbray-curtis-emperor-trimmed.qzv
  
  #Diversity analyses during bacterial colonization period 
```

    [32mSaved FeatureTable[Frequency] to: colrarefied-table-trimmed.qza[0m
    [32mSaved SampleData[AlphaDiversity] to: colfaith-pd-trimmed.qza[0m
    [32mSaved SampleData[AlphaDiversity] to: colobserved-otus-trimmed.qza[0m
    [32mSaved SampleData[AlphaDiversity] to: colshannon-vector-trimmed.qza[0m
    [32mSaved SampleData[AlphaDiversity] to: colevenness-vector-trimmed.qza[0m
    [32mSaved DistanceMatrix to: colunweighted-unifrac-distance-matrix-trimmed.qza[0m
    [32mSaved DistanceMatrix to: colweighted-unifrac-distance-matrix-trimmed.qza[0m
    [32mSaved DistanceMatrix to: coljaccard-distance-matrix-trimmed.qza[0m
    [32mSaved DistanceMatrix to: colbray-curtis-distance-matrix-trimmed.qza[0m
    [32mSaved PCoAResults to: colunweighted-unifrac-pca-results-trimmed.qza[0m
    [32mSaved PCoAResults to: colweighted-unifrac-pcoa-results-trimmed.qza[0m
    [32mSaved PCoAResults to: coljaccard-pcoa-results-trimmed-trimmed.qza[0m
    [32mSaved PCoAResults to: coltrimmed-bray-curtis-pcoa-results-trimmed.qza[0m
    [32mSaved Visualization to: colunweighted-unifrac-emperor-trimmed.qzv[0m
    [32mSaved Visualization to: colweighted-unifrac-emperor-trimmed.qzv[0m
    [32mSaved Visualization to: coljaccard-emperor-trimmed.qzv[0m
    [32mSaved Visualization to: colbray-curtis-emperor-trimmed.qzv[0m



```bash
qiime diversity beta-group-significance \
--i-distance-matrix colweighted-unifrac-distance-matrix-trimmed.qza \
--m-metadata-file  /Users/anshulsinha/Desktop/Sequencing_analyses/16S_ali_experiment_2018_cross_infect/fastq/rainin_metadata_ali_2018.txt \
--m-metadata-column bac_treatment \
--o-visualization colwunifrac-treatment-filtered-betasig-trimmed.qzv \
--p-pairwise
```

    [32mSaved Visualization to: colwunifrac-treatment-filtered-betasig-trimmed.qzv[0m



```bash
qiime diversity alpha-group-significance \
--i-alpha-diversity colshannon-vector-trimmed.qza \
--m-metadata-file /Users/anshulsinha/Desktop/Sequencing_analyses/16S_ali_experiment_2018_cross_infect/fastq/rainin_metadata_ali_2018.txt \
--o-visualization colshannon--treatment-filtered-betasig-trimmed.qzv 
```

    [32mSaved Visualization to: colshannon--treatment-filtered-betasig-trimmed.qzv[0m



```bash
qiime diversity beta-group-significance \
--i-distance-matrix colbray-curtis-distance-matrix-trimmed.qza \
--m-metadata-file  /Users/anshulsinha/Desktop/Sequencing_analyses/16S_ali_experiment_2018_cross_infect/fastq/rainin_metadata_ali_2018.txt \
--m-metadata-column bac_treatment \
--o-visualization colbcbac-treatment-filtered-betasig-trimmed.qzv \
--p-pairwise
```

    [32mSaved Visualization to: cobcbac-treatment-filtered-betasig-trimmed.qzv[0m



```bash
qiime diversity core-metrics-phylogenetic \
--i-phylogeny rooted-tree-trimmed.qza \
--i-table gav-filtered-table.qza \
--p-sampling-depth 39900 \
--m-metadata-file /Users/anshulsinha/Desktop/Sequencing_analyses/16S_ali_experiment_2018_cross_infect/fastq/rainin_metadata_ali_2018.txt \
  --o-rarefied-table gavrarefied-table-trimmed.qza \
  --o-faith-pd-vector gavfaith-pd-trimmed.qza \
  --o-observed-features-vector gavobserved-otus-trimmed.qza \
  --o-shannon-vector gavshannon-vector-trimmed.qza \
  --o-evenness-vector gavevenness-vector-trimmed.qza \
  --o-unweighted-unifrac-distance-matrix gavunweighted-unifrac-distance-matrix-trimmed.qza \
  --o-weighted-unifrac-distance-matrix gavweighted-unifrac-distance-matrix-trimmed.qza \
  --o-jaccard-distance-matrix gavjaccard-distance-matrix-trimmed.qza \
  --o-bray-curtis-distance-matrix gavbray-curtis-distance-matrix-trimmed.qza \
  --o-unweighted-unifrac-pcoa-results gavunweighted-unifrac-pca-results-trimmed.qza \
  --o-weighted-unifrac-pcoa-results gavweighted-unifrac-pcoa-results-trimmed.qza \
  --o-jaccard-pcoa-results gavjaccard-pcoa-results-trimmed-trimmed.qza \
  --o-bray-curtis-pcoa-results gavtrimmed-bray-curtis-pcoa-results-trimmed.qza \
  --o-unweighted-unifrac-emperor gavunweighted-unifrac-emperor-trimmed.qzv \
  --o-weighted-unifrac-emperor gavweighted-unifrac-emperor-trimmed.qzv \
  --o-jaccard-emperor gavjaccard-emperor-trimmed.qzv \
  --o-bray-curtis-emperor gavbray-curtis-emperor-trimmed.qzv
  #Diversity analyses during phage gavage period 
```

    [32mSaved FeatureTable[Frequency] to: gavrarefied-table-trimmed.qza[0m
    [32mSaved SampleData[AlphaDiversity] to: gavfaith-pd-trimmed.qza[0m
    [32mSaved SampleData[AlphaDiversity] to: gavobserved-otus-trimmed.qza[0m
    [32mSaved SampleData[AlphaDiversity] to: gavshannon-vector-trimmed.qza[0m
    [32mSaved SampleData[AlphaDiversity] to: gavevenness-vector-trimmed.qza[0m
    [32mSaved DistanceMatrix to: gavunweighted-unifrac-distance-matrix-trimmed.qza[0m
    [32mSaved DistanceMatrix to: gavweighted-unifrac-distance-matrix-trimmed.qza[0m
    [32mSaved DistanceMatrix to: gavjaccard-distance-matrix-trimmed.qza[0m
    [32mSaved DistanceMatrix to: gavbray-curtis-distance-matrix-trimmed.qza[0m
    [32mSaved PCoAResults to: gavunweighted-unifrac-pca-results-trimmed.qza[0m
    [32mSaved PCoAResults to: gavweighted-unifrac-pcoa-results-trimmed.qza[0m
    [32mSaved PCoAResults to: gavjaccard-pcoa-results-trimmed-trimmed.qza[0m
    [32mSaved PCoAResults to: gavtrimmed-bray-curtis-pcoa-results-trimmed.qza[0m
    [32mSaved Visualization to: gavunweighted-unifrac-emperor-trimmed.qzv[0m
    [32mSaved Visualization to: gavweighted-unifrac-emperor-trimmed.qzv[0m
    [32mSaved Visualization to: gavjaccard-emperor-trimmed.qzv[0m
    [32mSaved Visualization to: gavbray-curtis-emperor-trimmed.qzv[0m



```bash
qiime diversity alpha-group-significance \
--i-alpha-diversity gavshannon-vector-trimmed.qza \
--m-metadata-file /Users/anshulsinha/Desktop/Sequencing_analyses/16S_ali_experiment_2018_cross_infect/fastq/rainin_metadata_ali_2018.txt \
--o-visualization gavshannon--treatment-filtered-betasig-trimmed.qzv 
```

    [32mSaved Visualization to: gavshannon--treatment-filtered-betasig-trimmed.qzv[0m



```bash
qiime diversity beta-group-significance \
--i-distance-matrix gavweighted-unifrac-distance-matrix-trimmed.qza \
--m-metadata-file  /Users/anshulsinha/Desktop/Sequencing_analyses/16S_ali_experiment_2018_cross_infect/fastq/rainin_metadata_ali_2018.txt \
--m-metadata-column phage_treatment \
--o-visualization gavwunifracphage-treatment-filtered-betasig-trimmed.qzv \
--p-pairwise
```

    [32mSaved Visualization to: gavwunifracphage-treatment-filtered-betasig-trimmed.qzv[0m



```bash
qiime tools view gavwunifracphage-treatment-filtered-betasig-trimmed.qzv
```

    Press the 'q' key, Control-C, or Control-D to quit. This view may no longer be accessible or work correctly after quitting.


```bash
qiime diversity beta-group-significance \
--i-distance-matrix gavbray-curtis-distance-matrix-trimmed.qza \
--m-metadata-file  /Users/anshulsinha/Desktop/Sequencing_analyses/16S_ali_experiment_2018_cross_infect/fastq/rainin_metadata_ali_2018.txt \
--m-metadata-column phage_treatment \
--o-visualization gavbc-treatment-filtered-betasig-trimmed.qzv \
--p-pairwise
```

    [32mSaved Visualization to: gavbc-treatment-filtered-betasig-trimmed.qzv[0m



```bash
qiime diversity beta-group-significance \
--i-distance-matrix gavweighted-unifrac-distance-matrix-trimmed.qza \
--m-metadata-file  /Users/anshulsinha/Desktop/Sequencing_analyses/16S_ali_experiment_2018_cross_infect/fastq/rainin_metadata_ali_2018.txt \
--m-metadata-column bac_treatment \
--o-visualization gavwunifracbac-treatment-filtered-betasig-trimmed.qzv \
--p-pairwise
```

    [32mSaved Visualization to: gavwunifracbac-treatment-filtered-betasig-trimmed.qzv[0m



```bash
qiime diversity beta-group-significance \
--i-distance-matrix gavbray-curtis-distance-matrix-trimmed.qza \
--m-metadata-file  /Users/anshulsinha/Desktop/Sequencing_analyses/16S_ali_experiment_2018_cross_infect/fastq/rainin_metadata_ali_2018.txt \
--m-metadata-column bac_treatment \
--o-visualization gavwbcbac-treatment-filtered-betasig-trimmed.qzv \
--p-pairwise
```

    [32mSaved Visualization to: gavwbcbac-treatment-filtered-betasig-trimmed.qzv[0m



```bash
qiime diversity core-metrics-phylogenetic \
--i-phylogeny rooted-tree-trimmed.qza \
--i-table dss-filtered-table.qza \
--p-sampling-depth 39900 \
--m-metadata-file /Users/anshulsinha/Desktop/Sequencing_analyses/16S_ali_experiment_2018_cross_infect/fastq/rainin_metadata_ali_2018.txt \
  --o-rarefied-table dssrarefied-table-trimmed.qza \
  --o-faith-pd-vector dssfaith-pd-trimmed.qza \
  --o-observed-features-vector dssobserved-otus-trimmed.qza \
  --o-shannon-vector dssshannon-vector-trimmed.qza \
  --o-evenness-vector dssevenness-vector-trimmed.qza \
  --o-unweighted-unifrac-distance-matrix dssunweighted-unifrac-distance-matrix-trimmed.qza \
  --o-weighted-unifrac-distance-matrix dssweighted-unifrac-distance-matrix-trimmed.qza \
  --o-jaccard-distance-matrix dssjaccard-distance-matrix-trimmed.qza \
  --o-bray-curtis-distance-matrix dssbray-curtis-distance-matrix-trimmed.qza \
  --o-unweighted-unifrac-pcoa-results dssunweighted-unifrac-pca-results-trimmed.qza \
  --o-weighted-unifrac-pcoa-results dssweighted-unifrac-pcoa-results-trimmed.qza \
  --o-jaccard-pcoa-results dssjaccard-pcoa-results-trimmed-trimmed.qza \
  --o-bray-curtis-pcoa-results dsstrimmed-bray-curtis-pcoa-results-trimmed.qza \
  --o-unweighted-unifrac-emperor dssunweighted-unifrac-emperor-trimmed.qzv \
  --o-weighted-unifrac-emperor dssweighted-unifrac-emperor-trimmed.qzv \
  --o-jaccard-emperor dssjaccard-emperor-trimmed.qzv \
  --o-bray-curtis-emperor dssbray-curtis-emperor-trimmed.qzv

  #Diversity analyses during dss /washout period 
```

    [32mSaved FeatureTable[Frequency] to: dssrarefied-table-trimmed.qza[0m
    [32mSaved SampleData[AlphaDiversity] to: dssfaith-pd-trimmed.qza[0m
    [32mSaved SampleData[AlphaDiversity] to: dssobserved-otus-trimmed.qza[0m
    [32mSaved SampleData[AlphaDiversity] to: dssshannon-vector-trimmed.qza[0m
    [32mSaved SampleData[AlphaDiversity] to: dssevenness-vector-trimmed.qza[0m
    [32mSaved DistanceMatrix to: dssunweighted-unifrac-distance-matrix-trimmed.qza[0m
    [32mSaved DistanceMatrix to: dssweighted-unifrac-distance-matrix-trimmed.qza[0m
    [32mSaved DistanceMatrix to: dssjaccard-distance-matrix-trimmed.qza[0m
    [32mSaved DistanceMatrix to: dssbray-curtis-distance-matrix-trimmed.qza[0m
    [32mSaved PCoAResults to: dssunweighted-unifrac-pca-results-trimmed.qza[0m
    [32mSaved PCoAResults to: dssweighted-unifrac-pcoa-results-trimmed.qza[0m
    [32mSaved PCoAResults to: dssjaccard-pcoa-results-trimmed-trimmed.qza[0m
    [32mSaved PCoAResults to: dsstrimmed-bray-curtis-pcoa-results-trimmed.qza[0m
    [32mSaved Visualization to: dssunweighted-unifrac-emperor-trimmed.qzv[0m
    [32mSaved Visualization to: dssweighted-unifrac-emperor-trimmed.qzv[0m
    [32mSaved Visualization to: dssjaccard-emperor-trimmed.qzv[0m
    [32mSaved Visualization to: dssbray-curtis-emperor-trimmed.qzv[0m



```bash
qiime diversity beta-group-significance \
--i-distance-matrix   dssweighted-unifrac-distance-matrix-trimmed.qza \
--m-metadata-file  /Users/anshulsinha/Desktop/Sequencing_analyses/16S_ali_experiment_2018_cross_infect/fastq/rainin_metadata_ali_2018.txt \
--m-metadata-column bac_treatment \
--o-visualization dsswunifracbac-treatment-filtered-betasig-trimmed.qzv \
--p-pairwise
```

    [32mSaved Visualization to: dsswunifracbac-treatment-filtered-betasig-trimmed.qzv[0m



```bash
qiime diversity beta-group-significance \
--i-distance-matrix   dssweighted-unifrac-distance-matrix-trimmed.qza \
--m-metadata-file  /Users/anshulsinha/Desktop/Sequencing_analyses/16S_ali_experiment_2018_cross_infect/fastq/rainin_metadata_ali_2018.txt \
--m-metadata-column phage_treatment \
--o-visualization dswunifracphage-treatment-filtered-betasig-trimmed.qzv \
--p-pairwise


```

    [32mSaved Visualization to: dswunifracphage-treatment-filtered-betasig-trimmed.qzv[0m



```bash
qiime tools view dswunifracphage-treatment-filtered-betasig-trimmed.qzv
```

    Press the 'q' key, Control-C, or Control-D to quit. This view may no longer be accessible or work correctly after quitting.


```bash
qiime diversity beta-group-significance \
--i-distance-matrix   dssbray-curtis-distance-matrix-trimmed.qza \
--m-metadata-file  /Users/anshulsinha/Desktop/Sequencing_analyses/16S_ali_experiment_2018_cross_infect/fastq/rainin_metadata_ali_2018.txt \
--m-metadata-column phage_treatment \
--o-visualization dssbccphage-treatment-filtered-betasig-trimmed.qzv \
--p-pairwise

```

    [32mSaved Visualization to: dssbccphage-treatment-filtered-betasig-trimmed.qzv[0m



```bash
qiime diversity alpha-group-significance \
--i-alpha-diversity  dssshannon-vector-trimmed.qza \
--m-metadata-file /Users/anshulsinha/Desktop/Sequencing_analyses/16S_ali_experiment_2018_cross_infect/fastq/rainin_metadata_ali_2018.txt \
--o-visualization dssshannon--treatment-filtered-betasig-trimmed.qzv 
```

    [32mSaved Visualization to: dssshannon--treatment-filtered-betasig-trimmed.qzv[0m



```bash
qiime diversity beta-group-significance \
--i-distance-matrix    dssbray-curtis-distance-matrix-trimmed.qza \
--m-metadata-file  /Users/anshulsinha/Desktop/Sequencing_analyses/16S_ali_experiment_2018_cross_infect/fastq/rainin_metadata_ali_2018.txt \
--m-metadata-column bac_treatment \
--o-visualization dssbcbac-treatment-filtered-betasig-trimmed.qzv \
--p-pairwise
```

    [32mSaved Visualization to: dssbcbac-treatment-filtered-betasig-trimmed.qzv[0m



```bash
qiime feature-classifier classify-sklearn \
--i-classifier silva-138-99-515-806-nb-classifier.qza \
--i-reads rep-seqs-trimmed.qza \
--o-classification taxonomy.qza 
#classifying features using the Silva Db
```

    [32mSaved FeatureData[Taxonomy] to: taxonomy.qza[0m



```bash
qiime taxa collapse \
--i-table table-f2.qza \
--i-taxonomy taxonomy.qza \
--p-level 7 \
--o-collapsed-table species-table.qza
#collapsing all samples to species level
```

    [32mSaved FeatureTable[Frequency] to: species-table.qza[0m



```bash
qiime taxa collapse \
--i-table table-f2.qza \
--i-taxonomy taxonomy.qza \
--p-level 2 \
--o-collapsed-table phyla-table.qza
#collapsing all samples to phyla level
```

    [32mSaved FeatureTable[Frequency] to: phyla-table.qza[0m



```bash
qiime taxa collapse \
--i-table Dss-filtered-table.qza \
--i-taxonomy taxonomy.qza \
--p-level 7 \
--o-collapsed-table species-table-dss.qza
#Collapsing all DSS/washout period samples to species level
```

    [32mSaved FeatureTable[Frequency] to: species-table-dss.qza[0m



```bash
qiime composition add-pseudocount \
--i-table species-table.qza \
--o-composition-table species-comp-table.qza 
#adding pseudocount for ANCOM
```

    [32mSaved FeatureTable[Composition] to: species-comp-table.qza[0m



```bash
qiime composition add-pseudocount \
--i-table species-table-dss.qza \
--o-composition-table species-comp-table-dss.qza
#adding pseudocount for ANCOM (DSS samples)
```

    [32mSaved FeatureTable[Composition] to: species-comp-table-dss.qza[0m



```bash
qiime composition ancom \
--i-table species-comp-table.qza \
--m-metadata-file /Users/anshulsinha/Desktop/Sequencing_analyses/16S_ali_experiment_2018_cross_infect/fastq/rainin_metadata_ali_2018.txt \
--m-metadata-column bac_treatment \
--o-visualization ancom-species.qzv
#ANCOM at the species level - including all samples
#comparing bacterial treatment groups
```

    [32mSaved Visualization to: ancom-species.qzv[0m



```bash
qiime composition ancom \
--i-table species-comp-table-dss.qza \
--m-metadata-file /Users/anshulsinha/Desktop/Sequencing_analyses/16S_ali_experiment_2018_cross_infect/fastq/rainin_metadata_ali_2018.txt \
--m-metadata-column bac_treatment \
--o-visualization ancom-species-dss.qzv
#same as above with just DSS samples 
#comparing bacterial treatment groups
```

    [32mSaved Visualization to: ancom-species-dss.qzv[0m



```bash

```


```bash
#For each ANCOM comparison 
qiime taxa collapse \
--i-table Hbacgav-filtered-table.qza \
--i-taxonomy taxonomy.qza \
--p-level 7 \
--o-collapsed-table species-table-hbacgav.qza
#Collapsing all healthy bacteria, phage gavage period samples to species level
```

    [32mSaved FeatureTable[Frequency] to: species-table-hbacgav.qza[0m



```bash
qiime composition add-pseudocount \
--i-table species-table-hbacgav.qza \
--o-composition-table species-comp-tablehbacgav.qza 
#adding pseudocount for ANCOM
```

    [32mSaved FeatureTable[Composition] to: species-comp-tablehbacgav.qza[0m



```bash
qiime composition ancom \
--i-table species-comp-tablehbacgav.qza  \
--m-metadata-file /Users/anshulsinha/Desktop/Sequencing_analyses/16S_ali_experiment_2018_cross_infect/fastq/rainin_metadata_ali_2018.txt \
--m-metadata-column phage_treatment \
--o-visualization ancom-species-hbacgav.qzv
#VLP comparison- healthy bacteria background- phage gavage period 

```

    [32mSaved Visualization to: ancom-species-hbacgav.qzv[0m



```bash
#For each ANCOM comparison 
qiime taxa collapse \
--i-table UCbacgav-filtered-table.qza \
--i-taxonomy taxonomy.qza \
--p-level 7 \
--o-collapsed-table species-table-UCbacgav.qza
#Collapsing all UC bacteria, phage gavage period samples to species level
```

    [32mSaved FeatureTable[Frequency] to: species-table-UCbacgav.qza[0m



```bash
qiime composition add-pseudocount \
--i-table species-table-UCbacgav.qza \
--o-composition-table species-comp-tableUCbacgav.qza 
#adding pseudocount for ANCOM
```

    [32mSaved FeatureTable[Composition] to: species-comp-tableUCbacgav.qza[0m



```bash
qiime composition ancom \
--i-table species-comp-tableUCbacgav.qza   \
--m-metadata-file /Users/anshulsinha/Desktop/Sequencing_analyses/16S_ali_experiment_2018_cross_infect/fastq/rainin_metadata_ali_2018.txt \
--m-metadata-column phage_treatment \
--o-visualization ancom-species-UCbacgav.qzv
#VLP comparison- UC bacteria background- phage gavage period 


```

    [32mSaved Visualization to: ancom-species-UCbacgav.qzv[0m



```bash
#For each ANCOM comparison 
qiime taxa collapse \
--i-table HbacDss-filtered-table.qza \
--i-taxonomy taxonomy.qza \
--p-level 7 \
--o-collapsed-table species-table-Hbacdss.qza
#Collapsing all Healthy bacteria, DSS/Washout period samples to species level
```

    [32mSaved FeatureTable[Frequency] to: species-table-Hbacdss.qza[0m



```bash
qiime composition add-pseudocount \
--i-table species-table-Hbacdss.qza \
--o-composition-table species-comp-tableHbacdss.qza 
#adding pseudocount for ANCOM
```

    [32mSaved FeatureTable[Composition] to: species-comp-tableHbacdss.qza[0m



```bash
qiime composition ancom \
--i-table species-comp-tableHbacdss.qza   \
--m-metadata-file /Users/anshulsinha/Desktop/Sequencing_analyses/16S_ali_experiment_2018_cross_infect/fastq/rainin_metadata_ali_2018.txt \
--m-metadata-column phage_treatment \
--o-visualization ancom-species-Hbacdss.qzv
#VLP comparison- Healthy bacteria background- DSS washout period 



```

    [32mSaved Visualization to: ancom-species-Hbacdss.qzv[0m



```bash
#For each ANCOM comparison 
qiime taxa collapse \
--i-table UCDss-filtered-table.qza \
--i-taxonomy taxonomy.qza \
--p-level 7 \
--o-collapsed-table species-table-UCbacdss.qza
#Collapsing all UC bacteria, DSS/Washout period samples to species level
```

    [32mSaved FeatureTable[Frequency] to: species-table-UCbacdss.qza[0m



```bash
qiime composition add-pseudocount \
--i-table species-table-UCbacdss.qza \
--o-composition-table species-comp-tableUCbacdss.qza 
#adding pseudocount for ANCOM
```

    [32mSaved FeatureTable[Composition] to: species-comp-tableUCbacdss.qza[0m



```bash
qiime composition ancom \
--i-table species-comp-tableUCbacdss.qza   \
--m-metadata-file /Users/anshulsinha/Desktop/Sequencing_analyses/16S_ali_experiment_2018_cross_infect/fastq/rainin_metadata_ali_2018.txt \
--m-metadata-column phage_treatment \
--o-visualization ancom-species-UCbacdss.qzv
#VLP comparison- UC bacteria background- DSS washout period 



```

    [32mSaved Visualization to: ancom-species-UCbacdss.qzv[0m



```bash
qiime tools view ancom-species-UCbacdss.qzv
```

    Press the 'q' key, Control-C, or Control-D to quit. This view may no longer be accessible or work correctly after quitting.


```bash
qiime longitudinal feature-volatility  \
--i-table phyla-table.qza \
--m-metadata-file /Users/anshulsinha/Desktop/Sequencing_analyses/16S_ali_experiment_2018_cross_infect/fastq/rainin_metadata_ali_2018.txt \
--p-state-column Date \
--p-estimator RandomForestRegressor \
--p-n-jobs 4 \
--p-n-estimators 400 \
--o-filtered-table phyla-feature-vol-filtered-table-trimmed.qza \
--o-feature-importance phyla-feature-vol-importance-trimmed.qza \
--o-volatility-plot phyla-feature-vol-plot-trimmed.qzv \
--o-accuracy-results phyla-accuracy-results-feature-vol-trimmed.qzv \
--o-sample-estimator phyla-sample-estimator-feature-vol-trimmed.qza 
#Feature volatility output at species level; showing how each species changes over time
```

    [32mSaved FeatureTable[RelativeFrequency] to: phyla-feature-vol-filtered-table-trimmed.qza[0m
    [32mSaved FeatureData[Importance] to: phyla-feature-vol-importance-trimmed.qza[0m
    [32mSaved Visualization to: phyla-feature-vol-plot-trimmed.qzv[0m
    [32mSaved Visualization to: phyla-accuracy-results-feature-vol-trimmed.qzv[0m
    [32mSaved SampleEstimator[Regressor] to: phyla-sample-estimator-feature-vol-trimmed.qza[0m



```bash
qiime tools view phyla-feature-vol-plot-trimmed.qzv
```

    Press the 'q' key, Control-C, or Control-D to quit. This view may no longer be accessible or work correctly after quitting.


```bash
qiime longitudinal feature-volatility  \
--i-table species-table.qza \
--m-metadata-file /Users/anshulsinha/Desktop/Sequencing_analyses/16S_ali_experiment_2018_cross_infect/fastq/rainin_metadata_ali_2018.txt \
--p-state-column Date \
--p-estimator RandomForestRegressor \
--p-n-jobs 4 \
--p-n-estimators 400 \
--o-filtered-table species-feature-vol-filtered-table-trimmed.qza \
--o-feature-importance species-feature-vol-importance-trimmed.qza \
--o-volatility-plot species-feature-vol-plot-trimmed.qzv \
--o-accuracy-results species-accuracy-results-feature-vol-trimmed.qzv \
--o-sample-estimator species-sample-estimator-feature-vol-trimmed.qza 
#Feature volatility output at species level; showing how each species changes over time
```

    [32mSaved FeatureTable[RelativeFrequency] to: species-feature-vol-filtered-table-trimmed.qza[0m
    [32mSaved FeatureData[Importance] to: species-feature-vol-importance-trimmed.qza[0m
    [32mSaved Visualization to: species-feature-vol-plot-trimmed.qzv[0m
    [32mSaved Visualization to: species-accuracy-results-feature-vol-trimmed.qzv[0m
    [32mSaved SampleEstimator[Regressor] to: species-sample-estimator-feature-vol-trimmed.qza[0m



```bash
qiime tools view species-feature-vol-plot-trimmed.qzv
```


```bash
qiime feature-table group  \
--i-table gav-filtered-table.qza \
--p-axis sample \
--m-metadata-file /Users/anshulsinha/Desktop/Sequencing_analyses/16S_ali_experiment_2018_cross_infect/fastq/rainin_metadata_ali_2018.txt \
--m-metadata-column phage_treatment \
--p-mode sum \
--o-grouped-table gav-phage_treatment-grouped-table.qza
```

    [32mSaved FeatureTable[Frequency] to: gav-phage_treatment-grouped-table.qza[0m



```bash
qiime taxa barplot \
--i-table gav-phage_treatment-grouped-table.qza \
--i-taxonomy taxonomy.qza \
--m-metadata-file /Users/anshulsinha/Desktop/Sequencing_analyses/16S_ali_experiment_2018_cross_infect/fastq/rainin_metadata_collapsed_phage_treatment.txt \
--o-visualization phage_treatment-taxabp_gavage.qzv
```

    [32mSaved Visualization to: phage_treatment-taxabp_gavage.qzv[0m



```bash
qiime feature-table group  \
--i-table Dss-filtered-table.qza \
--p-axis sample \
--m-metadata-file /Users/anshulsinha/Desktop/Sequencing_analyses/16S_ali_experiment_2018_cross_infect/fastq/rainin_metadata_ali_2018.txt \
--m-metadata-column phage_treatment \
--p-mode sum \
--o-grouped-table dss-phage_treatment-grouped-table.qza
```

    [32mSaved FeatureTable[Frequency] to: dss-phage_treatment-grouped-table.qza[0m



```bash
qiime taxa barplot \
--i-table dss-phage_treatment-grouped-table.qza \
--i-taxonomy taxonomy.qza \
--m-metadata-file /Users/anshulsinha/Desktop/Sequencing_analyses/16S_ali_experiment_2018_cross_infect/fastq/rainin_metadata_collapsed_phage_treatment.txt \
--o-visualization phage_treatment-taxabp_dss.qzv
```

    [32mSaved Visualization to: phage_treatment-taxabp_dss.qzv[0m



```bash
qiime feature-table group  \
--i-table table-f2.qza \
--p-axis sample \
--m-metadata-file /Users/anshulsinha/Desktop/Sequencing_analyses/16S_ali_experiment_2018_cross_infect/fastq/rainin_metadata_ali_2018.txt \
--m-metadata-column bac_treatment \
--p-mode sum \
--o-grouped-table bac-grouped-table.qza
```

    [32mSaved FeatureTable[Frequency] to: bac-grouped-table.qza[0m



```bash
qiime taxa barplot \
--i-table bac-grouped-table.qza \
--i-taxonomy taxonomy.qza \
--m-metadata-file /Users/anshulsinha/Desktop/Sequencing_analyses/16S_ali_experiment_2018_cross_infect/fastq/rainin_metadata_collapsed_bac_treatment.txt \
--o-visualization taxabp-bac_treatment.qzv
```

    [32mSaved Visualization to: taxabp-bac_treatment.qzv[0m

