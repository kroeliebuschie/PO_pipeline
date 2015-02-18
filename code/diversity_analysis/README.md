Analysis of the RMS diversity
=============================

## Description and Contents
These scripts calculate RMS values of pdb's in an input folder compared to a reference. In the case of Backrub this would be
comparing the backrub structures or backrubbed + minimized structures to the original structure and see how much they have changed.

* `make_Rtable.R`
* `make_profit_script.sh`
* `make_iprofit_script.sh`
* `make_iprofit_fit_script.sh`

## Usage 
What the script actualy do is generate ProFit scripts and you run these with ProFit.
The result can be analysed by the R script at the end. Run it like this:
```bash
make_profit_script.sh reference.pdb mobiles_folder/ "xtra profit cmd" > output_profit_script.txt
profit -f output_profit_script.txt > output_profit_results.txt
```
The "xtra profit cmd" can be for example "ALIGN WHOLE" which would first align the structures before fitting them (necasairy when using strctures with different sequences).

The iprofit scripts needs an additional positions.txt as argument. These scripts calculate the RMS over only the binding pocket residues. The difference between 
`make_iprofit_fit_script.sh` and `make_iprofit_script.sh` is that latter one does not superimpose the structures prior to RMS calculation.

```bash
make_iprofit_script.sh reference.pdb mobiles_folder/ positions.txt > iprofit_script.txt
```

before preceding to the next step it might be good to perform this to the profit output:
```bash
grep -A1 "##" results.txt > results_grepped.txt
```

The R script takes the profit output textfiles as arguments and returns a pdf file with the plot.
```bash
Rscript make_Rtable.R output_profit_results1.txt output_profit_results2.txt output_profit_results3.txt
```
