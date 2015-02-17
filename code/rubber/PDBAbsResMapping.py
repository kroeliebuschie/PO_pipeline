#!/usr/bin/python 
## a module with a class mapping the 

class PDBresMap:
    ''' 
    This class is a mapping of the pdb
    file residues and the absolute 
    numbering used by some programs like 
    Rosetta BackRub.
    '''
    map_dict = {}
    def __init__(self, PDB, includeHET=True):
        self.name = PDB
        
        # The PDB file needs to be read
        f_handle = open(PDB, 'rU')
        
        # initiate the variables for chain,
        # residue number and absolute number
        chain = resn = ''
        absn  = 0

        # Get all the data from the ATOM 
        # records and write them to c_dict
        # afterwards write c_dict to map_dict
        for line in f_handle.readlines():
            if line.startswith("ATOM") or line.startswith("HETATM"):
                # Skip lines with HETATM if necasairy
                if includeHET == False:
                    if line.startswith("HETATM"):
                        continue

                # get the cains
                if chain != line[21]:
                    if 'c_dict' in locals():
                        PDBresMap.map_dict[chain] = c_dict
                    c_dict = {}
                    chain= line[21]

                # get the residue number
                if resn != int(line[22:26]):
                    resn = int(line[22:26])
                    absn +=1
                    c_dict[resn] = absn

        # at the end of the for loop we still  
        # have to add the last dictionairy
        if 'c_dict' in locals():
            PDBresMap.map_dict[chain] = c_dict
    
    def PDBtoABS(self, chain, resn):
        ''' 
        return the absolute residue number
        given a residue number and chain
        '''
        if not PDBresMap.map_dict:
            raise IndexError('There are no residues or chains. This PDBresMap is empty, check the PDB file.')
        try:
            return PDBresMap.map_dict[chain][int(resn)]
        except KeyError:
            print 'Residue number or chain has not been found'
            raise

    def ABStoPDB(self, absn):
        '''
        return a tuple with chain and resn
        given an absolute residue number
        '''
        if not PDBresMap.map_dict:
            raise IndexError('There are no residues or chains. This PDBresMap is empty, check the PDB file.')
        try:
            for chain, c_dict in PDBresMap.map_dict.iteritems():
                for resn, absnd in c_dict.iteritems():
                    if absnd == absn:
                        pdb_cr = (chain, resn)
            return pdb_cr
        except NameError:
            print "The residue number could not be found"
            raise


