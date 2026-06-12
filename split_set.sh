#!/bin/bash

cat $1 | sed -r 's/AGE,DIFFERENTIAL_DIAGNOSIS,SEX,PATHOLOGY,EVIDENCES,INITIAL_EVIDENCE/AGE|DIFFERENTIAL_DIAGNOSIS|SEX|PATHOLOGY|EVIDENCES|INITIAL_EVIDENCE/g' sed -r 's/([0-9]+),/\1|/g' | sed -r 's/\]\",/\]\"|/g' | sed -r 's/(F|M),/\1|/g' | sed -r 's/,\"\[/|\"\[/g' > $(echo $1"_pipe_split")

# This long command will take in the name of a file, anc exchange all the commas ',' for pipes '|' under certain conditions to make
# processing easier later on
