### 2026-06-11
- Created Disease Diagnosis Engine repo in Github
- Created split_set.sh, a bash script that will take the original format of the DDXPlus dataset
  and place pipe characters where the columns of the dataset should be split

### 2026-06-14
- Created dataset headers that will hold all the vectors utilized with their respective features

### 2026-06-16
- Preprocessed the data provided by the DDXPlus dataset for feature extraction and vector generation

    ### Problem
    - Feature generation created a runtime bottleneck that caused the feature extraction pipeline to take several hours to preprocess a small fraction of the data

    ### Investigation
    - String regex operations, array parsing, object allocation, and NaN value replacement were
    happening within the main row-processing loop

    ### Solution
    - Vectorized string operations and string-to-array parsings with Pandas' built in vector operations
    - Deferred aggregations and operations non-essential for processing

    ### Reasoning
    - Pandas' built in vector operations are better optimized than applying the same function to each row individually. Plus, such operations are not required to be executed within the feature extracting loop.
    - Allocation heavy functions and operations that should be applied to all the dataset regardless can be deferred as they are not essential for the feature extracting loop

    ### Impact
    - Main feature extracting loop improved from processing 30k rows in 2 hours to processing 1M rows in 10 minutes

    ### Learning
    - Repeated computations and feature extraction operations inside the loop generate a an inmense runtime overhead

### 2026-06-18
- Continued feature extraction by merging all resulting rows into one dataset

    ### Problem
    - Despite drastically reducing the time in feature extraction a couple of days ago, merging all the resulting rows (more than 1M) in one shot will cause the cluster to run out of RAM

    ### Investigation
    - An array of more than 1M entries is being merged into one single dataset in one go, generating so many internal copies of the data that the provided RAM is not enough

    ### Solution
    - Sacrifice some of the speed of the pipeline after its previous changes for merging rows every 10k ready-to-merge rows and storing the resulting dataset as a parquet for later merging.

    ### Reasoning
    - After experimenting with the RAM limitations of my environment, I observed that chunks of 10k rows provided a stable use of RAM without exceeding its limits. Higher amounts such as 15k or 20k would exceed the RAM capabilities while smaller chunks caused computation to take longer.

    ### Impact
    - The pipeline takes approxinately 4 hours in processing all the 1M entries of the original data but doesn't run out of RAM while processing the entries.
    - Storage as parquets ensures that in case of error, the rows already processed and merged are still stored and the lost progress in case of error is minimal

    ### Learning
    - Runtime is not the only valuable metric while developing a pipeline. Creating a pipeline that can run on a reasonable time while respecting hardware constrains is more important than a hypotetical pipeline that can run at lightspeed with unlimited hardware.

### 2026-06-19

### Major Milestone: Succesfully extracted features of the 1M rows in the DDXPlus dataset into Binary Vectors representation
### Challenges:
- Runtime bottlenecks due to row operations
- Memory bottlenecks due to large aggregations
- Risk of possible progress loss due to interrupting computations

### Solutions:
- Vectorizing and deferring operations
- Aggregating chunks of data instead of every single row in one go
- Storing every processed chunk

### Outcome (up to now):
- Dataset in binary vector format ready for calculations
- Recovery backup in case of interrupted computing
- Stable memory utilization
