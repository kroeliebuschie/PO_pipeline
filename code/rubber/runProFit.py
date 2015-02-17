#!/usr/bin/python
## This script runs Profit to do RMSD calculations on
## PDB structures in a folder. It can restrict the 
## calculation to only the interface residues. 
##
## Mehdi Nellen, Tuebingen 2015


import sys, os
import re
import json
import argparse
import tempfile
import subprocess
import glob
import itertools
# uncomment if can
#from py.Common.MiscTools import expand_path

## remove the following command if the py.common can be sourced
def expand_path(path_str):
    '''@param path_str: a string that contains a file/directory path
    @return: absolute path with environment & user variables expanded'''
    return os.path.abspath(os.path.expanduser(os.path.expandvars(path_str)))


def getArguments(command_line):
    '''create the command line argument parser 
    @return: a ArgumentParser.parse_args() Namespace
    with the parameters. (adapted from masili)'''
    parser = argparse.ArgumentParser(description='Run ProFit to do RMSD calculations. This script takes a position file as input'
            ' and calculates RMS values over these residues in the PDB structures given. ',   fromfile_prefix_chars='@',
        formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    
    parser.add_argument('position_file', 
                        help='contains information about the pocket residue positions '
                        'and which amino acids are allowed at them.',
                        type=file)
    parser.add_argument('pdb_dir', help='directory containing PDB files (Rosetta Backrub output)', type=expand_path)
    parser.add_argument('fit', help='boolian whether it should first superimpose '
                        'models before calculating RMS (True or False)', type=str)
    parser.add_argument('file_stem', help='The unique identifier for a group of file'
                        ' (e.g. "foo_*_bar_" is the stem for "foo_1_bar_1.pdb" "foo_2_bar_4.pdb" ...)', type=str)
    parser.add_argument('--profit-bin', help='The profit binary file '
                        'which runs profit ',
                        type=expand_path)

    args = parser.parse_args(command_line)
    if args.profit_bin:
        assert os.path.exists(args.profit_bin), 'directory %s for option --profit-bin does not exist'%args.profit_bin
    else:
        args.profit_bin = ''
    if not os.path.exists(args.pdb_dir):
        os.mkdir(args.pdb_dir)
    if args.fit == 'True':
        args.fit = True
    elif args.fit == 'False':
        args.fit = False
    else:
        raise Exception('fit should either be True or False')

    return args




def iRMS(positions, ref_pdb, mob_pdb, fit):
    ''' Make the command which has to be run by profit returns a string with all commands'''
    # join chain id and residue number like "A.33"
    indices = [ '.'.join([datei['chain'], datei['index']]) for datei in positions ]
    # join chain.resn with eachother so profit can read it like "A.33-A.33"  
    indices = [ '-'.join(str(j) for j in i) for i in zip(indices,indices) ] 
    
    # make the commands for profit
    txt  = 'reference ' + ref_pdb + '\n'
    txt += 'mobile ' + mob_pdb + '\n'
    # make zone, superimpose Calphas, don't use DELZONE for superimposing
    txt += 'ZONE * \nATOMS CA\n'
    for ind in indices:
        txt += 'DELZONE ' + ind + '\n'
    # go
    if fit:
        txt += 'fit\n'
    else:
        txt += 'nofit\n'
    # calc rms over these
    for ind in indices:
        txt += 'RZONE ' + ind + '\n'
    txt += 'RATOMS CA\n'
    txt += '#pickme\n'
    txt += 'RMS \n'
    txt += '#done\nquit\n\n'
    
    return txt

def ProFit(ref_pdb, mob_pdb, fit, positions):
    '''Function which runs profit with the pdbs given and checks weather 
       they should be fit prior to iRMS calculations'''
    # first make the txt file then create it as a tmp file and then run profit
    txt = iRMS(positions, ref_pdb, mob_pdb, fit)
    with tempfile.NamedTemporaryFile() as temp:
        temp.write(txt)
        temp.flush()
        # create the comand for the shell proces
        cmd = profit_bin + ' -f ' + temp.name 
        # run it
        proc = subprocess.Popen(cmd, shell=True, stdout = subprocess.PIPE, stdin = subprocess.PIPE, stderr=subprocess.PIPE)
        # get the output from the procces and return only the rms value
        it_std = iter(proc.stdout.readline,"")
         
        for line in it_std:
            if re.search("#pickme", line):
                rms = next(it_std)
                rms = re.sub('RMS: ', '', rms)
                rms = float(rms)
                break
    return rms

def main( command_line):
    '''Run everything'''
    args = getArguments( command_line)
    print args
    # all files from rosetta will be written to pdb_dir
    global profit_bin
    profit_bin = args.profit_bin
    print os.path.join(args.pdb_dir,  ''.join((args.file_stem, '*.pdb')))
    pdb_files = glob.glob(args.pdb_dir + os.sep + args.file_stem + '*.pdb')
    
    # get the chain index and mutations from the position file
    # addapted from masili
    positions = [] 
    params = {} 
    for l in args.position_file: 
        l = l.strip() 
        if l == '[position]': 
            if params == {}: 
                continue 
            k = params.keys() 
            k.sort() 
            assert k == ['chain', 'index', 'mutations'], 'the position file ' + args.position_file.name + ' has invalid syntax.' 
            params['mutations'] = params['mutations'].split() 
            if 'HIS' in params['mutations']: 
                params['mutations'].remove('HIS') 
                params['mutations'] += ['HSE', 'HSP', 'HSD'] 
                         
            positions.append(params) 
            params = {} 
        elif not (l == '' or l.isspace()): 
            sp = l.split('=') 
            params[sp[0].strip()] = sp[1].strip() 
    k = params.keys() 
    k.sort() 
    assert k == ['chain', 'index', 'mutations'], 'the position file ' + args.position_file.name + ' has invalid syntax.' 
    params['mutations'] = params['mutations'].split() 
    positions.append(params) 
    
    # create lists
    df = {'pdb_list_0': pdb_files, 'pdb_list_1': [], 'pdb_list_2': [], 'rmsd' : []}

    # make combinations of 2
    it_pdb = itertools.combinations(pdb_files, 2)
    for comb in it_pdb:
        df['pdb_list_1'].append(comb[0])
        df['pdb_list_2'].append(comb[1])
        df['rmsd'].append(ProFit(comb[0], comb[1], args.fit, positions))
    # write json file
    with open('distance_matrix.json', 'w') as json_f: 
        json_f.write(json.dumps(df))
        json_f.close()

if __name__ == "__main__":
    main( sys.argv[1:])

