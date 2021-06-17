```bash
source activate qiime2-2020.2
```

    xcrun: error: invalid active developer path (/Library/Developer/CommandLineTools), missing xcrun at: /Library/Developer/CommandLineTools/usr/bin/xcrun
    (qiime2-2020.2) 




```bash
cd /Users/anshul.sinha/Desktop/Sequencing_analyses/Rainin_16S/Rainin_pooled_expt1_expt2_inoculum
```

    (qiime2-2020.2) 




```bash
qiime tools import \
 --type 'SampleData[PairedEndSequencesWithQuality]'\
 --input-path /Users/anshul.sinha/Desktop/Sequencing_analyses/Rainin_pooled_expt1_expt2_inoculum/fastQ/rainin_manifest_pooled.csv \
 --output-path paired-end-demux-pooled.qza \
 --input-format PairedEndFastqManifestPhred33
 
 #Importing seqs from both trials of the experiment shown in Fig. 1B
 
```


```bash
qiime cutadapt trim-paired \
--i-demultiplexed-sequences /Users/anshul.sinha/Desktop/Sequencing_analyses/Rainin_16S/Rainin_pooled_expt1_expt2_inoculumRainin_pooled_expt1_expt2_inoculum/fastQ/paired-end-demux-pooled.qza \
--p-cores 4 \
--p-front-f GTGCCAGCMGCCGCGGTAA \
--p-front-r GGACTACHVGGGTWTCTAAT \
--o-trimmed-sequences paired-end-demux-trimmed-pooled.qza

#This command will cut everything before the forward primers or after reverse primer sequences
#type zless and then copy your file path to see if sequences are removed
```


```bash
qiime tools export \
--input-path paired-end-demux-trimmed.qza \
--output-path exported-trimmed-seqs
#export trimmed seqs then zless file path to see if primers are still there
```


```bash
qiime demux summarize \
--i-data paired-end-demux-trimmed-pooled.qza \
--o-visualization paired-end-demux-pooled-trimmed.qzv
```

    [32mSaved Visualization to: paired-end-demux-pooled-trimmed.qzv[0m



```bash
qiime dada2 denoise-paired \
--i-demultiplexed-seqs paired-end-demux-trimmed-pooled.qza \
--o-table table-pooled-2019.qza \
--o-representative-sequences rep-seqs-trimmed-pooled-2019.qza \
--p-trunc-len-f 175 \
--p-trunc-len-r 175 \
--p-min-fold-parent-over-abundance 5 \
--p-n-threads 0 \
--o-denoising-stats stats-dada2-winter-pooled-2019.qza
#trimming seqs based on quality and running dada2

```

    [32mSaved FeatureTable[Frequency] to: table-pooled-2019.qza[0m
    [32mSaved FeatureData[Sequence] to: rep-seqs-trimmed-pooled-2019.qza[0m
    [32mSaved SampleData[DADA2Stats] to: stats-dada2-winter-pooled-2019.qza[0m



```bash
qiime metadata tabulate \
--m-input-file stats-dada2-winter-pooled-2019.qza \
--o-visualization stats-dada2-trimmed-pooled.qzv

```

    [32mSaved Visualization to: stats-dada2-trimmed-pooled.qzv[0m



```bash
qiime feature-table summarize \
 --i-table table-pooled-2019.qza  \
 --o-visualization table-winter-pooled.qzv \
 --m-sample-metadata-file rainin_metadata_file_pooled_2019.tsv \

#Feature table associates the metadata with each ASV - ie- How many reads of ASV X are found in Sample Y

```

    [32mSaved Visualization to: table-winter-pooled.qzv[0m



```bash
qiime feature-table filter-features \
  --i-table table-pooled-2019.qza \
  --p-min-frequency 10 \
  --o-filtered-table table-pooled-trimmed.qza
#filtering ASVs present at read counts below 10 

```

    [32mSaved FeatureTable[Frequency] to: table-pooled-trimmed.qza[0m



```bash
qiime phylogeny align-to-tree-mafft-fasttree \
 --i-sequences rep-seqs-trimmed-pooled-2019.qza \
 --o-alignment aligned-rep-seqs-trimmed-pooled-2019.qza \
 --o-masked-alignment masked-aligned-rep-seqs-trimmed-pooled-2019.qza \
 --o-tree unrooted-tree-trimmed-pooled-2019.qza \
 --o-rooted-tree rooted-tree-trimmed-pooled.qza
#For the diversity metrics that rely on phylogeny ie. UniFrac, maaft performs a multiple alignment between ASVs
#Next the pipeline removes highly variable positions, which add noise to the phylogenetic tree
#Then the fasttree program creates a tree from the masked alignment
```

    [32mSaved FeatureData[AlignedSequence] to: aligned-rep-seqs-trimmed-pooled-2019.qza[0m
    [32mSaved FeatureData[AlignedSequence] to: masked-aligned-rep-seqs-trimmed-pooled-2019.qza[0m
    [32mSaved Phylogeny[Unrooted] to: unrooted-tree-trimmed-pooled-2019.qza[0m
    [32mSaved Phylogeny[Rooted] to: rooted-tree-trimmed-pooled.qza[0m



```bash
qiime feature-table filter-samples \
--i-table table-pooled-trimmed.qza \
--m-metadata-file rainin_metadata_file_pooled_2019.tsv \
--p-where "Experiment= '1'" \
--o-filtered-table expt1-filtered-table-pooled.qza

#filtering samples here for just the 1st experiment
```

    [32mSaved FeatureTable[Frequency] to: expt1-filtered-table-pooled.qza[0m



```bash
qiime feature-table filter-samples \
--i-table table-pooled-trimmed.qza \
--m-metadata-file rainin_metadata_file_pooled_2019.tsv \
--p-where "Experiment= '2'" \
--o-filtered-table expt2-filtered-table-pooled.qza
#filtering samples here for just the 2nd experiment
```

    [32mSaved FeatureTable[Frequency] to: expt2-filtered-table-pooled.qza[0m



```bash
qiime feature-table filter-samples \
--i-table expt2-filtered-table-pooled.qza \
--m-metadata-file rainin_metadata_file_pooled_2019.tsv \
--p-where "Treatment= 'No phage'" \
--o-filtered-table np-filtered-table-pooled-f1-expt2.qza

qiime feature-table filter-features \
  --i-table np-filtered-table-pooled-f1-expt2.qza \
  --p-min-samples 2 \
  --o-filtered-table np-filtered-table-trimmed-pooled-expt2.qza
  #filtering samples in the 2nd experiment for PBS control treatment
```

    [32mSaved FeatureTable[Frequency] to: np-filtered-table-pooled-f1-expt2.qza[0m
    [32mSaved FeatureTable[Frequency] to: np-filtered-table-trimmed-pooled-expt2.qza[0m



```bash
qiime feature-table filter-samples \
--i-table expt2-filtered-table-pooled.qza \
--m-metadata-file rainin_metadata_file_pooled_2019.tsv \
--p-where "Treatment= 'Healthy phage'" \
--o-filtered-table hp-filtered-table-pooled-f1-expt2.qza

qiime feature-table filter-features \
  --i-table hp-filtered-table-pooled-f1-expt2.qza \
  --p-min-samples 2 \
  --o-filtered-table hp-filtered-table-trimmed-pooled-expt2.qza
    #filtering samples in the 2nd experiment for HP treatment
```

    [32mSaved FeatureTable[Frequency] to: hp-filtered-table-pooled-f1-expt2.qza[0m
    [32mSaved FeatureTable[Frequency] to: hp-filtered-table-trimmed-pooled-expt2.qza[0m



```bash
qiime feature-table filter-samples \
--i-table expt2-filtered-table-pooled.qza \
--m-metadata-file rainin_metadata_file_pooled_2019.tsv \
--p-where "Treatment= 'UC phage'" \
--o-filtered-table uc-filtered-table-pooled-f1-expt2.qza

qiime feature-table filter-features \
  --i-table uc-filtered-table-pooled-f1-expt2.qza \
  --p-min-samples 2 \
  --o-filtered-table uc-filtered-table-trimmed-pooled-expt2.qza
      #filtering samples in the 2nd experiment for UC treatment
```

    [32mSaved FeatureTable[Frequency] to: uc-filtered-table-pooled-f1-expt2.qza[0m
    [32mSaved FeatureTable[Frequency] to: uc-filtered-table-trimmed-pooled-expt2.qza[0m



```bash
qiime feature-table filter-samples \
--i-table expt1-filtered-table-pooled.qza \
--m-metadata-file rainin_metadata_file_pooled_2019.tsv \
--p-where "Treatment= 'No phage'" \
--o-filtered-table np-filtered-table-pooled-f1-expt1.qza

qiime feature-table filter-features \
  --i-table np-filtered-table-pooled-f1-expt1.qza \
  --p-min-samples 2 \
  --o-filtered-table np-filtered-table-trimmed-pooled-expt1.qza
  
    #filtering samples in the 1st experiment for PBS control treatment
```

    [32mSaved FeatureTable[Frequency] to: np-filtered-table-pooled-f1-expt1.qza[0m
    [32mSaved FeatureTable[Frequency] to: np-filtered-table-trimmed-pooled-expt1.qza[0m



```bash
qiime feature-table filter-samples \
--i-table expt1-filtered-table-pooled.qza \
--m-metadata-file rainin_metadata_file_pooled_2019.tsv \
--p-where "Treatment= 'Healthy phage'" \
--o-filtered-table hp-filtered-table-pooled-f1-expt1.qza

qiime feature-table filter-features \
  --i-table hp-filtered-table-pooled-f1-expt1.qza \
  --p-min-samples 2 \
  --o-filtered-table hp-filtered-table-trimmed-pooled-expt1.qza
      #filtering samples in the 1st experiment for HP treatment
```

    [32mSaved FeatureTable[Frequency] to: hp-filtered-table-pooled-f1-expt1.qza[0m
    [32mSaved FeatureTable[Frequency] to: hp-filtered-table-trimmed-pooled-expt1.qza[0m



```bash
qiime feature-table filter-samples \
--i-table expt1-filtered-table-pooled.qza \
--m-metadata-file rainin_metadata_file_pooled_2019.tsv \
--p-where "Treatment= 'UC phage'" \
--o-filtered-table uc-filtered-table-pooled-f1-expt1.qza

qiime feature-table filter-features \
  --i-table uc-filtered-table-pooled-f1-expt1.qza \
  --p-min-samples 2 \
  --o-filtered-table uc-filtered-table-trimmed-pooled-expt1.qza
        #filtering samples in the 1st experiment for UC treatment
```

    [32mSaved FeatureTable[Frequency] to: uc-filtered-table-pooled-f1-expt1.qza[0m
    [32mSaved FeatureTable[Frequency] to: uc-filtered-table-trimmed-pooled-expt1.qza[0m



```bash
qiime feature-table merge \
  --i-tables np-filtered-table-trimmed-pooled-expt1.qza \
  --i-tables hp-filtered-table-trimmed-pooled-expt1.qza \
  --i-tables uc-filtered-table-trimmed-pooled-expt1.qza \
  --o-merged-table merged-expt1-no-ic.qza
    #merged and filtered table for experiment 1
```

    [32mSaved FeatureTable[Frequency] to: merged-expt1-no-ic.qza[0m



```bash
qiime feature-classifier classify-sklearn \
--i-classifier silva-132-99-515-806-nb-classifier.qza \
--i-reads rep-seqs-trimmed-pooled-2019.qza \
--o-classification taxonomy-trimmed.qza
#assigning taxononmy to reads 
```


```bash
qiime metadata tabulate \
--m-input-file taxonomy-trimmed.qza \
--o-visualization taxonomy-trimmed.qzv


```


```bash
qiime taxa collapse \
--i-table merged-expt1-no-ic.qza \
--i-taxonomy taxonomy-trimmed.qza \
--p-level 7 \
--o-collapsed-table collapsed-species-expt1.qza
#Collapsing all taxa to the species level- for use in qiime longitudinal 
```

    [32mSaved FeatureTable[Frequency] to: collapsed-species-expt1.qza[0m



```bash
qiime taxa collapse \
--i-table merged-expt2-noic.qza \
--i-taxonomy taxonomy-trimmed.qza \
--p-level 7 \
--o-collapsed-table collapsed-species-expt2.qza
#For use in qiime longitudinal 
```

    [32mSaved FeatureTable[Frequency] to: collapsed-species-expt2.qza[0m



```bash
qiime longitudinal feature-volatility \
--i-table collapsed-species-expt1.qza \
--m-metadata-file rainin_metadata_file_pooled_2019.tsv \
--p-state-column Date \
--p-individual-id-column Cage \
--p-estimator KNeighborsRegressor \
--p-n-jobs 4 \
--p-n-estimators 400 \
--o-filtered-table expt1species-feature-vol-filtered-table-trimmed-w.qza \
--o-feature-importance expt1species-feature-vol-importance-trimmed-w.qza \
--o-volatility-plot expt1species-feature-vol-plot-trimmed-w.qzv \
--o-accuracy-results expt1species-accuracy-results-feature-vol-trimmed-w.qzv \
--o-sample-estimator expt1species-sample-estimator-feature-vol-trimmed-w.qza

#Feature volatility- species level for expt 1
```


```bash
qiime feature-table filter-samples \
--i-table  merged-expt1-no-ic.qza  \
--m-metadata-file rainin_metadata_file_pooled_2019.tsv \
--p-where "Period= 'Colonization'" \
--o-filtered-table col-filtered-table-expt1-noic.qza
#all samples in the bacterial colonization period in experiment #1 
```

    
    Aborted!
    (qiime2-2020.2) 


```bash
qiime diversity core-metrics-phylogenetic \
  --i-phylogeny  rooted-tree-trimmed-pooled.qza \
  --i-table col-filtered-table-expt1-noic.qza \
  --p-sampling-depth 18000 \
  --m-metadata-file rainin_metadata_file_pooled_2019.tsv \
  --o-rarefied-table rarefied-table-pooled-noic-1-col.qza \
 --o-faith-pd-vector faith-pd-pooled-noic-1-col.qza \
 --o-observed-otus-vector observed-otus-pooled-noic-1-col.qza \
 --o-shannon-vector shannon-vector-pooled-noic-uc.qza \
 --o-evenness-vector evenness-vector-pooled-noic-1-col.qza \
 --o-unweighted-unifrac-distance-matrix unweighted-unifrac-distance-matrix-pooled-noic-1-col.qza \
 --o-weighted-unifrac-distance-matrix weighted-unifrac-distance-matrix-pooled-noic-1-col.qza \
 --o-jaccard-distance-matrix jaccard-distance-matrix-pooled-noic-1-col.qza \
 --o-bray-curtis-distance-matrix bray-curtis-distance-matrix-pooled-noic-1-col.qza \
 --o-unweighted-unifrac-pcoa-results unweighted-unifrac-pca-results-pooled-noic-1-col.qza \
 --o-weighted-unifrac-pcoa-results weighted-unifrac-pcoa-results-pooled-noic-1-col.qza \
 --o-jaccard-pcoa-results jaccard-pcoa-results-trimmed-pooled-noic-1-col.qza \
 --o-bray-curtis-pcoa-results trimmed-bray-curtis-pcoa-results-pooled-noic-1-col.qza \
 --o-unweighted-unifrac-emperor unweighted-unifrac-emperor-pooled-noic-1-col.qzv \
 --o-weighted-unifrac-emperor weighted-unifrac-emperor-pooled-noic-1-col.qzv \
 --o-jaccard-emperor jaccard-emperor-pooled-noic-1-col.qzv \
 --o-bray-curtis-emperor bray-curtis-emperor-pooled-noic-1-col.qzv
 
 #performing beta-diversity analyses - colonization period - experiment 1 
 
```

    [32mSaved FeatureTable[Frequency] to: rarefied-table-pooled-noic-1-col.qza[0m
    [32mSaved SampleData[AlphaDiversity] % Properties('phylogenetic') to: faith-pd-pooled-noic-1-col.qza[0m
    [32mSaved SampleData[AlphaDiversity] to: observed-otus-pooled-noic-1-col.qza[0m
    [32mSaved SampleData[AlphaDiversity] to: shannon-vector-pooled-noic-uc.qza[0m
    [32mSaved SampleData[AlphaDiversity] to: evenness-vector-pooled-noic-1-col.qza[0m
    [32mSaved DistanceMatrix % Properties('phylogenetic') to: unweighted-unifrac-distance-matrix-pooled-noic-1-col.qza[0m
    [32mSaved DistanceMatrix % Properties('phylogenetic') to: weighted-unifrac-distance-matrix-pooled-noic-1-col.qza[0m
    [32mSaved DistanceMatrix to: jaccard-distance-matrix-pooled-noic-1-col.qza[0m
    [32mSaved DistanceMatrix to: bray-curtis-distance-matrix-pooled-noic-1-col.qza[0m
    [32mSaved PCoAResults to: unweighted-unifrac-pca-results-pooled-noic-1-col.qza[0m
    [32mSaved PCoAResults to: weighted-unifrac-pcoa-results-pooled-noic-1-col.qza[0m
    [32mSaved PCoAResults to: jaccard-pcoa-results-trimmed-pooled-noic-1-col.qza[0m
    [32mSaved PCoAResults to: trimmed-bray-curtis-pcoa-results-pooled-noic-1-col.qza[0m
    [32mSaved Visualization to: unweighted-unifrac-emperor-pooled-noic-1-col.qzv[0m
    [32mSaved Visualization to: weighted-unifrac-emperor-pooled-noic-1-col.qzv[0m
    [32mSaved Visualization to: jaccard-emperor-pooled-noic-1-col.qzv[0m
    [32mSaved Visualization to: bray-curtis-emperor-pooled-noic-1-col.qzv[0m
    (qiime2-2020.2) (qiime2-2020.2) (qiime2-2020.2) 




```bash
qiime diversity beta-group-significance \
--i-distance-matrix weighted-unifrac-distance-matrix-pooled-noic-1-col.qza \
--m-metadata-file rainin_metadata_file_pooled_2019.tsv \
--m-metadata-column Treatment \
--o-visualization wunifrac-col-beta-sig-pooled-expt.qzv \
--p-pairwise
#beta-significance - experiment 1 colonization period
```

    [32mSaved Visualization to: wunifrac-col-beta-sig-pooled-expt.qzv[0m
    (qiime2-2020.2) 




```bash
qiime feature-table filter-samples \
--i-table  merged-expt2-noic.qza  \
--m-metadata-file rainin_metadata_file_pooled_2019.tsv \
--p-where "Period= 'Colonization'" \
--o-filtered-table col-filtered-table-expt2-noic.qza
 #performing beta-diversity analyses here- colonization period - experiment 1 

```

    [32mSaved FeatureTable[Frequency] to: col-filtered-table-expt2-noic.qza[0m



```bash
qiime diversity core-metrics-phylogenetic \
  --i-phylogeny  rooted-tree-trimmed-pooled.qza \
  --i-table col-filtered-table-expt2-noic.qza \
  --p-sampling-depth 27000 \
  --m-metadata-file rainin_metadata_file_pooled_2019.tsv \
  --o-rarefied-table rarefied-table-pooled-noic-2-col.qza \
 --o-faith-pd-vector faith-pd-pooled-noic-2-col.qza \
 --o-observed-otus-vector observed-otus-pooled-noic-2-col.qza \
 --o-shannon-vector shannon-vector-pooled-noic-2-uc.qza \
 --o-evenness-vector evenness-vector-pooled-noic-2-col.qza \
 --o-unweighted-unifrac-distance-matrix unweighted-unifrac-distance-matrix-pooled-noic-2-col.qza \
 --o-weighted-unifrac-distance-matrix weighted-unifrac-distance-matrix-pooled-noic-2-col.qza \
 --o-jaccard-distance-matrix jaccard-distance-matrix-pooled-noic-2-col.qza \
 --o-bray-curtis-distance-matrix bray-curtis-distance-matrix-pooled-noic-2-col.qza \
 --o-unweighted-unifrac-pcoa-results unweighted-unifrac-pca-results-pooled-noic-2-col.qza \
 --o-weighted-unifrac-pcoa-results weighted-unifrac-pcoa-results-pooled-noic-2-col.qza \
 --o-jaccard-pcoa-results jaccard-pcoa-results-trimmed-pooled-noic-2-col.qza \
 --o-bray-curtis-pcoa-results trimmed-bray-curtis-pcoa-results-pooled-noic-2-col.qza \
 --o-unweighted-unifrac-emperor unweighted-unifrac-emperor-pooled-noic-2-col.qzv \
 --o-weighted-unifrac-emperor weighted-unifrac-emperor-pooled-noic-2-col.qzv \
 --o-jaccard-emperor jaccard-emperor-pooled-noic-2-col.qzv \
 --o-bray-curtis-emperor bray-curtis-emperor-pooled-noic-2-col.qzv
  #performing beta-diversity analyses - colonization period - experiment 2 

```


```bash
qiime diversity beta-group-significance \
--i-distance-matrix weighted-unifrac-distance-matrix-pooled-noic-2-col.qza \
--m-metadata-file rainin_metadata_file_pooled_2019.tsv \
--m-metadata-column Treatment \
--o-visualization wunifrac-col-beta-sig-pooled-expt2.qzv \
--p-pairwise
#beta-significance - experiment 2 colonization period
```


```bash
qiime taxa collapse \
--i-table col-filtered-table-expt1-noic.qza \
--i-taxonomy taxonomy-trimmed.qza \
--p-level 7 \
--o-collapsed-table collapsed-species-expt1-col.qza
#Collapsing all species in experiment 1 colonization period 
```

    [32mSaved FeatureTable[Frequency] to: collapsed-species-expt1-col.qza[0m



```bash
qiime taxa collapse \
--i-table col-filtered-table-expt2-noic.qza \
--i-taxonomy taxonomy-trimmed.qza \
--p-level 7 \
--o-collapsed-table collapsed-species-expt2-col.qza
#Collapsing all species in experiment 2 colonization period 
```

    [32mSaved FeatureTable[Frequency] to: collapsed-species-expt2-col.qza[0m



```bash
qiime composition add-pseudocount \
--i-table  collapsed-species-expt1-col.qza \
--o-composition-table col-pseudo-expt1-species.qza
#Adding pseudocount for experiment #1 - colonization
```

    [32mSaved FeatureTable[Composition] to: col-pseudo-expt1-species.qza[0m



```bash
qiime composition add-pseudocount \
--i-table  collapsed-species-expt2-col.qza \
--o-composition-table col-pseudo-expt2-species.qza
#Adding pseudocount for experiment #2 - colonization 
```

    [32mSaved FeatureTable[Composition] to: col-pseudo-expt2-species.qza[0m



```bash
qiime composition ancom \
--i-table col-pseudo-expt1-species.qza \
--m-metadata-file  rainin_metadata_file_pooled_2019.tsv \
--m-metadata-column Treatment \
--o-visualization ancom-col-expt1-noic.qzv
#Running ANCOM for experiment #1 
```

    [32mSaved Visualization to: ancom-col-expt1-noic.qzv[0m



```bash
qiime composition ancom \
--i-table col-pseudo-expt2-species.qza \
--m-metadata-file  rainin_metadata_file_pooled_2019.tsv \
--m-metadata-column Treatment \
--o-visualization ancom-col-expt2-noic.qzv
#Running ANCOM for experiment #2 
```

    [32mSaved Visualization to: ancom-col-expt2-noic.qzv[0m



```bash
qiime feature-table filter-samples \
--i-table merged-expt1-no-ic.qza  \
--m-metadata-file rainin_metadata_file_pooled_2019.tsv \
--p-where "Period= 'gavage'" \
--o-filtered-table gav-filtered-table-expt1-noic.qza
#filtering for samples in VLP gavage period - experiment 1 
```


```bash
qiime diversity core-metrics-phylogenetic \
  --i-phylogeny  rooted-tree-trimmed-pooled.qza \
  --i-table gav-filtered-table-expt1-noic.qza \
  --p-sampling-depth 18000 \
  --m-metadata-file rainin_metadata_file_pooled_2019.tsv \
  --o-rarefied-table rarefied-table-pooled-noic-1-gav.qza \
 --o-faith-pd-vector faith-pd-pooled-noic-1-gav.qza \
 --o-observed-otus-vector observed-otus-pooled-noic-1-gav.qza \
 --o-shannon-vector shannon-vector-pooled-noic-gav.qza \
 --o-evenness-vector evenness-vector-pooled-noic-1-gav.qza \
 --o-unweighted-unifrac-distance-matrix unweighted-unifrac-distance-matrix-pooled-noic-1-gav.qza \
 --o-weighted-unifrac-distance-matrix weighted-unifrac-distance-matrix-pooled-noic-1-gav.qza \
 --o-jaccard-distance-matrix jaccard-distance-matrix-pooled-noic-1-gav.qza \
 --o-bray-curtis-distance-matrix bray-curtis-distance-matrix-pooled-noic-1-gav.qza \
 --o-unweighted-unifrac-pcoa-results unweighted-unifrac-pca-results-pooled-noic-1-gav.qza \
 --o-weighted-unifrac-pcoa-results weighted-unifrac-pcoa-results-pooled-noic-1-gav.qza \
 --o-jaccard-pcoa-results jaccard-pcoa-results-trimmed-pooled-noic-1-gav.qza \
 --o-bray-curtis-pcoa-results trimmed-bray-curtis-pcoa-results-pooled-noic-1-gav.qza \
 --o-unweighted-unifrac-emperor unweighted-unifrac-emperor-pooled-noic-1-gav.qzv \
 --o-weighted-unifrac-emperor weighted-unifrac-emperor-pooled-noic-1-gav.qzv \
 --o-jaccard-emperor jaccard-emperor-pooled-noic-1-gav.qzv \
 --o-bray-curtis-emperor bray-curtis-emperor-pooled-noic-1-gav.qzv
  #performing beta-diversity analyses here- gavage period - experiment 1 

```

    [32mSaved FeatureTable[Frequency] to: rarefied-table-pooled-noic-1-gav.qza[0m
    [32mSaved SampleData[AlphaDiversity] % Properties('phylogenetic') to: faith-pd-pooled-noic-1-gav.qza[0m
    [32mSaved SampleData[AlphaDiversity] to: observed-otus-pooled-noic-1-gav.qza[0m
    [32mSaved SampleData[AlphaDiversity] to: shannon-vector-pooled-noic-gav.qza[0m
    [32mSaved SampleData[AlphaDiversity] to: evenness-vector-pooled-noic-1-gav.qza[0m
    [32mSaved DistanceMatrix % Properties('phylogenetic') to: unweighted-unifrac-distance-matrix-pooled-noic-1-gav.qza[0m
    [32mSaved DistanceMatrix % Properties('phylogenetic') to: weighted-unifrac-distance-matrix-pooled-noic-1-gav.qza[0m
    [32mSaved DistanceMatrix to: jaccard-distance-matrix-pooled-noic-1-gav.qza[0m
    [32mSaved DistanceMatrix to: bray-curtis-distance-matrix-pooled-noic-1-gav.qza[0m
    [32mSaved PCoAResults to: unweighted-unifrac-pca-results-pooled-noic-1-gav.qza[0m
    [32mSaved PCoAResults to: weighted-unifrac-pcoa-results-pooled-noic-1-gav.qza[0m
    [32mSaved PCoAResults to: jaccard-pcoa-results-trimmed-pooled-noic-1-gav.qza[0m
    [32mSaved PCoAResults to: trimmed-bray-curtis-pcoa-results-pooled-noic-1-gav.qza[0m
    [32mSaved Visualization to: unweighted-unifrac-emperor-pooled-noic-1-gav.qzv[0m
    [32mSaved Visualization to: weighted-unifrac-emperor-pooled-noic-1-gav.qzv[0m
    [32mSaved Visualization to: jaccard-emperor-pooled-noic-1-gav.qzv[0m
    [32mSaved Visualization to: bray-curtis-emperor-pooled-noic-1-gav.qzv[0m
    (qiime2-2020.2) 




```bash
qiime diversity beta-group-significance \
--i-distance-matrix weighted-unifrac-distance-matrix-pooled-noic-1-gav.qza \
--m-metadata-file rainin_metadata_file_pooled_2019.tsv \
--m-metadata-column Treatment \
--o-visualization wunifrac-gav-beta-sig-pooled-expt.qzv \
--p-pairwise
#beta-significance - experiment 1 gavage period
```

    [32mSaved Visualization to: wunifrac-gav-beta-sig-pooled-expt.qzv[0m
    (qiime2-2020.2) 




```bash
qiime feature-table filter-samples \
--i-table merged-expt2-noic.qza  \
--m-metadata-file rainin_metadata_file_pooled_2019.tsv \
--p-where "Period= 'gavage'" \
--o-filtered-table gav-filtered-table-expt2-noic.qza
#filtering for samples in VLP gavage period - experiment 2 
```


```bash
qiime diversity core-metrics-phylogenetic \
  --i-phylogeny  rooted-tree-trimmed-pooled.qza \
  --i-table gav-filtered-table-expt1-noic.qza \
  --p-sampling-depth 27000 \
  --m-metadata-file rainin_metadata_file_pooled_2019.tsv \
  --o-rarefied-table rarefied-table-pooled-noic-2-gav.qza \
 --o-faith-pd-vector faith-pd-pooled-noic-2-gav.qza \
 --o-observed-otus-vector observed-otus-pooled-noic-2-gav.qza \
 --o-shannon-vector shannon-vector-pooled-noic-2-gav.qza \
 --o-evenness-vector evenness-vector-pooled-noic-2-gav.qza \
 --o-unweighted-unifrac-distance-matrix unweighted-unifrac-distance-matrix-pooled-noic-2-gav.qza \
 --o-weighted-unifrac-distance-matrix weighted-unifrac-distance-matrix-pooled-noic-2-gav.qza \
 --o-jaccard-distance-matrix jaccard-distance-matrix-pooled-noic-2-gav.qza \
 --o-bray-curtis-distance-matrix bray-curtis-distance-matrix-pooled-noic-2-gav.qza \
 --o-unweighted-unifrac-pcoa-results unweighted-unifrac-pca-results-pooled-noic-2-gav.qza \
 --o-weighted-unifrac-pcoa-results weighted-unifrac-pcoa-results-pooled-noic-2-gav.qza \
 --o-jaccard-pcoa-results jaccard-pcoa-results-trimmed-pooled-noic-2-gav.qza \
 --o-bray-curtis-pcoa-results trimmed-bray-curtis-pcoa-results-pooled-noic-2-gav.qza \
 --o-unweighted-unifrac-emperor unweighted-unifrac-emperor-pooled-noic-2-gav.qzv \
 --o-weighted-unifrac-emperor weighted-unifrac-emperor-pooled-noic-2-gav.qzv \
 --o-jaccard-emperor jaccard-emperor-pooled-noic-2-gav.qzv \
 --o-bray-curtis-emperor bray-curtis-emperor-pooled-noic-2-gav.qzv
  #performing beta-diversity analyses here- gavage period - experiment 2
```


```bash
qiime diversity beta-group-significance \
--i-distance-matrix weighted-unifrac-distance-matrix-pooled-noic-2-gav.qza \
--m-metadata-file rainin_metadata_file_pooled_2019.tsv \
--m-metadata-column Treatment \
--o-visualization wunifrac-gav-beta-sig-pooled-expt2.qzv \
--p-pairwise
#beta-significance - experiment 2 gavage period
```


```bash
qiime taxa collapse \
--i-table gav-filtered-table-expt1-noic.qza \
--i-taxonomy taxonomy-trimmed.qza \
--p-level 7 \
--o-collapsed-table collapsed-species-gav-expt1.qza
#collapsing  to species level in experiment #1 
```

    [32mSaved FeatureTable[Frequency] to: collapsed-species-gav-expt1.qza[0m



```bash
qiime taxa collapse \
--i-table gav-filtered-table-expt2-noic.qza \
--i-taxonomy taxonomy-trimmed.qza \
--p-level 7 \
--o-collapsed-table collapsed-species-gav-expt2.qza
#collapsing  to species level in experiment #2
```

    [32mSaved FeatureTable[Frequency] to: collapsed-species-gav-expt2.qza[0m



```bash
qiime composition add-pseudocount \
--i-table  collapsed-species-gav-expt1.qza \
--o-composition-table gav-expt1-pseudo-count-species.qza 

```

    [32mSaved FeatureTable[Composition] to: gav-expt1-pseudo-count-species.qza[0m



```bash
qiime composition add-pseudocount \
--i-table  collapsed-species-gav-expt2.qza \
--o-composition-table gav-expt2-pseudo-count-species.qza 
```

    [32mSaved FeatureTable[Composition] to: gav-expt2-pseudo-count-species.qza[0m



```bash
qiime composition ancom \
--i-table gav-expt1-pseudo-count-species.qza  \
--m-metadata-file  rainin_metadata_file_pooled_2019.tsv \
--m-metadata-column Treatment \
--o-visualization ancom-gav-expt1-species.qzv
#differentially abundant species  = gavage period, experiment #1 
```

    [32mSaved Visualization to: ancom-gav-expt1-species.qzv[0m



```bash
qiime composition ancom \
--i-table gav-expt2-pseudo-count-species.qza  \
--m-metadata-file  rainin_metadata_file_pooled_2019.tsv \
--m-metadata-column Treatment \
--o-visualization ancom-gav-expt2-species.qzv
#differentially abundant species  = gavage period, experiment #2
```

    [32mSaved Visualization to: ancom-gav-expt2-species.qzv[0m



```bash
qiime feature-table filter-samples \
--i-table merged-expt1-no-ic.qza  \
--m-metadata-file rainin_metadata_file_pooled_2019.tsv \
--p-where "Period= 'DSS+washout'" \
--o-filtered-table dss-filtered-table-expt1-noic.qza
#filtering for samples in DSS/washout period- experiment 1
```


```bash
qiime diversity core-metrics-phylogenetic \
  --i-phylogeny  rooted-tree-trimmed-pooled.qza \
  --i-table dss-filtered-table-expt1-noic.qza \
  --p-sampling-depth 18000 \
  --m-metadata-file rainin_metadata_file_pooled_2019.tsv \
  --o-rarefied-table rarefied-table-pooled-noic-1-dss.qza \
 --o-faith-pd-vector faith-pd-pooled-noic-1-dss.qza \
 --o-observed-otus-vector observed-otus-pooled-noic-1-dss.qza \
 --o-shannon-vector shannon-vector-pooled-noic-dss.qza \
 --o-evenness-vector evenness-vector-pooled-noic-1-dss.qza \
 --o-unweighted-unifrac-distance-matrix unweighted-unifrac-distance-matrix-pooled-noic-1-dss.qza \
 --o-weighted-unifrac-distance-matrix weighted-unifrac-distance-matrix-pooled-noic-1-dss.qza \
 --o-jaccard-distance-matrix jaccard-distance-matrix-pooled-noic-1-dss.qza \
 --o-bray-curtis-distance-matrix bray-curtis-distance-matrix-pooled-noic-1-dss.qza \
 --o-unweighted-unifrac-pcoa-results unweighted-unifrac-pca-results-pooled-noic-1-dss.qza \
 --o-weighted-unifrac-pcoa-results weighted-unifrac-pcoa-results-pooled-noic-1-dss.qza \
 --o-jaccard-pcoa-results jaccard-pcoa-results-trimmed-pooled-noic-1-dss.qza \
 --o-bray-curtis-pcoa-results trimmed-bray-curtis-pcoa-results-pooled-noic-1-dss.qza \
 --o-unweighted-unifrac-emperor unweighted-unifrac-emperor-pooled-noic-1-dss.qzv \
 --o-weighted-unifrac-emperor weighted-unifrac-emperor-pooled-noic-1-dss.qzv \
 --o-jaccard-emperor jaccard-emperor-pooled-noic-1-dss.qzv \
 --o-bray-curtis-emperor bray-curtis-emperor-pooled-noic-1-dss.qzv
```

    [32mSaved FeatureTable[Frequency] to: rarefied-table-pooled-noic-1-dss.qza[0m
    [32mSaved SampleData[AlphaDiversity] % Properties('phylogenetic') to: faith-pd-pooled-noic-1-dss.qza[0m
    [32mSaved SampleData[AlphaDiversity] to: observed-otus-pooled-noic-1-dss.qza[0m
    [32mSaved SampleData[AlphaDiversity] to: shannon-vector-pooled-noic-dss.qza[0m
    [32mSaved SampleData[AlphaDiversity] to: evenness-vector-pooled-noic-1-dss.qza[0m
    [32mSaved DistanceMatrix % Properties('phylogenetic') to: unweighted-unifrac-distance-matrix-pooled-noic-1-dss.qza[0m
    [32mSaved DistanceMatrix % Properties('phylogenetic') to: weighted-unifrac-distance-matrix-pooled-noic-1-dss.qza[0m
    [32mSaved DistanceMatrix to: jaccard-distance-matrix-pooled-noic-1-dss.qza[0m
    [32mSaved DistanceMatrix to: bray-curtis-distance-matrix-pooled-noic-1-dss.qza[0m
    [32mSaved PCoAResults to: unweighted-unifrac-pca-results-pooled-noic-1-dss.qza[0m
    [32mSaved PCoAResults to: weighted-unifrac-pcoa-results-pooled-noic-1-dss.qza[0m
    [32mSaved PCoAResults to: jaccard-pcoa-results-trimmed-pooled-noic-1-dss.qza[0m
    [32mSaved PCoAResults to: trimmed-bray-curtis-pcoa-results-pooled-noic-1-dss.qza[0m
    [32mSaved Visualization to: unweighted-unifrac-emperor-pooled-noic-1-dss.qzv[0m
    [32mSaved Visualization to: weighted-unifrac-emperor-pooled-noic-1-dss.qzv[0m
    [32mSaved Visualization to: jaccard-emperor-pooled-noic-1-dss.qzv[0m
    [32mSaved Visualization to: bray-curtis-emperor-pooled-noic-1-dss.qzv[0m
    (qiime2-2020.2) 




```bash
qiime diversity beta-group-significance \
--i-distance-matrix weighted-unifrac-distance-matrix-pooled-noic-1-dss.qza \
--m-metadata-file rainin_metadata_file_pooled_2019.tsv \
--m-metadata-column Treatment \
--o-visualization wunifrac-dss-beta-sig-pooled-expt.qzv \
--p-pairwise
#beta-significance - DSS/washout period - experiment 1
```

    [32mSaved Visualization to: wunifrac-dss-beta-sig-pooled-expt.qzv[0m
    (qiime2-2020.2) 




```bash
qiime feature-table filter-samples \
--i-table merged-expt2-no-ic.qza  \
--m-metadata-file rainin_metadata_file_pooled_2019.tsv \
--p-where "Period= 'DSS+washout'" \
--o-filtered-table dss-filtered-table-expt2-noic.qza
#filtering for samples in DSS/washout period- experiment 2
```


```bash
qiime diversity core-metrics-phylogenetic \
  --i-phylogeny  rooted-tree-trimmed-pooled.qza \
  --i-table dss-filtered-table-expt2-noic.qza \
  --p-sampling-depth 27000 \
  --m-metadata-file rainin_metadata_file_pooled_2019.tsv \
  --o-rarefied-table rarefied-table-pooled-noic-2-dss.qza \
 --o-faith-pd-vector faith-pd-pooled-noic-2-dss.qza \
 --o-observed-otus-vector observed-otus-pooled-noic-2-dss.qza \
 --o-shannon-vector shannon-vector-pooled-noic-2-dss.qza \
 --o-evenness-vector evenness-vector-pooled-noic-2-dss.qza \
 --o-unweighted-unifrac-distance-matrix unweighted-unifrac-distance-matrix-pooled-noic-2-dss.qza \
 --o-weighted-unifrac-distance-matrix weighted-unifrac-distance-matrix-pooled-noic-2-dss.qza \
 --o-jaccard-distance-matrix jaccard-distance-matrix-pooled-noic-2-dss.qza \
 --o-bray-curtis-distance-matrix bray-curtis-distance-matrix-pooled-noic-2-dss.qza \
 --o-unweighted-unifrac-pcoa-results unweighted-unifrac-pca-results-pooled-noic-2-dss.qza \
 --o-weighted-unifrac-pcoa-results weighted-unifrac-pcoa-results-pooled-noic-2-dss.qza \
 --o-jaccard-pcoa-results jaccard-pcoa-results-trimmed-pooled-noic-2-dss.qza \
 --o-bray-curtis-pcoa-results trimmed-bray-curtis-pcoa-results-pooled-noic-2-dss.qza \
 --o-unweighted-unifrac-emperor unweighted-unifrac-emperor-pooled-noic-2-dss.qzv \
 --o-weighted-unifrac-emperor weighted-unifrac-emperor-pooled-noic-2-dss.qzv \
 --o-jaccard-emperor jaccard-emperor-pooled-noic-2-dss.qzv \
 --o-bray-curtis-emperor bray-curtis-emperor-pooled-noic-2-dss.qzv
```


```bash
qiime taxa collapse \
--i-table dss-filtered-table-pooled-noic.qza \
--i-taxonomy taxonomy-trimmed.qza \
--p-level 7 \
--o-collapsed-table collapsed-species-pooled-dss.qza
#collapsed species DSS
```

    [32mSaved FeatureTable[Frequency] to: collapsed-species-pooled-dss.qza[0m



```bash
qiime taxa collapse \
--i-table dss-filtered-table-expt1-noic.qza \
--i-taxonomy taxonomy-trimmed.qza \
--p-level 7 \
--o-collapsed-table collapsed-species-expt1-dss.qza

#collapsing to species level experiment 1 in DSS/ washout period
```

    [32mSaved FeatureTable[Frequency] to: collapsed-species-expt1-dss.qza[0m



```bash
qiime taxa collapse \
--i-table dss-filtered-table-expt2-noic.qza \
--i-taxonomy taxonomy-trimmed.qza \
--p-level 7 \
--o-collapsed-table collapsed-species-expt2-dss.qza
#collapsing to species level experiment 1 in DSS/ washout period
```

    [32mSaved FeatureTable[Frequency] to: collapsed-species-expt2-dss.qza[0m



```bash
qiime composition add-pseudocount \
--i-table collapsed-species-expt1-dss.qza \
--o-composition-table comptable-expt1-pseudo-dss.qza 

```

    [32mSaved FeatureTable[Composition] to: comptable-expt1-pseudo-dss.qza[0m



```bash
qiime composition add-pseudocount \
--i-table dss-filtered-table-expt1-noic.qza \
--o-composition-table comptable-expt1-pseudo-dss-asvs.qza 

```

    [32mSaved FeatureTable[Composition] to: comptable-expt1-pseudo-dss-asvs.qza[0m
    (qiime2-2020.2) 




```bash
qiime composition add-pseudocount \
--i-table collapsed-species-expt2-dss.qza \
--o-composition-table comptable-expt2-pseudo-dss.qza 
```

    [32mSaved FeatureTable[Composition] to: comptable-expt2-pseudo-dss.qza[0m



```bash
qiime composition ancom \
--i-table comptable-expt1-pseudo-dss.qza   \
--m-metadata-file  rainin_metadata_file_pooled_2019.tsv \
--m-metadata-column Treatment \
--o-visualization ancom-expt1-dss.qzv
#differentially abundant species experiment 1 DSS/washout
```

    [32mSaved Visualization to: ancom-expt1-dss.qzv[0m
    (qiime2-2020.2) (qiime2-2020.2) 




```bash
qiime composition ancom \
--i-table comptable-expt2-pseudo-dss.qza \
--m-metadata-file  rainin_metadata_file_pooled_2019.tsv \
--m-metadata-column Treatment \
--o-visualization ancom-expt2-dss.qzv
#differentially abundant species experiment 2 DSS/washout
```

    [32mSaved Visualization to: ancom-expt2-dss.qzv[0m



```bash
qiime longitudinal feature-volatility \
--i-table collapsed-species-expt1.qza \
--m-metadata-file rainin_metadata_file_pooled_2019.tsv \
--p-state-column Date \
--p-individual-id-column Cage \
--p-estimator KNeighborsRegressor \
--p-n-jobs 4 \
--p-n-estimators 400 \
--o-filtered-table expt1species-feature-vol-filtered-table-trimmed-w.qza \
--o-feature-importance expt1species-feature-vol-importance-trimmed-w.qza \
--o-volatility-plot expt1species-feature-vol-plot-trimmed-w.qzv \
--o-accuracy-results expt1species-accuracy-results-feature-vol-trimmed-w.qzv \
--o-sample-estimator expt1species-sample-estimator-feature-vol-trimmed-w.qza

#Feature volatility- species level for expt 1
```

    [32mSaved FeatureTable[RelativeFrequency] to: expt1species-feature-vol-filtered-table-trimmed-w.qza[0m
    [32mSaved FeatureData[Importance] to: expt1species-feature-vol-importance-trimmed-w.qza[0m
    [32mSaved Visualization to: expt1species-feature-vol-plot-trimmed-w.qzv[0m
    [32mSaved Visualization to: expt1species-accuracy-results-feature-vol-trimmed-w.qzv[0m
    [32mSaved SampleEstimator[Regressor] to: expt1species-sample-estimator-feature-vol-trimmed-w.qza[0m



```bash
qiime longitudinal feature-volatility \
--i-table collapsed-species-expt2.qza \
--m-metadata-file rainin_metadata_file_pooled_2019.tsv \
--p-state-column Date \
--p-individual-id-column Cage \
--p-estimator KNeighborsRegressor \
--p-n-jobs 4 \
--p-n-estimators 400 \
--o-filtered-table expt2species-feature-vol-filtered-table-trimmed-w.qza \
--o-feature-importance expt2species-feature-vol-importance-trimmed-w.qza \
--o-volatility-plot expt2species-feature-vol-plot-trimmed-w.qzv \
--o-accuracy-results expt2species-accuracy-results-feature-vol-trimmed-w.qzv \
--o-sample-estimator expt2species-sample-estimator-feature-vol-trimmed-w.qza

#Feature volatility- species level for expt 2
```

    [32mSaved FeatureTable[RelativeFrequency] to: expt2species-feature-vol-filtered-table-trimmed-w.qza[0m
    [32mSaved FeatureData[Importance] to: expt2species-feature-vol-importance-trimmed-w.qza[0m
    [32mSaved Visualization to: expt2species-feature-vol-plot-trimmed-w.qzv[0m
    [32mSaved Visualization to: expt2species-accuracy-results-feature-vol-trimmed-w.qzv[0m
    [32mSaved SampleEstimator[Regressor] to: expt2species-sample-estimator-feature-vol-trimmed-w.qza[0m

