#!/bin/bash 
## run The backrub scripts automaticaly
##
## Author: Mehdi Nellen, Tuebingen 2015

## ARGS:
##  $1  PDB identifier
## SETTINGS:
NSTR=20     # number of structures
MNTC=1000   # number of montecarlo simulations
NCLS=2      # number of clusters

# Run backRub, creates new folder
python /ebio/abt1/share/PO_pipeline/code/rubber/runBackRub.py \
    scaffold_${1}/${1}_scaffold.pdb \
    positions.txt \
    BackRub_${1}/  \
    $NSTR \
    $MNTC \
    --backrub-pyfile /ebio/abt1/share/software/rosetta/2014_wk_05/main/source/bin/backrub.linuxgccrelease

#python /ebio/abt1/share/PO_pipeline/code/rubber/runProFit.py \
#    positions.txt \
#    BackRub_${1}/ \
#    False \
#    *scaffold \
#    --profit-bin /ebio/abt1/mnellen/software/ProFitV3.1/src/profit
#
#
#mv distance_matrix.json BackRub_${1}/
#
#python /ebio/abt1/share/PO_pipeline/code/rubber/clusterRMSD.py \
#    BackRub_${1}/distance_matrix.json \
#    $NCLS \
#    single

### analysis 
#mkdir diversity_analysis_${1}
#
#/ebio/abt1/share/PO_pipeline/code/diversity_analysis/make_profit_script.sh \
#        scaffold_${1}/${1}_scaffold.pdb \
#        BackRub_${1}/ \
#        "#" > diversity_analysis_${1}/profit_script.txt 
#
#
#profit -f diversity_analysis_${1}/output_profit_script.txt > diversity_analysis_${1}/whole_structure_fit.txt
#
## This will calculate RMS of the binding pocketwithout fitting
#make_iprofit_script.sh \
#    scaffold_${1}/${1}_scaffold.pdb \
#    BackRub_${1}/ \
#    positions.txt > diversity_analysis_${1}/iprofit_script.txt
#
#profit -f diversity_analysis_${1}/iprofit_script.txt > diversity_analysis_${1}/${1}_binding_pocket_nofit.txt
#
## This will calculate RMS of the binding pocketwithout fitting
#make_iprofit_fit_script.sh \ 
#    scaffold_${1}/${1}_scaffold.pdb \
#    BackRub_${1}/ \
#    positions.txt > diversity_analysis_${1}/iprofit_fit_script.txt
#
#profit -f diversity_analysis_${1}/iprofit_fit_script.txt > diversity_analysis_${1}/${1}_binding_pocket_fit.txt
#
# grep step
#
#Rscript make_Rtable.R \
#    diversity_analysis_${1}/whole_structure_fit.txt \
#    diversity_analysis_${1}/${1}_binding_pocket_nofit.txt \
#    diversity_analysis_${1}/${1}_binding_pocket_fit.txt
#

