```bash
source activate qiime2-2020.6
```

    bash: activate: No such file or directory





```bash
cd /Users/anshulsinha/Desktop/Sequencing_analyses/Rainin_16S/rainin_16S_fall_2019_control_expt
```


```bash
qiime tools import \
    --type 'SampleData[PairedEndSequencesWithQuality]'\
    --input-path /Users/anshulsinha/Desktop/Sequencing_analyses/Rainin_16S/rainin_16S_fall_2019_control_expt/manifest_control_expt.csv \
    --output-path paired-end-demux-ctrl-expt.qza \
    --input-format PairedEndFastqManifestPhred33
#Importing data from fastq files

```

    [32mImported /Users/anshulsinha/Desktop/Sequencing_analyses/Rainin_16S/rainin_16S_fall_2019_control_expt/manifest_control_expt.csv as PairedEndFastqManifestPhred33 to paired-end-demux-ctrl-expt.qza[0m
    (qiime2-2020.6) (qiime2-2020.6) (qiime2-2020.6) (qiime2-2020.6) 




```bash
qiime cutadapt trim-paired \
--i-demultiplexed-sequences paired-end-demux-ctrl-expt.qza \
--p-cores 4 \
--p-front-f GTGCCAGCMGCCGCGGTAA \
--p-front-r  GGACTACHVGGGTWTCTAAT \
--o-trimmed-sequences paired-end-demux-trimmed_ctrl_expt.qza
#Trimming forward and reverse primers + tag sequences
#This command will cut everything before the forward or reverse sequence
#type zless and then copy your file path to see if sequences are removed 
```

    [32mSaved SampleData[PairedEndSequencesWithQuality] to: paired-end-demux-trimmed_ctrl_expt.qza[0m
    (qiime2-2020.6) (qiime2-2020.6) (qiime2-2020.6) (qiime2-2020.6) (qiime2-2020.6) (qiime2-2020.6) 




```bash
qiime demux summarize \
--i-data paired-end-demux-trimmed_ctrl_expt.qza \
--o-visualization paired-end-demux-trimmed_ctrl_expt.qzv 
```

    [32mSaved Visualization to: paired-end-demux-trimmed_ctrl_expt.qzv[0m
    (qiime2-2020.6) 




```bash
qiime dada2 denoise-paired \
--i-demultiplexed-seqs  paired-end-demux-trimmed_ctrl_expt.qza \
--o-table table_ctrl_expt.qza \
--o-representative-sequences rep-seqs-trimmed_ctrl_expt.qza \
--p-min-fold-parent-over-abundance 5 \
--p-trunc-len-f 220 \
--p-trunc-len-r 210 \
--p-n-threads 0 \
--o-denoising-stats stats-dada2-trimmed_ctrl_expt.qza
#trimming seqs based on quality and running dada2
#originally had a high proportion of chimeras, even after trimming primers off
#changed chimera stringency in dada2 using the p-min fold over abundance to 5 from default 2 
```

    [32mSaved FeatureTable[Frequency] to: table_ctrl_expt.qza[0m
    [32mSaved FeatureData[Sequence] to: rep-seqs-trimmed_ctrl_expt.qza[0m
    [32mSaved SampleData[DADA2Stats] to: stats-dada2-trimmed_ctrl_expt.qza[0m
    (qiime2-2020.6) (qiime2-2020.6) (qiime2-2020.6) (qiime2-2020.6) (qiime2-2020.6) 




```bash
qiime metadata tabulate \
--m-input-file stats-dada2-trimmed_ctrl_expt.qza \
--o-visualization stats-dada2-trimmed_ctrl_expt.qzv
# how many reads passed through each dada2 step per sample.

```

    [32mSaved Visualization to: stats-dada2-trimmed_ctrl_expt.qzv[0m
    (qiime2-2020.6) (qiime2-2020.6) (qiime2-2020.6) (qiime2-2020.6) 




```bash
  qiime feature-table filter-features \
  --i-table table_ctrl_expt.qza \
  --p-min-samples 2 \
  --o-filtered-table table_ctrl_exptf1.qza \

qiime feature-table filter-features \
  --i-table table_ctrl_exptf1.qza \
  --p-min-frequency 10 \
  --o-filtered-table table_stocks.qza
  #Removing features with less than 10 reads per sample and those only found in a single sample
```

    [32mSaved FeatureTable[Frequency] to: table_ctrl_exptf1.qza[0m
    [32mSaved FeatureTable[Frequency] to: table_stocks.qza[0m



```bash
qiime feature-table summarize \
    --i-table table_stocks.qza \
    --o-visualization table_stocks.qzv \
    --m-sample-metadata-file /Users/anshulsinha/Desktop/Sequencing_analyses/Rainin_16S/rainin_16S_fall_2019_control_expt/metadata_ctrl_experiment.txt 
    #Looking at the generated feature table- tells us how many reads each sample contains 
 
```

    [32mSaved Visualization to: table_stocks.qzv[0m



```bash
qiime tools view table_stocks.qzv
```

    Press the 'q' key, Control-C, or Control-D to quit. This view may no longer be accessible or work correctly after quitting.


```bash
qiime feature-table tabulate-seqs \
    --i-data rep-seqs-trimmed_ctrl_expt.qza \
    --o-visualization rep-seqs-trimmed_ctrl_expt.qzv
```

    [32mSaved Visualization to: rep-seqs-trimmed_ctrl_expt.qzv[0m



```bash
qiime phylogeny align-to-tree-mafft-fasttree \
    --i-sequences rep-seqs-trimmed_ctrl_expt.qza \
    --o-alignment aligned-rep-seqs-trimmed_ctrl_expt.qza \
    --o-masked-alignment masked-aligned-rep-seqs-trimmed_ctrl_expt.qza \
    --o-tree unrooted-tree-trimmed_ctrl_expt.qza \
    --o-rooted-tree rooted-tree-trimmed_ctrl_expt.qza 
#For the diversity metrics that rely on phylogeny ie. UniFrac, maaft performs a multiple alignment
```

    [32mSaved FeatureData[AlignedSequence] to: aligned-rep-seqs-trimmed_ctrl_expt.qza[0m
    [32mSaved FeatureData[AlignedSequence] to: masked-aligned-rep-seqs-trimmed_ctrl_expt.qza[0m
    [32mSaved Phylogeny[Unrooted] to: unrooted-tree-trimmed_ctrl_expt.qza[0m
    [32mSaved Phylogeny[Rooted] to: rooted-tree-trimmed_ctrl_expt.qza[0m



```bash
qiime feature-table filter-samples \
--i-table table_stocks.qza \
--m-metadata-file /Users/anshulsinha/Desktop/Sequencing_analyses/Rainin_16S/rainin_16S_fall_2019_control_expt/metadata_ctrl.tsv \
--p-where "period = 'neg'" \
--p-exclude-ids "TRUE" \
--o-filtered-table nostock-filtered-table_ctrl_expt.qza
#Filtering out neg control samples 
```

    [32mSaved FeatureTable[Frequency] to: nostock-filtered-table_ctrl_expt.qza[0m



```bash
qiime feature-table filter-samples \
--i-table nostock-filtered-table_ctrl_expt1.qza \
--m-metadata-file /Users/anshulsinha/Desktop/Sequencing_analyses/Rainin_16S/rainin_16S_fall_2019_control_expt/metadata_ctrl.tsv \
--p-where "period = 'colonization'" \
--o-filtered-table col-nostock-filtered-table_ctrl_expt.qza
#Filtering samples only present in bacterial colonization period 
```

    [32mSaved FeatureTable[Frequency] to: col-nostock-filtered-table_ctrl_expt.qza[0m



```bash
qiime feature-table filter-samples \
--i-table nostock-filtered-table_ctrl_expt1.qza \
--m-metadata-file /Users/anshulsinha/Desktop/Sequencing_analyses/Rainin_16S/rainin_16S_fall_2019_control_expt/metadata_ctrl.tsv \
--p-where "period = 'gavage'" \
--o-filtered-table gav-nostock-filtered-table_ctrl_expt.qza
#Filtering samples only present in phage gavage period
```

    [32mSaved FeatureTable[Frequency] to: gav-nostock-filtered-table_ctrl_expt.qza[0m



```bash
qiime feature-table filter-samples \
--i-table nostock-filtered-table_ctrl_expt1.qza \
--m-metadata-file /Users/anshulsinha/Desktop/Sequencing_analyses/Rainin_16S/rainin_16S_fall_2019_control_expt/metadata_ctrl.tsv \
--p-where "period = 'DSS'" \
--o-filtered-table dss-nostock-filtered-table_ctrl_expt.qza
#Filtering samples only present during DSS washout period 
```

    [32mSaved FeatureTable[Frequency] to: dss-nostock-filtered-table_ctrl_expt.qza[0m



```bash
qiime feature-table filter-samples \
--i-table nostock-filtered-table_ctrl_expt1.qza \
--m-metadata-file /Users/anshulsinha/Desktop/Sequencing_analyses/Rainin_16S/rainin_16S_fall_2019_control_expt/metadata_ctrl.tsv \
--p-where "Treatment = 'UC Phage (No DSS)'" \
--o-filtered-table ucphage-nodss-nostock-filtered-table_ctrl_expt.qza
#Including only UC VLP (NO DSS) samples 
```

    [32mSaved FeatureTable[Frequency] to: ucphage-nodss-nostock-filtered-table_ctrl_expt.qza[0m



```bash
qiime feature-table filter-samples \
--i-table nostock-filtered-table_ctrl_expt1.qza \
--m-metadata-file /Users/anshulsinha/Desktop/Sequencing_analyses/Rainin_16S/rainin_16S_fall_2019_control_expt/metadata_ctrl.tsv \
--p-where "Treatment = 'UC Phage (+DSS)'" \
--o-filtered-table ucphage-yesdss-nostock-filtered-table_ctrl_expt.qza
#Including only UC VLP (+ DSS) samples 
```

    [32mSaved FeatureTable[Frequency] to: ucphage-yesdss-nostock-filtered-table_ctrl_expt.qza[0m



```bash
qiime feature-table filter-samples \
--i-table nostock-filtered-table_ctrl_expt1.qza \
--m-metadata-file /Users/anshulsinha/Desktop/Sequencing_analyses/Rainin_16S/rainin_16S_fall_2019_control_expt/metadata_ctrl.tsv \
--p-where "Treatment = 'HK UC Phage (+DSS)'" \
--o-filtered-table hkucphage-yesdss-nostock-filtered-table_ctrl_expt.qza
#Including only HK UC VLP (+ DSS) samples 
```

    [32mSaved FeatureTable[Frequency] to: hkucphage-yesdss-nostock-filtered-table_ctrl_expt.qza[0m



```bash
qiime feature-table filter-samples \
--i-table table_stocks.qza \
--m-metadata-file /Users/anshulsinha/Desktop/Sequencing_analyses/Rainin_16S/rainin_16S_fall_2019_control_expt/metadata_ctrl.tsv \
--p-where "pooled_stock = 'no'" \
--p-exclude-ids TRUE \
--o-filtered-table pooled-stocks-filtered-table_ctrl_expt.qza
#including all pooled stock samples by excluding anything in the metadata that isn't a pooled stock
```

    [32mSaved FeatureTable[Frequency] to: pooled-stocks-filtered-table_ctrl_expt.qza[0m



```bash
qiime feature-table filter-samples \
--i-table table_stocks.qza \
--m-metadata-file /Users/anshulsinha/Desktop/Sequencing_analyses/Rainin_16S/rainin_16S_fall_2019_control_expt/metadata_ctrl.tsv \
--p-where "UC_stock = 'yes'" \
--o-filtered-table ucstocks-filtered-table_ctrl_expt.qza
#filtering for just the  uc stock
#Note this includes individual and pooled samples - because we have removed features found in a single sample, this means the data generated from individual samples may be inaccurate 

```

    [32mSaved FeatureTable[Frequency] to: ucstocks-filtered-table_ctrl_expt.qza[0m



```bash
qiime feature-table filter-samples \
--i-table table_stocks.qza \
--m-metadata-file /Users/anshulsinha/Desktop/Sequencing_analyses/Rainin_16S/rainin_16S_fall_2019_control_expt/metadata_ctrl.tsv \
--p-where "healthy_stock = 'yes'" \
--o-filtered-table hstocks-filtered-table_ctrl_expt.qza
#filtering for just the healthy stock
#Note this includes individual and pooled samples - because we have removed features found in a single sample, this means the data generated from individual samples may be inaccurate 

```

    [32mSaved FeatureTable[Frequency] to: hstocks-filtered-table_ctrl_expt.qza[0m



```bash
qiime diversity core-metrics-phylogenetic \
--i-phylogeny rooted-tree-trimmed_ctrl_expt.qza  \
--i-table nostock-filtered-table_ctrl_expt.qza \
--p-sampling-depth 31455 \
--m-metadata-file /Users/anshulsinha/Desktop/Sequencing_analyses/Rainin_16S/rainin_16S_fall_2019_control_expt/metadata_ctrl.tsv \
--o-rarefied-table rarefied-table-trimmed-ctrl-exptnostock.qza \
--o-faith-pd-vector faith-pd-trimmed-ctrl-exptnostock.qza \
--o-observed-features-vector observed-otus-trimmed-ctrl-exptnostock.qza \
--o-shannon-vector shannon-vector-trimmed-ctrl-exptnostock.qza \
--o-evenness-vector evenness-vector-trimmed-ctrl-exptnostock.qza \
--o-unweighted-unifrac-distance-matrix unweighted-unifrac-distance-matrix-trimmed-ctrl-exptnostock.qza \
--o-weighted-unifrac-distance-matrix weighted-unifrac-distance-matrix-trimmed-ctrl-exptnostock.qza \
--o-jaccard-distance-matrix jaccard-distance-matrix-trimmed-ctrl-exptnostock.qza \
--o-bray-curtis-distance-matrix bray-curtis-distance-matrix-trimmed-ctrl-exptnostock.qza \
--o-unweighted-unifrac-pcoa-results unweighted-unifrac-pca-results-trimmed-ctrl-exptnostock.qza \
--o-weighted-unifrac-pcoa-results weighted-unifrac-pcoa-results-trimmed-ctrl-exptnostock.qza \
--o-jaccard-pcoa-results jaccard-pcoa-results-trimmed-trimmed-ctrl-exptnostock.qza \
--o-bray-curtis-pcoa-results trimmed-bray-curtis-pcoa-results-trimmed-ctrl-exptnostock.qza \
--o-unweighted-unifrac-emperor unweighted-unifrac-emperor-trimmed-ctrl-exptnostock.qzv \
--o-weighted-unifrac-emperor weighted-unifrac-emperor-trimmed-ctrl-exptnostock.qzv \
--o-jaccard-emperor jaccard-emperor-trimmed-ctrl-exptnostock.qzv \
--o-bray-curtis-emperor bc-emperor-ctrl-exptnostock.qzv
#Diversity analyses including all samples and treatment groups 
```

    [32mSaved FeatureTable[Frequency] to: rarefied-table-trimmed-ctrl-exptnostock.qza[0m
    [32mSaved SampleData[AlphaDiversity] to: faith-pd-trimmed-ctrl-exptnostock.qza[0m
    [32mSaved SampleData[AlphaDiversity] to: observed-otus-trimmed-ctrl-exptnostock.qza[0m
    [32mSaved SampleData[AlphaDiversity] to: shannon-vector-trimmed-ctrl-exptnostock.qza[0m
    [32mSaved SampleData[AlphaDiversity] to: evenness-vector-trimmed-ctrl-exptnostock.qza[0m
    [32mSaved DistanceMatrix to: unweighted-unifrac-distance-matrix-trimmed-ctrl-exptnostock.qza[0m
    [32mSaved DistanceMatrix to: weighted-unifrac-distance-matrix-trimmed-ctrl-exptnostock.qza[0m
    [32mSaved DistanceMatrix to: jaccard-distance-matrix-trimmed-ctrl-exptnostock.qza[0m
    [32mSaved DistanceMatrix to: bray-curtis-distance-matrix-trimmed-ctrl-exptnostock.qza[0m
    [32mSaved PCoAResults to: unweighted-unifrac-pca-results-trimmed-ctrl-exptnostock.qza[0m
    [32mSaved PCoAResults to: weighted-unifrac-pcoa-results-trimmed-ctrl-exptnostock.qza[0m
    [32mSaved PCoAResults to: jaccard-pcoa-results-trimmed-trimmed-ctrl-exptnostock.qza[0m
    [32mSaved PCoAResults to: trimmed-bray-curtis-pcoa-results-trimmed-ctrl-exptnostock.qza[0m
    [32mSaved Visualization to: unweighted-unifrac-emperor-trimmed-ctrl-exptnostock.qzv[0m
    [32mSaved Visualization to: weighted-unifrac-emperor-trimmed-ctrl-exptnostock.qzv[0m
    [32mSaved Visualization to: jaccard-emperor-trimmed-ctrl-exptnostock.qzv[0m
    [32mSaved Visualization to: bc-emperor-ctrl-exptnostock.qzv[0m



```bash
qiime diversity core-metrics-phylogenetic \
--i-phylogeny rooted-tree-trimmed_ctrl_expt.qza  \
--i-table col-nostock-filtered-table_ctrl_expt.qza \
--p-sampling-depth 31455 \
--m-metadata-file /Users/anshulsinha/Desktop/Sequencing_analyses/Rainin_16S/rainin_16S_fall_2019_control_expt/metadata_ctrl.tsv \
--o-rarefied-table colrarefied-table-trimmed-ctrl-exptnostock.qza \
--o-faith-pd-vector colfaith-pd-trimmed-ctrl-exptnostock.qza \
--o-observed-features-vector colobserved-otus-trimmed-ctrl-exptnostock.qza \
--o-shannon-vector colshannon-vector-trimmed-ctrl-exptnostock.qza \
--o-evenness-vector colevenness-vector-trimmed-ctrl-exptnostock.qza \
--o-unweighted-unifrac-distance-matrix colunweighted-unifrac-distance-matrix-trimmed-ctrl-exptnostock.qza \
--o-weighted-unifrac-distance-matrix colweighted-unifrac-distance-matrix-trimmed-ctrl-exptnostock.qza \
--o-jaccard-distance-matrix coljaccard-distance-matrix-trimmed-ctrl-exptnostock.qza \
--o-bray-curtis-distance-matrix colbray-curtis-distance-matrix-trimmed-ctrl-exptnostock.qza \
--o-unweighted-unifrac-pcoa-results colunweighted-unifrac-pca-results-trimmed-ctrl-exptnostock.qza \
--o-weighted-unifrac-pcoa-results colweighted-unifrac-pcoa-results-trimmed-ctrl-exptnostock.qza \
--o-jaccard-pcoa-results coljaccard-pcoa-results-trimmed-trimmed-ctrl-exptnostock.qza \
--o-bray-curtis-pcoa-results coltrimmed-bray-curtis-pcoa-results-trimmed-ctrl-exptnostock.qza \
--o-unweighted-unifrac-emperor colunweighted-unifrac-emperor-trimmed-ctrl-exptnostock.qzv \
--o-weighted-unifrac-emperor colweighted-unifrac-emperor-trimmed-ctrl-exptnostock.qzv \
--o-jaccard-emperor coljaccard-emperor-trimmed-ctrl-exptnostock.qzv \
--o-bray-curtis-emperor colbc-emperor-ctrl-exptnostock.qzv
#filtered diversity analyses
```

    [32mSaved FeatureTable[Frequency] to: colrarefied-table-trimmed-ctrl-exptnostock.qza[0m
    [32mSaved SampleData[AlphaDiversity] to: colfaith-pd-trimmed-ctrl-exptnostock.qza[0m
    [32mSaved SampleData[AlphaDiversity] to: colobserved-otus-trimmed-ctrl-exptnostock.qza[0m
    [32mSaved SampleData[AlphaDiversity] to: colshannon-vector-trimmed-ctrl-exptnostock.qza[0m
    [32mSaved SampleData[AlphaDiversity] to: colevenness-vector-trimmed-ctrl-exptnostock.qza[0m
    [32mSaved DistanceMatrix to: colunweighted-unifrac-distance-matrix-trimmed-ctrl-exptnostock.qza[0m
    [32mSaved DistanceMatrix to: colweighted-unifrac-distance-matrix-trimmed-ctrl-exptnostock.qza[0m
    [32mSaved DistanceMatrix to: coljaccard-distance-matrix-trimmed-ctrl-exptnostock.qza[0m
    [32mSaved DistanceMatrix to: colbray-curtis-distance-matrix-trimmed-ctrl-exptnostock.qza[0m
    [32mSaved PCoAResults to: colunweighted-unifrac-pca-results-trimmed-ctrl-exptnostock.qza[0m
    [32mSaved PCoAResults to: colweighted-unifrac-pcoa-results-trimmed-ctrl-exptnostock.qza[0m
    [32mSaved PCoAResults to: coljaccard-pcoa-results-trimmed-trimmed-ctrl-exptnostock.qza[0m
    [32mSaved PCoAResults to: coltrimmed-bray-curtis-pcoa-results-trimmed-ctrl-exptnostock.qza[0m
    [32mSaved Visualization to: colunweighted-unifrac-emperor-trimmed-ctrl-exptnostock.qzv[0m
    [32mSaved Visualization to: colweighted-unifrac-emperor-trimmed-ctrl-exptnostock.qzv[0m
    [32mSaved Visualization to: coljaccard-emperor-trimmed-ctrl-exptnostock.qzv[0m
    [32mSaved Visualization to: colbc-emperor-ctrl-exptnostock.qzv[0m



```bash
qiime diversity core-metrics-phylogenetic \
--i-phylogeny rooted-tree-trimmed_ctrl_expt.qza  \
--i-table gav-nostock-filtered-table_ctrl_expt.qza \
--p-sampling-depth 31455 \
--m-metadata-file /Users/anshulsinha/Desktop/Sequencing_analyses/Rainin_16S/rainin_16S_fall_2019_control_expt/metadata_ctrl.tsv \
--o-rarefied-table gavrarefied-table-trimmed-ctrl-exptnostock.qza \
--o-faith-pd-vector gavfaith-pd-trimmed-ctrl-exptnostock.qza \
--o-observed-features-vector gavobserved-otus-trimmed-ctrl-exptnostock.qza \
--o-shannon-vector gavshannon-vector-trimmed-ctrl-exptnostock.qza \
--o-evenness-vector gavevenness-vector-trimmed-ctrl-exptnostock.qza \
--o-unweighted-unifrac-distance-matrix gavunweighted-unifrac-distance-matrix-trimmed-ctrl-exptnostock.qza \
--o-weighted-unifrac-distance-matrix gavweighted-unifrac-distance-matrix-trimmed-ctrl-exptnostock.qza \
--o-jaccard-distance-matrix gavjaccard-distance-matrix-trimmed-ctrl-exptnostock.qza \
--o-bray-curtis-distance-matrix gavbray-curtis-distance-matrix-trimmed-ctrl-exptnostock.qza \
--o-unweighted-unifrac-pcoa-results gavunweighted-unifrac-pca-results-trimmed-ctrl-exptnostock.qza \
--o-weighted-unifrac-pcoa-results gavweighted-unifrac-pcoa-results-trimmed-ctrl-exptnostock.qza \
--o-jaccard-pcoa-results gavjaccard-pcoa-results-trimmed-trimmed-ctrl-exptnostock.qza \
--o-bray-curtis-pcoa-results gavtrimmed-bray-curtis-pcoa-results-trimmed-ctrl-exptnostock.qza \
--o-unweighted-unifrac-emperor gavunweighted-unifrac-emperor-trimmed-ctrl-exptnostock.qzv \
--o-weighted-unifrac-emperor gavweighted-unifrac-emperor-trimmed-ctrl-exptnostock.qzv \
--o-jaccard-emperor gavjaccard-emperor-trimmed-ctrl-exptnostock.qzv \
--o-bray-curtis-emperor gavbc-emperor-ctrl-exptnostock.qzv
#filtered diversity analyses
```

    [32mSaved FeatureTable[Frequency] to: gavrarefied-table-trimmed-ctrl-exptnostock.qza[0m
    [32mSaved SampleData[AlphaDiversity] to: gavfaith-pd-trimmed-ctrl-exptnostock.qza[0m
    [32mSaved SampleData[AlphaDiversity] to: gavobserved-otus-trimmed-ctrl-exptnostock.qza[0m
    [32mSaved SampleData[AlphaDiversity] to: gavshannon-vector-trimmed-ctrl-exptnostock.qza[0m
    [32mSaved SampleData[AlphaDiversity] to: gavevenness-vector-trimmed-ctrl-exptnostock.qza[0m
    [32mSaved DistanceMatrix to: gavunweighted-unifrac-distance-matrix-trimmed-ctrl-exptnostock.qza[0m
    [32mSaved DistanceMatrix to: gavweighted-unifrac-distance-matrix-trimmed-ctrl-exptnostock.qza[0m
    [32mSaved DistanceMatrix to: gavjaccard-distance-matrix-trimmed-ctrl-exptnostock.qza[0m
    [32mSaved DistanceMatrix to: gavbray-curtis-distance-matrix-trimmed-ctrl-exptnostock.qza[0m
    [32mSaved PCoAResults to: gavunweighted-unifrac-pca-results-trimmed-ctrl-exptnostock.qza[0m
    [32mSaved PCoAResults to: gavweighted-unifrac-pcoa-results-trimmed-ctrl-exptnostock.qza[0m
    [32mSaved PCoAResults to: gavjaccard-pcoa-results-trimmed-trimmed-ctrl-exptnostock.qza[0m
    [32mSaved PCoAResults to: gavtrimmed-bray-curtis-pcoa-results-trimmed-ctrl-exptnostock.qza[0m
    [32mSaved Visualization to: gavunweighted-unifrac-emperor-trimmed-ctrl-exptnostock.qzv[0m
    [32mSaved Visualization to: gavweighted-unifrac-emperor-trimmed-ctrl-exptnostock.qzv[0m
    [32mSaved Visualization to: gavjaccard-emperor-trimmed-ctrl-exptnostock.qzv[0m
    [32mSaved Visualization to: gavbc-emperor-ctrl-exptnostock.qzv[0m



```bash
qiime diversity core-metrics-phylogenetic \
--i-phylogeny rooted-tree-trimmed_ctrl_expt.qza  \
--i-table dss-nostock-filtered-table_ctrl_expt.qza \
--p-sampling-depth 31455 \
--m-metadata-file /Users/anshulsinha/Desktop/Sequencing_analyses/Rainin_16S/rainin_16S_fall_2019_control_expt/metadata_ctrl.tsv \
--o-rarefied-table dssrarefied-table-trimmed-ctrl-exptnostock.qza \
--o-faith-pd-vector dssfaith-pd-trimmed-ctrl-exptnostock.qza \
--o-observed-features-vector dssobserved-otus-trimmed-ctrl-exptnostock.qza \
--o-shannon-vector dssshannon-vector-trimmed-ctrl-exptnostock.qza \
--o-evenness-vector dssevenness-vector-trimmed-ctrl-exptnostock.qza \
--o-unweighted-unifrac-distance-matrix dssunweighted-unifrac-distance-matrix-trimmed-ctrl-exptnostock.qza \
--o-weighted-unifrac-distance-matrix dssweighted-unifrac-distance-matrix-trimmed-ctrl-exptnostock.qza \
--o-jaccard-distance-matrix dssjaccard-distance-matrix-trimmed-ctrl-exptnostock.qza \
--o-bray-curtis-distance-matrix dssbray-curtis-distance-matrix-trimmed-ctrl-exptnostock.qza \
--o-unweighted-unifrac-pcoa-results dssunweighted-unifrac-pca-results-trimmed-ctrl-exptnostock.qza \
--o-weighted-unifrac-pcoa-results dssweighted-unifrac-pcoa-results-trimmed-ctrl-exptnostock.qza \
--o-jaccard-pcoa-results dssjaccard-pcoa-results-trimmed-trimmed-ctrl-exptnostock.qza \
--o-bray-curtis-pcoa-results dsstrimmed-bray-curtis-pcoa-results-trimmed-ctrl-exptnostock.qza \
--o-unweighted-unifrac-emperor dssunweighted-unifrac-emperor-trimmed-ctrl-exptnostock.qzv \
--o-weighted-unifrac-emperor dssweighted-unifrac-emperor-trimmed-ctrl-exptnostock.qzv \
--o-jaccard-emperor dssjaccard-emperor-trimmed-ctrl-exptnostock.qzv \
--o-bray-curtis-emperor dssbc-emperor-ctrl-exptnostock.qzv
#filtered diversity analyses
```

    [32mSaved FeatureTable[Frequency] to: dssrarefied-table-trimmed-ctrl-exptnostock.qza[0m
    [32mSaved SampleData[AlphaDiversity] to: dssfaith-pd-trimmed-ctrl-exptnostock.qza[0m
    [32mSaved SampleData[AlphaDiversity] to: dssobserved-otus-trimmed-ctrl-exptnostock.qza[0m
    [32mSaved SampleData[AlphaDiversity] to: dssshannon-vector-trimmed-ctrl-exptnostock.qza[0m
    [32mSaved SampleData[AlphaDiversity] to: dssevenness-vector-trimmed-ctrl-exptnostock.qza[0m
    [32mSaved DistanceMatrix to: dssunweighted-unifrac-distance-matrix-trimmed-ctrl-exptnostock.qza[0m
    [32mSaved DistanceMatrix to: dssweighted-unifrac-distance-matrix-trimmed-ctrl-exptnostock.qza[0m
    [32mSaved DistanceMatrix to: dssjaccard-distance-matrix-trimmed-ctrl-exptnostock.qza[0m
    [32mSaved DistanceMatrix to: dssbray-curtis-distance-matrix-trimmed-ctrl-exptnostock.qza[0m
    [32mSaved PCoAResults to: dssunweighted-unifrac-pca-results-trimmed-ctrl-exptnostock.qza[0m
    [32mSaved PCoAResults to: dssweighted-unifrac-pcoa-results-trimmed-ctrl-exptnostock.qza[0m
    [32mSaved PCoAResults to: dssjaccard-pcoa-results-trimmed-trimmed-ctrl-exptnostock.qza[0m
    [32mSaved PCoAResults to: dsstrimmed-bray-curtis-pcoa-results-trimmed-ctrl-exptnostock.qza[0m
    [32mSaved Visualization to: dssunweighted-unifrac-emperor-trimmed-ctrl-exptnostock.qzv[0m
    [32mSaved Visualization to: dssweighted-unifrac-emperor-trimmed-ctrl-exptnostock.qzv[0m
    [32mSaved Visualization to: dssjaccard-emperor-trimmed-ctrl-exptnostock.qzv[0m
    [32mSaved Visualization to: dssbc-emperor-ctrl-exptnostock.qzv[0m



```bash
qiime diversity core-metrics-phylogenetic \
--i-phylogeny rooted-tree-trimmed_ctrl_expt.qza  \
--i-table ucphage-nodss-nostock-filtered-table_ctrl_expt.qza \
--p-sampling-depth 31455 \
--m-metadata-file /Users/anshulsinha/Desktop/Sequencing_analyses/Rainin_16S/rainin_16S_fall_2019_control_expt/metadata_ctrl.tsv \
--o-rarefied-table ucpnrarefied-table-trimmed-ctrl-exptnostock.qza \
--o-faith-pd-vector ucpnfaith-pd-trimmed-ctrl-exptnostock.qza \
--o-observed-features-vector ucpnobserved-otus-trimmed-ctrl-exptnostock.qza \
--o-shannon-vector ucpnshannon-vector-trimmed-ctrl-exptnostock.qza \
--o-evenness-vector ucpnevenness-vector-trimmed-ctrl-exptnostock.qza \
--o-unweighted-unifrac-distance-matrix ucpnunweighted-unifrac-distance-matrix-trimmed-ctrl-exptnostock.qza \
--o-weighted-unifrac-distance-matrix ucpnweighted-unifrac-distance-matrix-trimmed-ctrl-exptnostock.qza \
--o-jaccard-distance-matrix ucpnjaccard-distance-matrix-trimmed-ctrl-exptnostock.qza \
--o-bray-curtis-distance-matrix ucpnbray-curtis-distance-matrix-trimmed-ctrl-exptnostock.qza \
--o-unweighted-unifrac-pcoa-results ucpnunweighted-unifrac-pca-results-trimmed-ctrl-exptnostock.qza \
--o-weighted-unifrac-pcoa-results ucpnweighted-unifrac-pcoa-results-trimmed-ctrl-exptnostock.qza \
--o-jaccard-pcoa-results ucpnjaccard-pcoa-results-trimmed-trimmed-ctrl-exptnostock.qza \
--o-bray-curtis-pcoa-results ucpntrimmed-bray-curtis-pcoa-results-trimmed-ctrl-exptnostock.qza \
--o-unweighted-unifrac-emperor ucpnunweighted-unifrac-emperor-trimmed-ctrl-exptnostock.qzv \
--o-weighted-unifrac-emperor ucpnweighted-unifrac-emperor-trimmed-ctrl-exptnostock.qzv \
--o-jaccard-emperor ucpnjaccard-emperor-trimmed-ctrl-exptnostock.qzv \
--o-bray-curtis-emperor ucpnbc-emperor-ctrl-exptnostock.qzv
#filtered diversity analyses
```

    [32mSaved FeatureTable[Frequency] to: ucpnrarefied-table-trimmed-ctrl-exptnostock.qza[0m
    [32mSaved SampleData[AlphaDiversity] to: ucpnfaith-pd-trimmed-ctrl-exptnostock.qza[0m
    [32mSaved SampleData[AlphaDiversity] to: ucpnobserved-otus-trimmed-ctrl-exptnostock.qza[0m
    [32mSaved SampleData[AlphaDiversity] to: ucpnshannon-vector-trimmed-ctrl-exptnostock.qza[0m
    [32mSaved SampleData[AlphaDiversity] to: ucpnevenness-vector-trimmed-ctrl-exptnostock.qza[0m
    [32mSaved DistanceMatrix to: ucpnunweighted-unifrac-distance-matrix-trimmed-ctrl-exptnostock.qza[0m
    [32mSaved DistanceMatrix to: ucpnweighted-unifrac-distance-matrix-trimmed-ctrl-exptnostock.qza[0m
    [32mSaved DistanceMatrix to: ucpnjaccard-distance-matrix-trimmed-ctrl-exptnostock.qza[0m
    [32mSaved DistanceMatrix to: ucpnbray-curtis-distance-matrix-trimmed-ctrl-exptnostock.qza[0m
    [32mSaved PCoAResults to: ucpnunweighted-unifrac-pca-results-trimmed-ctrl-exptnostock.qza[0m
    [32mSaved PCoAResults to: ucpnweighted-unifrac-pcoa-results-trimmed-ctrl-exptnostock.qza[0m
    [32mSaved PCoAResults to: ucpnjaccard-pcoa-results-trimmed-trimmed-ctrl-exptnostock.qza[0m
    [32mSaved PCoAResults to: ucpntrimmed-bray-curtis-pcoa-results-trimmed-ctrl-exptnostock.qza[0m
    [32mSaved Visualization to: ucpnunweighted-unifrac-emperor-trimmed-ctrl-exptnostock.qzv[0m
    [32mSaved Visualization to: ucpnweighted-unifrac-emperor-trimmed-ctrl-exptnostock.qzv[0m
    [32mSaved Visualization to: ucpnjaccard-emperor-trimmed-ctrl-exptnostock.qzv[0m
    [32mSaved Visualization to: ucpnbc-emperor-ctrl-exptnostock.qzv[0m



```bash
qiime diversity core-metrics-phylogenetic \
--i-phylogeny rooted-tree-trimmed_ctrl_expt.qza  \
--i-table ucphage-yesdss-nostock-filtered-table_ctrl_expt.qza \
--p-sampling-depth 31455 \
--m-metadata-file /Users/anshulsinha/Desktop/Sequencing_analyses/Rainin_16S/rainin_16S_fall_2019_control_expt/metadata_ctrl.tsv \
--o-rarefied-table ucpyrarefied-table-trimmed-ctrl-exptnostock.qza \
--o-faith-pd-vector ucpyfaith-pd-trimmed-ctrl-exptnostock.qza \
--o-observed-features-vector ucpyobserved-otus-trimmed-ctrl-exptnostock.qza \
--o-shannon-vector ucpyshannon-vector-trimmed-ctrl-exptnostock.qza \
--o-evenness-vector ucpyevenness-vector-trimmed-ctrl-exptnostock.qza \
--o-unweighted-unifrac-distance-matrix ucpyunweighted-unifrac-distance-matrix-trimmed-ctrl-exptnostock.qza \
--o-weighted-unifrac-distance-matrix ucpyweighted-unifrac-distance-matrix-trimmed-ctrl-exptnostock.qza \
--o-jaccard-distance-matrix ucpyjaccard-distance-matrix-trimmed-ctrl-exptnostock.qza \
--o-bray-curtis-distance-matrix ucpybray-curtis-distance-matrix-trimmed-ctrl-exptnostock.qza \
--o-unweighted-unifrac-pcoa-results ucpyunweighted-unifrac-pca-results-trimmed-ctrl-exptnostock.qza \
--o-weighted-unifrac-pcoa-results ucpyweighted-unifrac-pcoa-results-trimmed-ctrl-exptnostock.qza \
--o-jaccard-pcoa-results ucpyjaccard-pcoa-results-trimmed-trimmed-ctrl-exptnostock.qza \
--o-bray-curtis-pcoa-results ucpytrimmed-bray-curtis-pcoa-results-trimmed-ctrl-exptnostock.qza \
--o-unweighted-unifrac-emperor ucpyunweighted-unifrac-emperor-trimmed-ctrl-exptnostock.qzv \
--o-weighted-unifrac-emperor ucpyweighted-unifrac-emperor-trimmed-ctrl-exptnostock.qzv \
--o-jaccard-emperor ucpyjaccard-emperor-trimmed-ctrl-exptnostock.qzv \
--o-bray-curtis-emperor ucpybc-emperor-ctrl-exptnostock.qzv
#filtered diversity analyses
```

    [32mSaved FeatureTable[Frequency] to: ucpyrarefied-table-trimmed-ctrl-exptnostock.qza[0m
    [32mSaved SampleData[AlphaDiversity] to: ucpyfaith-pd-trimmed-ctrl-exptnostock.qza[0m
    [32mSaved SampleData[AlphaDiversity] to: ucpyobserved-otus-trimmed-ctrl-exptnostock.qza[0m
    [32mSaved SampleData[AlphaDiversity] to: ucpyshannon-vector-trimmed-ctrl-exptnostock.qza[0m
    [32mSaved SampleData[AlphaDiversity] to: ucpyevenness-vector-trimmed-ctrl-exptnostock.qza[0m
    [32mSaved DistanceMatrix to: ucpyunweighted-unifrac-distance-matrix-trimmed-ctrl-exptnostock.qza[0m
    [32mSaved DistanceMatrix to: ucpyweighted-unifrac-distance-matrix-trimmed-ctrl-exptnostock.qza[0m
    [32mSaved DistanceMatrix to: ucpyjaccard-distance-matrix-trimmed-ctrl-exptnostock.qza[0m
    [32mSaved DistanceMatrix to: ucpybray-curtis-distance-matrix-trimmed-ctrl-exptnostock.qza[0m
    [32mSaved PCoAResults to: ucpyunweighted-unifrac-pca-results-trimmed-ctrl-exptnostock.qza[0m
    [32mSaved PCoAResults to: ucpyweighted-unifrac-pcoa-results-trimmed-ctrl-exptnostock.qza[0m
    [32mSaved PCoAResults to: ucpyjaccard-pcoa-results-trimmed-trimmed-ctrl-exptnostock.qza[0m
    [32mSaved PCoAResults to: ucpytrimmed-bray-curtis-pcoa-results-trimmed-ctrl-exptnostock.qza[0m
    [32mSaved Visualization to: ucpyunweighted-unifrac-emperor-trimmed-ctrl-exptnostock.qzv[0m
    [32mSaved Visualization to: ucpyweighted-unifrac-emperor-trimmed-ctrl-exptnostock.qzv[0m
    [32mSaved Visualization to: ucpyjaccard-emperor-trimmed-ctrl-exptnostock.qzv[0m
    [32mSaved Visualization to: ucpybc-emperor-ctrl-exptnostock.qzv[0m



```bash
qiime diversity core-metrics-phylogenetic \
--i-phylogeny rooted-tree-trimmed_ctrl_expt.qza  \
--i-table hkucphage-yesdss-nostock-filtered-table_ctrl_expt.qza \
--p-sampling-depth 31455 \
--m-metadata-file /Users/anshulsinha/Desktop/Sequencing_analyses/Rainin_16S/rainin_16S_fall_2019_control_expt/metadata_ctrl.tsv \
--o-rarefied-table hkucpyrarefied-table-trimmed-ctrl-exptnostock.qza \
--o-faith-pd-vector hkucpyfaith-pd-trimmed-ctrl-exptnostock.qza \
--o-observed-features-vector hkucpyobserved-otus-trimmed-ctrl-exptnostock.qza \
--o-shannon-vector hkucpyshannon-vector-trimmed-ctrl-exptnostock.qza \
--o-evenness-vector hkucpyevenness-vector-trimmed-ctrl-exptnostock.qza \
--o-unweighted-unifrac-distance-matrix hkucpyunweighted-unifrac-distance-matrix-trimmed-ctrl-exptnostock.qza \
--o-weighted-unifrac-distance-matrix hkucpyweighted-unifrac-distance-matrix-trimmed-ctrl-exptnostock.qza \
--o-jaccard-distance-matrix hkucpyjaccard-distance-matrix-trimmed-ctrl-exptnostock.qza \
--o-bray-curtis-distance-matrix hkucpybray-curtis-distance-matrix-trimmed-ctrl-exptnostock.qza \
--o-unweighted-unifrac-pcoa-results hkucpyunweighted-unifrac-pca-results-trimmed-ctrl-exptnostock.qza \
--o-weighted-unifrac-pcoa-results hkucpyweighted-unifrac-pcoa-results-trimmed-ctrl-exptnostock.qza \
--o-jaccard-pcoa-results hkucpyjaccard-pcoa-results-trimmed-trimmed-ctrl-exptnostock.qza \
--o-bray-curtis-pcoa-results hkucpytrimmed-bray-curtis-pcoa-results-trimmed-ctrl-exptnostock.qza \
--o-unweighted-unifrac-emperor hkucpyunweighted-unifrac-emperor-trimmed-ctrl-exptnostock.qzv \
--o-weighted-unifrac-emperor hkucpyweighted-unifrac-emperor-trimmed-ctrl-exptnostock.qzv \
--o-jaccard-emperor hkucpyjaccard-emperor-trimmed-ctrl-exptnostock.qzv \
--o-bray-curtis-emperor hkucpybc-emperor-ctrl-exptnostock.qzv
#filtered diversity analyses
```

    [32mSaved FeatureTable[Frequency] to: hkucpyrarefied-table-trimmed-ctrl-exptnostock.qza[0m
    [32mSaved SampleData[AlphaDiversity] to: hkucpyfaith-pd-trimmed-ctrl-exptnostock.qza[0m
    [32mSaved SampleData[AlphaDiversity] to: hkucpyobserved-otus-trimmed-ctrl-exptnostock.qza[0m
    [32mSaved SampleData[AlphaDiversity] to: hkucpyshannon-vector-trimmed-ctrl-exptnostock.qza[0m
    [32mSaved SampleData[AlphaDiversity] to: hkucpyevenness-vector-trimmed-ctrl-exptnostock.qza[0m
    [32mSaved DistanceMatrix to: hkucpyunweighted-unifrac-distance-matrix-trimmed-ctrl-exptnostock.qza[0m
    [32mSaved DistanceMatrix to: hkucpyweighted-unifrac-distance-matrix-trimmed-ctrl-exptnostock.qza[0m
    [32mSaved DistanceMatrix to: hkucpyjaccard-distance-matrix-trimmed-ctrl-exptnostock.qza[0m
    [32mSaved DistanceMatrix to: hkucpybray-curtis-distance-matrix-trimmed-ctrl-exptnostock.qza[0m
    [32mSaved PCoAResults to: hkucpyunweighted-unifrac-pca-results-trimmed-ctrl-exptnostock.qza[0m
    [32mSaved PCoAResults to: hkucpyweighted-unifrac-pcoa-results-trimmed-ctrl-exptnostock.qza[0m
    [32mSaved PCoAResults to: hkucpyjaccard-pcoa-results-trimmed-trimmed-ctrl-exptnostock.qza[0m
    [32mSaved PCoAResults to: hkucpytrimmed-bray-curtis-pcoa-results-trimmed-ctrl-exptnostock.qza[0m
    [32mSaved Visualization to: hkucpyunweighted-unifrac-emperor-trimmed-ctrl-exptnostock.qzv[0m
    [32mSaved Visualization to: hkucpyweighted-unifrac-emperor-trimmed-ctrl-exptnostock.qzv[0m
    [32mSaved Visualization to: hkucpyjaccard-emperor-trimmed-ctrl-exptnostock.qzv[0m
    [32mSaved Visualization to: hkucpybc-emperor-ctrl-exptnostock.qzv[0m



```bash
qiime diversity alpha-group-significance \
--i-alpha-diversity colfaith-pd-trimmed-ctrl-exptnostock.qza \
--m-metadata-file /Users/anshulsinha/Desktop/Sequencing_analyses/Rainin_16S/rainin_16S_fall_2019_control_expt/metadata_ctrl.tsv \
--o-visualization faiths-col.qzv 
#filtered alpha diversity 
```

    [32mSaved Visualization to: faiths-col.qzv[0m



```bash
qiime diversity alpha-group-significance \
--i-alpha-diversity gavfaith-pd-trimmed-ctrl-exptnostock.qza \
--m-metadata-file /Users/anshulsinha/Desktop/Sequencing_analyses/Rainin_16S/rainin_16S_fall_2019_control_expt/metadata_ctrl.tsv \
--o-visualization faiths-gav.qzv 
#filtered alpha diversity 
```

    [32mSaved Visualization to: faiths-gav.qzv[0m



```bash
qiime diversity alpha-group-significance \
--i-alpha-diversity dssfaith-pd-trimmed-ctrl-exptnostock.qza \
--m-metadata-file /Users/anshulsinha/Desktop/Sequencing_analyses/Rainin_16S/rainin_16S_fall_2019_control_expt/metadata_ctrl.tsv \
--o-visualization faiths-dss.qzv 
#filtered alpha diversity 
```

    [32mSaved Visualization to: faiths-dss.qzv[0m



```bash
qiime diversity alpha-group-significance \
--i-alpha-diversity ucpyfaith-pd-trimmed-ctrl-exptnostock.qza \
--m-metadata-file /Users/anshulsinha/Desktop/Sequencing_analyses/Rainin_16S/rainin_16S_fall_2019_control_expt/metadata_ctrl.tsv \
--o-visualization faiths-ucpy.qzv 
#filtered alpha diversity 
```

    [32mSaved Visualization to: faiths-ucpy.qzv[0m



```bash
qiime diversity alpha-group-significance \
--i-alpha-diversity hkucpyfaith-pd-trimmed-ctrl-exptnostock.qza \
--m-metadata-file /Users/anshulsinha/Desktop/Sequencing_analyses/Rainin_16S/rainin_16S_fall_2019_control_expt/metadata_ctrl.tsv \
--o-visualization hkfaiths-ucpy.qzv 
#filtered alpha diversity 
```

    [32mSaved Visualization to: hkfaiths-ucpy.qzv[0m



```bash
qiime diversity alpha-group-significance \
--i-alpha-diversity  colshannon-vector-trimmed-ctrl-exptnostock.qza \
--m-metadata-file /Users/anshulsinha/Desktop/Sequencing_analyses/Rainin_16S/rainin_16S_fall_2019_control_expt/metadata_ctrl.tsv \
--o-visualization shannon-col.qzv 

#filtered alpha diversity 
```

    [32mSaved Visualization to: shannon-col.qzv[0m



```bash
qiime diversity alpha-group-significance \
--i-alpha-diversity  gavshannon-vector-trimmed-ctrl-exptnostock.qza \
--m-metadata-file /Users/anshulsinha/Desktop/Sequencing_analyses/Rainin_16S/rainin_16S_fall_2019_control_expt/metadata_ctrl.tsv \
--o-visualization shannon-gav.qzv 
#filtered alpha diversity 

```

    [32mSaved Visualization to: shannon-gav.qzv[0m



```bash
qiime diversity alpha-group-significance \
--i-alpha-diversity  dssshannon-vector-trimmed-ctrl-exptnostock.qza \
--m-metadata-file /Users/anshulsinha/Desktop/Sequencing_analyses/Rainin_16S/rainin_16S_fall_2019_control_expt/metadata_ctrl.tsv \
--o-visualization shannon-dss.qzv 

#filtered alpha diversity 
```

    [32mSaved Visualization to: shannon-dss.qzv[0m



```bash
qiime diversity alpha-group-significance \
--i-alpha-diversity  ucpnshannon-vector-trimmed-ctrl-exptnostock.qza \
--m-metadata-file /Users/anshulsinha/Desktop/Sequencing_analyses/Rainin_16S/rainin_16S_fall_2019_control_expt/metadata_ctrl.tsv \
--o-visualization shannon-ucpn.qzv 
#filtered alpha diversity 
```

    [32mSaved Visualization to: shannon-ucpn.qzv[0m



```bash
qiime diversity alpha-group-significance \
--i-alpha-diversity  ucpyshannon-vector-trimmed-ctrl-exptnostock.qza \
--m-metadata-file /Users/anshulsinha/Desktop/Sequencing_analyses/Rainin_16S/rainin_16S_fall_2019_control_expt/metadata_ctrl.tsv \
--o-visualization shannon-ucpy.qzv 
#filtered alpha diversity 
```

    [32mSaved Visualization to: shannon-ucpy.qzv[0m



```bash
qiime diversity alpha-group-significance \
--i-alpha-diversity  hkucpyshannon-vector-trimmed-ctrl-exptnostock.qza \
--m-metadata-file /Users/anshulsinha/Desktop/Sequencing_analyses/Rainin_16S/rainin_16S_fall_2019_control_expt/metadata_ctrl.tsv \
--o-visualization hkshannon-ucpy.qzv 
#filtered alpha diversity 
```

    [32mSaved Visualization to: hkshannon-ucpy.qzv[0m



```bash
qiime diversity beta-group-significance \
--i-distance-matrix  colweighted-unifrac-distance-matrix-trimmed-ctrl-exptnostock.qza \
--m-metadata-file  /Users/anshulsinha/Desktop/Sequencing_analyses/Rainin_16S/rainin_16S_fall_2019_control_expt/metadata_ctrl.tsv \
--m-metadata-column Treatment \
--o-visualization wunifracbac-col-filtered-betasig-trimmed.qzv \
--p-pairwise
#filtered alpha diversity 
```

    [32mSaved Visualization to: wunifracbac-col-filtered-betasig-trimmed.qzv[0m



```bash
qiime tools view wunifracbac-col-filtered-betasig-trimmed.qzv
```

    Press the 'q' key, Control-C, or Control-D to quit. This view may no longer be accessible or work correctly after quitting.


```bash
qiime diversity beta-group-significance \
--i-distance-matrix  colbray-curtis-distance-matrix-trimmed-ctrl-exptnostock.qza \
--m-metadata-file /Users/anshulsinha/Desktop/Sequencing_analyses/Rainin_16S/rainin_16S_fall_2019_control_expt/metadata_ctrl.tsv \
--m-metadata-column Treatment \
--o-visualization bc-col-filtered-betasig-trimmed.qzv \
--p-pairwise
#filtered alpha diversity 
```

    [32mSaved Visualization to: bc-col-filtered-betasig-trimmed.qzv[0m



```bash
qiime diversity beta-group-significance \
--i-distance-matrix  gavweighted-unifrac-distance-matrix-trimmed-ctrl-exptnostock.qza \
--m-metadata-file  /Users/anshulsinha/Desktop/Sequencing_analyses/Rainin_16S/rainin_16S_fall_2019_control_expt/metadata_ctrl.tsv \
--m-metadata-column Treatment \
--o-visualization wunifracbac-gav-filtered-betasig-trimmed.qzv \
--p-pairwise
#filtered alpha diversity 
```

    [32mSaved Visualization to: wunifracbac-gav-filtered-betasig-trimmed.qzv[0m



```bash
qiime diversity beta-group-significance \
--i-distance-matrix  gavbray-curtis-distance-matrix-trimmed-ctrl-exptnostock.qza \
--m-metadata-file   /Users/anshulsinha/Desktop/Sequencing_analyses/Rainin_16S/rainin_16S_fall_2019_control_expt/metadata_ctrl.tsv \
--m-metadata-column Treatment \
--o-visualization bc-gav-filtered-betasig-trimmed.qzv \
--p-pairwise
#filtered alpha diversity 
```

    [32mSaved Visualization to: bc-gav-filtered-betasig-trimmed.qzv[0m



```bash
qiime diversity beta-group-significance \
--i-distance-matrix  dssweighted-unifrac-distance-matrix-trimmed-ctrl-exptnostock.qza \
--m-metadata-file  /Users/anshulsinha/Desktop/Sequencing_analyses/Rainin_16S/rainin_16S_fall_2019_control_expt/metadata_ctrl.tsv \
--m-metadata-column Treatment \
--o-visualization wunifracbac-dss-filtered-betasig-trimmed.qzv \
--p-pairwise
#filtered alpha diversity 
```

    [32mSaved Visualization to: wunifracbac-dss-filtered-betasig-trimmed.qzv[0m



```bash
qiime tools view wunifracbac-dss-filtered-betasig-trimmed.qzv
```

    Press the 'q' key, Control-C, or Control-D to quit. This view may no longer be accessible or work correctly after quitting.


```bash
qiime diversity beta-group-significance \
--i-distance-matrix  dssbray-curtis-distance-matrix-trimmed-ctrl-exptnostock.qza \
--m-metadata-file   /Users/anshulsinha/Desktop/Sequencing_analyses/Rainin_16S/rainin_16S_fall_2019_control_expt/metadata_ctrl.tsv \
--m-metadata-column Treatment \
--o-visualization braycurtis-dss-filtered-betasig-trimmed.qzv \
--p-pairwise
#filtered alpha diversity 
```

    [32mSaved Visualization to: braycurtis-dss-filtered-betasig-trimmed.qzv[0m



```bash
qiime diversity beta-group-significance \
--i-distance-matrix  ucpnweighted-unifrac-distance-matrix-trimmed-ctrl-exptnostock.qza \
--m-metadata-file   /Users/anshulsinha/Desktop/Sequencing_analyses/Rainin_16S/rainin_16S_fall_2019_control_expt/metadata_ctrl.tsv \
--m-metadata-column Period \
--o-visualization weighteduni-ucpn-filtered-betasig-trimmed.qzv \
--p-pairwise
#filtered alpha diversity 
```

    [32mSaved Visualization to: weighteduni-ucpn-filtered-betasig-trimmed.qzv[0m



```bash

```


```bash
qiime diversity beta-group-significance \
--i-distance-matrix  ucpnbray-curtis-distance-matrix-trimmed-ctrl-exptnostock.qza \
--m-metadata-file   /Users/anshulsinha/Desktop/Sequencing_analyses/Rainin_16S/rainin_16S_fall_2019_control_expt/metadata_ctrl.tsv \
--m-metadata-column Period \
--o-visualization bc-ucpn-filtered-betasig-trimmed.qzv \
--p-pairwise
#filtered alpha diversity 
```

    [32mSaved Visualization to: bc-ucpn-filtered-betasig-trimmed.qzv[0m



```bash
qiime diversity beta-group-significance \
--i-distance-matrix  hkucpyweighted-unifrac-distance-matrix-trimmed-ctrl-exptnostock.qza \
--m-metadata-file   /Users/anshulsinha/Desktop/Sequencing_analyses/Rainin_16S/rainin_16S_fall_2019_control_expt/metadata_ctrl.tsv \
--m-metadata-column Period \
--o-visualization weighteduni-hkucpy-filtered-betasig-trimmed.qzv \
--p-pairwise
#filtered alpha diversity 
```

    [32mSaved Visualization to: weighteduni-hkucpy-filtered-betasig-trimmed.qzv[0m



```bash
qiime diversity beta-group-significance \
--i-distance-matrix  hkucpybray-curtis-distance-matrix-trimmed-ctrl-exptnostock.qza \
--m-metadata-file   /Users/anshulsinha/Desktop/Sequencing_analyses/Rainin_16S/rainin_16S_fall_2019_control_expt/metadata_ctrl.tsv \
--m-metadata-column Period \
--o-visualization bc-hkucpy-filtered-betasig-trimmed.qzv \
--p-pairwise
#filtered alpha diversity 
```

    [32mSaved Visualization to: bc-hkucpy-filtered-betasig-trimmed.qzv[0m



```bash
qiime diversity beta-group-significance \
--i-distance-matrix  ucpyweighted-unifrac-distance-matrix-trimmed-ctrl-exptnostock.qza \
--m-metadata-file   /Users/anshulsinha/Desktop/Sequencing_analyses/Rainin_16S/rainin_16S_fall_2019_control_expt/metadata_ctrl.tsv \
--m-metadata-column Period \
--o-visualization weighteduni-ucpy-filtered-betasig-trimmed.qzv \
--p-pairwise
#filtered alpha diversity 
```

    [32mSaved Visualization to: weighteduni-ucpy-filtered-betasig-trimmed.qzv[0m



```bash
qiime diversity beta-group-significance \
--i-distance-matrix  ucpybray-curtis-distance-matrix-trimmed-ctrl-exptnostock.qza \
--m-metadata-file /Users/anshulsinha/Desktop/Sequencing_analyses/Rainin_16S/rainin_16S_fall_2019_control_expt/metadata_ctrl.tsv \
--o-visualization bc-ucpy-filtered-betasig-trimmed.qzv \
--p-pairwise
#filtered alpha diversity 
```

    Usage: [34mqiime diversity beta-group-significance[0m [OPTIONS]
    
      Determine whether groups of samples are significantly different from one
      another using a permutation-based statistical test.
    
    [1mInputs[0m:
      [34m[4m--i-distance-matrix[0m ARTIFACT
        [32mDistanceMatrix[0m     Matrix of distances between pairs of samples.
                                                                        [35m[required][0m
    [1mParameters[0m:
      [34m[4m--m-metadata-file[0m METADATA
      [34m[4m--m-metadata-column[0m COLUMN  [32mMetadataColumn[Categorical][0m
                           Categorical sample metadata column.          [35m[required][0m
      [34m--p-method[0m TEXT [32mChoices('permanova', 'anosim', 'permdisp')[0m
                           The group significance test to be applied.
                                                            [35m[default: 'permanova'][0m
      [34m--p-pairwise[0m / [34m--p-no-pairwise[0m
                           Perform pairwise tests between all pairs of groups in
                           addition to the test across all groups. This can be
                           very slow if there are a lot of groups in the metadata
                           column.                                [35m[default: False][0m
      [34m--p-permutations[0m INTEGER
                           The number of permutations to be run when computing
                           p-values.                                [35m[default: 999][0m
    [1mOutputs[0m:
      [34m[4m--o-visualization[0m VISUALIZATION
                                                                        [35m[required][0m
    [1mMiscellaneous[0m:
      [34m--output-dir[0m PATH    Output unspecified results to a directory
      [34m--verbose[0m / [34m--quiet[0m  Display verbose output to stdout and/or stderr during
                           execution of this action. Or silence output if
                           execution is successful (silence is golden).
      [34m--examples[0m           Show usage examples and exit.
      [34m--citations[0m          Show citations and exit.
      [34m--help[0m               Show this message and exit.
    
    [33m                    There was a problem with the command:                     [0m
    [31m[1m (1/1) Missing option '--m-metadata-column'.[0m





```bash
qiime feature-classifier classify-sklearn \
--i-classifier silva-138-99-515-806-nb-classifier.qza \
--i-reads rep-seqs-trimmed_ctrl_expt.qza \
--o-classification taxonomy.qza 
#using Silva db for classification and outputting taxonomy artifact
```

    [32mSaved FeatureData[Taxonomy] to: taxonomy.qza[0m
    (qiime2-2020.6) 




```bash
qiime metadata tabulate \
--m-input-file taxonomy.qza \
--o-visualization taxonomy.qzv 

```

    [32mSaved Visualization to: taxonomy.qzv[0m



```bash
qiime taxa collapse \
--i-table col-nostock-filtered-table_ctrl_expt.qza \
--i-taxonomy taxonomy.qza \
--p-level 7 \
--o-collapsed-table colspecies-table.qza
#Collapsing taxonomy table to species level 
```

    [32mSaved FeatureTable[Frequency] to: colspecies-table.qza[0m



```bash
qiime composition add-pseudocount \
--i-table colspecies-table.qza \
--o-composition-table col-species-comp-table.qza
#adding pseudocount for ANCOM
```

    [32mSaved FeatureTable[Composition] to: col-species-comp-table.qza[0m



```bash
qiime composition ancom \
--i-table col-species-comp-table.qza  \
--m-metadata-file /Users/anshulsinha/Desktop/Sequencing_analyses/Rainin_16S/rainin_16S_fall_2019_control_expt/metadata_ctrl_experiment.txt \
--m-metadata-column Treatment \
--o-visualization ancom-species-trimmed-col.qzv
#filtered ancom
```

    [32mSaved Visualization to: ancom-species-trimmed-col.qzv[0m



```bash
qiime taxa collapse \
--i-table gav-nostock-filtered-table_ctrl_expt.qza \
--i-taxonomy taxonomy.qza \
--p-level 7 \
--o-collapsed-table gavspecies-table.qza
#Collapsing taxonomy table to species level 
```

    [32mSaved FeatureTable[Frequency] to: gavspecies-table.qza[0m



```bash
qiime tools view ancom-species-trimmed-gav.qzv
```

    Press the 'q' key, Control-C, or Control-D to quit. This view may no longer be accessible or work correctly after quitting.


```bash
qiime composition add-pseudocount \
--i-table gavspecies-table.qza \
--o-composition-table gav-species-comp-table.qza
#adding pseudocount for ANCOM
```

    [32mSaved FeatureTable[Composition] to: gav-species-comp-table.qza[0m



```bash
qiime composition ancom \
--i-table gav-species-comp-table.qza  \
--m-metadata-file /Users/anshulsinha/Desktop/Sequencing_analyses/Rainin_16S/rainin_16S_fall_2019_control_expt/metadata_ctrl_experiment.txt \
--m-metadata-column Treatment \
--o-visualization ancom-species-trimmed-gav.qzv \
#filtered ancom
```

    [32mSaved Visualization to: ancom-species-trimmed-gav.qzv[0m



```bash
qiime taxa collapse \
--i-table dss-nostock-filtered-table_ctrl_expt.qza \
--i-taxonomy taxonomy.qza \
--p-level 7 \
--o-collapsed-table dssspecies-table.qza
#Collapsing taxonomy table to species level 
```

    [32mSaved FeatureTable[Frequency] to: dssspecies-table.qza[0m



```bash
qiime composition add-pseudocount \
--i-table dssspecies-table.qza \
--o-composition-table dss-species-comp-table.qza
#adding pseudocount for ANCOM
```

    [32mSaved FeatureTable[Composition] to: dss-species-comp-table.qza[0m



```bash
qiime composition ancom \
--i-table dss-species-comp-table.qza  \
--m-metadata-file /Users/anshulsinha/Desktop/Sequencing_analyses/Rainin_16S/rainin_16S_fall_2019_control_expt/metadata_ctrl_experiment.txt \
--m-metadata-column Treatment \
--o-visualization ancom-species-trimmed-dss.qzv
#filtered ANCOM
```

    [32mSaved Visualization to: ancom-species-trimmed-dss.qzv[0m



```bash
qiime feature-table group  \
--i-table pooled-stocks-filtered-table_ctrl_expt.qza \
--p-axis sample \
--m-metadata-file /Users/anshulsinha/Desktop/Sequencing_analyses/Rainin_16S/rainin_16S_fall_2019_control_expt/metadata_ctrl_experiment.txt \
--m-metadata-column Treatment \
--p-mode sum \
--o-grouped-table pooled-stocks-grouped-table.qza

#Pooled stocks grouped feature table


```

    [32mSaved FeatureTable[Frequency] to: pooled-stocks-grouped-table.qza[0m



```bash
qiime taxa barplot \
--i-table pooled-stocks-grouped-table.qza \
--i-taxonomy taxonomy.qza \
--m-metadata-file /Users/anshulsinha/Desktop/Sequencing_analyses/Rainin_16S/rainin_16S_fall_2019_control_expt/metadata_ctrl_stock_treatments.tsv \
--o-visualization taxa-bar-plots-pooled-stocks.qzv
#col stocks bar-plot
```

    [32mSaved Visualization to: taxa-bar-plots-pooled-stocks.qzv[0m



```bash
qiime tools view taxa-bar-plots-pooled-stocks.qzv
```


```bash
qiime taxa collapse \
--i-table table_stocks.qza \
--i-taxonomy taxonomy.qza \
--p-level 7 \
--o-collapsed-table species-table.qza
#collapsing species for ALL samples 
```

    [32mSaved FeatureTable[Frequency] to: species-table.qza[0m



```bash
qiime longitudinal feature-volatility  \
--i-table species-table.qza \
--m-metadata-file /Users/anshulsinha/Desktop/Sequencing_analyses/Rainin_16S/rainin_16S_fall_2019_control_expt/metadata_ctrl_experiment.txt \
--p-state-column Date \
--p-estimator RandomForestRegressor \
--p-n-jobs 4 \
--p-n-estimators 400 \
--o-filtered-table species-feature-vol-filtered-table-trimmed.qza \
--o-feature-importance species-feature-vol-importance-trimmed.qza \
--o-volatility-plot species-feature-vol-plot-trimmed.qzv \
--o-accuracy-results species-accuracy-results-feature-vol-trimmed.qzv \
--o-sample-estimator species-sample-estimator-feature-vol-trimmed.qza 
#Feature volatility at species level- shows how each species changes over time 
```

    [32mSaved FeatureTable[RelativeFrequency] to: species-feature-vol-filtered-table-trimmed.qza[0m
    [32mSaved FeatureData[Importance] to: species-feature-vol-importance-trimmed.qza[0m
    [32mSaved Visualization to: species-feature-vol-plot-trimmed.qzv[0m
    [32mSaved Visualization to: species-accuracy-results-feature-vol-trimmed.qzv[0m
    [32mSaved SampleEstimator[Regressor] to: species-sample-estimator-feature-vol-trimmed.qza[0m



```bash

```
