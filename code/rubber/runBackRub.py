#!/usr/bin/python
## This Script will run backrub on the scaffold structure provided
## args can be set. A lot of this script has been adapted from masili's
## Scripts to make reading a little bit easier.
##
## Mehdi Nellen, Tuebingen 2015


import sys, os
import argparse
from PDBAbsResMapping import PDBresMap 
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
    parser = argparse.ArgumentParser(description='Run Rosetta BackRub on some scaffold. It will only backrub residues in the position file.',   fromfile_prefix_chars='@',
        formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    
    parser.add_argument('scaffold_file', help='Location of the PDB file of the '
                        'scaffold', type=expand_path)
    parser.add_argument('position_file', 
                        help='contains information about the pocket residue positions '
                        'and which amino acids are allowed at them.',
                        type=file)
    parser.add_argument('output_dir', help='output directory', type=expand_path)
    parser.add_argument('nStruct', help='number of structures to produce', type=int)
    parser.add_argument('nMonte', help='number of montecarlo trials to run', type=int)
    parser.add_argument('--backrub-pyfile', help='The python file '
                        'which runs BackRub (default: assumed to be in $PATH)',
                        type=expand_path)

    args = parser.parse_args(command_line)
    assert os.path.exists(args.scaffold_file), 'file %s for argument scaffold_file does not exist'%args.scaffold_file
    if args.backrub_pyfile:
        assert os.path.exists(args.backrub_pyfile), 'directory %s for option --backrub-pyfile does not exist'%args.backrub_pyfile
    else:
        args.backrub_pyfile = ''
    if not os.path.exists(args.output_dir):
        os.mkdir(args.output_dir)

    return args


def createBackrubCommand(backrub_pyfile, nStruct, nMonte, positions, scaffold):
    ''' Make the command which has to be run by the system '''
    # make a mapping of pdb resn to absolute numbers 
    pmap = PDBresMap(scaffold)
    indices=[]
    for datai in positions:
        # index of the binding pocket in rosettas absolute numbering
        i = pmap.PDBtoABS(datai['chain'], int(datai['index']))
        indices.append(i-2)
        indices.append(i-1)
        indices.append(i)
        indices.append(i+1)
        indices.append(i+2)
    # only keep unique ones
    indices = list(set(indices))
    indices = ' '.join(str(x) for x in indices)

    # make the command
    print backrub_pyfile, scaffold, nStruct, nMonte, indices 
    cmd_string = "{0} -s {1} -nstruct {2} -backrub:ntrials {3} -pivot_residues {4}".format(backrub_pyfile, scaffold, nStruct, nMonte, indices)
    return cmd_string

def main( command_line):
    '''Run everything'''
    args = getArguments( command_line)
    # all files from rosetta will be written to output_dir
    os.chdir(args.output_dir)
     
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
    
    # create the command string and run it 
    cmd = createBackrubCommand(args.backrub_pyfile, args.nStruct, args.nMonte, positions, args.scaffold_file)
    os.system(cmd)

if __name__ == "__main__":
    main( sys.argv[1:])

