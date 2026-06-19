### Project Goal
Develop a disease diagnosis retrieval engine capable of identifying clinically similar patient cases using binary symptom feature vectors and similarity search.

### Dataset
Name: DDXPlus
Origin: https://figshare.com/articles/dataset/DDXPlus_Dataset_English_/22687585
Number of diseases: 49
Patient records used for training: 1025602
Data Limitations: Ethnicity, place of residency, and social class are also valuable data for diagnosing a person with a disease

### Similarity Method
- Cosine similarity
- Euclidean distance
Explanation on results once that part is reached...

### Optimizations
    Optimization 1
        Bottleneck:
        - Runtime was too long to process each row, taking up to 2 hours processing 30k rows out of the 1M rows in the dataset
        Solution:
        - Vectorized string operations, deferred aggregations and row concatenation operations outside the processing loop
        Impact:
        - The runtime dropped drastically from 2 hours for 30k rows to 10 minutes for the whole dataset
    
    Optimization 2:
        Bottleneck:
        - Merging the resulting 1M rows into one dataset in one go caused the RAM to reach its maximum hardware capabilities
        Solution:
        - Implement chunking while sacrificing speed
        - Rows are merged every 10k rows processed within the loop to avoid merging 1M rows in one go
        Impact:
        - The runtime for processing the whole dataset increased to 4 hours, nevertheless, the pipeline no longer requires to exceed the provided hardware resources
    
    Optimization 3:
        Bottleneck:
        - Leaving the machine running for 4 hours straight in an unrestricted environment is not realistic. Power outages, connection issues, and/or software crashes will cause the computation to halt and loose all the preprocessed data.
        Solution:
        - Every time a 10k row chunk is preprocessed, it will be stored in a parquet to the disk before starting the next chunk, creating a backup and setting a starting point once computation is restarted.
        Impact:
        - Progress loss on unexpected computing issues is minimal, in the worst case scenario, only one chunk of 10k rows will be lost instead of the hundreds of thousands that were processed already.
