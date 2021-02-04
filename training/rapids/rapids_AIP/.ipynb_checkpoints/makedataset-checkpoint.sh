#!/bin/bash

## Generate the 100GB Higgs dataset for use in the tutorial

# Run in terminal from ~/ : bash rapids_AIP/makedataset.sh

# Set chunks to 10 for 10 1 GB files (which will be uploaded 10 times for a total of 100GB). If you want more data to play around with, just increase NUM_CHUNKS)
NUM_CHUNKS=${1:-10}
GCS_BUCKET="rwtmp_demo_ml/nvidiadask/atest" #Choose a name for your bucket, or if you already have a bucket/folder in mind, put that here

# Create a GCS bucket in which to store the data
#gsutil mb -l us-central1 gs://$GCS_BUCKET

# Download the Higgs dataset 
wget https://archive.ics.uci.edu/ml/machine-learning-databases/00280/HIGGS.csv.gz

gzip -dk HIGGS.csv.gz

mkdir -p chunked_higgs

num_lines=`cat HIGGS.csv| wc -l`

len=1470000

step_size=$(( (num_lines-len) / num_chunks))

 
## Replicate the original dataset into 10 1GB chunks
for i in `seq 1 ${NUM_CHUNKS}`;

do

    start_idx=$(( (i-1) * step_size + 1))

    end_idx=$(( (i-1) * step_size + len))

    echo $i ...

    echo $start_idx 

    echo $end_idx

    sed -n "${start_idx},${end_idx}p" HIGGS.csv > chunked_higgs/$i.csv

done

# Upload data to GCS, in ten different folders so that we can easily test different subsets of the data (each folder holds 10GB of data)
gsutil -m cp ~/chunked_higgs/* gs://$GCS_BUCKET/abcdefghij
gsutil -m cp ~/chunked_higgs/* gs://$GCS_BUCKET/abcdefghi
gsutil -m cp ~/chunked_higgs/* gs://$GCS_BUCKET/abcdefgh
gsutil -m cp ~/chunked_higgs/* gs://$GCS_BUCKET/abcdefg
gsutil -m cp ~/chunked_higgs/* gs://$GCS_BUCKET/abcdef
gsutil -m cp ~/chunked_higgs/* gs://$GCS_BUCKET/abcde
gsutil -m cp ~/chunked_higgs/* gs://$GCS_BUCKET/abcd
gsutil -m cp ~/chunked_higgs/* gs://$GCS_BUCKET/abc
gsutil -m cp ~/chunked_higgs/* gs://$GCS_BUCKET/ab
gsutil -m cp ~/chunked_higgs/* gs://$GCS_BUCKET/a

# Remove the downloaded and replicated files to free up space
cd ~/
rm HIGGS.csv.gz HIGGS.csv
rm -r chunked_higgs

