Rosetta Backrub module
======================

## Content and Description
This module contains script that will make backrub movements to the scaffold structure (for PocketOptimizer). 
This will increase the diversity of the starting structures. It consists of a backrub step, an optional minimization step,
a fitting step, a clustering step and a scoring step.

* runBackRub.py
* PDBAbsResMapping.py
* runProFit.py
* clusterRMSD.py

## Dependencies
* Python
* Rosetta BackRub
* ProFit

## Usage
All python scripts have a help option (`python script.py -h`).

You start of with a `scaffold.pdb` and `positions.txt` and the following script generates backrub movements.
It uses the postions in `positions.txt` to generate pivot points in BackRub (all residues +-2 of the residues in `positions.txt` are
made pivot points).

```bash
# Run backrub with 10000 montecarlo simulations generating 200 models
python runBackRub.py scaffold.pdb positions.txt BR_output_dir/ --backrub-pyfile /path/to/backrub.linuxgccrelease 200 10000
```

The output from the previous step can be used to generate pairwise RMS calculations using profit.
This step will perform an all-to-all comparison. The script looks up the residues in `positions.txt` and only calculates the 
RMS over these residues. The boolian argument tells the script whether it should first fit the rest of the sctructure before calculating
the RMS.
```bash
# Use 'False' to NOT fit before calculate RMS values
python runProFit.py positions.txt BR_output_dir/ False scaffold_ --profit-bin /path/to/profit
```

The previous script outputs a json file which can be used to cluster the matrix resulting from the all-to-all comparison

```bash
# make 4 clusters using the single method and use the json file
python clusterRMSD.py distance_matrix.json 4 single
```

## issues, developments and extra info

rosetta_sub.sh  script example to submit rosetta to a cluster

