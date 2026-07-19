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

### 2026-06-20

- Computed disease-level feature centroids by averaging patient feature vectors, enabling exploratory analysis of symptom prevalence and providing a basis for similarity-based disease retrieval

### 2026-06-27

- Developed an additional encoding technique for illnesses that theoretically increases the information retention in the system.
- The new encoding represents the explicit precense of a symptom with 1, the explicit absence of a system with -1, and the lack of information of a system with a 0. Oposite to the previously stated encoding of 1 and 0, this new system differentiates between having no information regarding a symtpom and its explicit absence.

### 2026-06-28

- Started designing alternative architectures that mix encoding, weightings, and retrieval techniques to find the best combination
- The architectures are a mix of either binary encoding or signed encoding, exploration of weights for literature definition of disease vectors, and cosine similarity or weighted cosine similarity or euclidean distance for retireval techniques

### 2026-06-29

- Ran first test for Binary encoding, cosine similarity, and no weighting with only one record for Anemia. The results was that the model effectively predicted that the diagnosis was Anemia based on the provided symptoms

### 2026-07-16

- Started the development and experimenting with an LLM integration for easy natural language interaction with clients

### 2026-06-17

- Started complimentary information retrieval system (retireving symptoms that contribute the most to the diagnosis as well as symptoms with no information whose precense or abcense are likely to affect the diagnosis)
- The objective of such system is providing the fastest way to find the most confident diagnosis we can get from the engine while also providing the justification for such diagnosis

### 2026-06-19

- Finished first part of recommendation system. The system consists of comparing the differences on each index and retireving the symptoms for which the difference between the top 1 diagnosis and the patient record is the smallest possible
