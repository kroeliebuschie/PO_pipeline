#!/bin/bash
#$ -l h_vmem=2G
#$ -cwd 
#$ -r n
#$ -l h_rt=00:03:00

## This submits rosetta jobs to the cluster
##
## Author Mehdi Nellen, Tuebingen 2015

 
# run rostta with ' -nstruct' amount of structures
/ebio/abt1/share/software/rosetta/2014_wk_05/main/source/bin/./backrub.linuxgccrelease -s scaffold.pdb -nstruct 10 -backrub:ntrials 10000 


