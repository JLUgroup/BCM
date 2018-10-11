# coding: utf-8

from read import Read
import fbcm
import numpy as np

class Bcm(object):
    '''

    '''

    def __init__(self,filepath=None,type=None):
        self.filepath = filepath
        self.type = type


    def bcm_calc(self):

        structure = Read(self.filepath,self.type).getStructure()
        nele = len(structure['elements'])
        natom = sum(structure['numbers'])
        lattice = structure['lattice']
        positions = structure['positions']
        numbers = structure['numbers']
        bcmatrix = fbcm.bcm(nele,natom,positions,lattice,numbers)
        while 0 in bcmatrix
        bcmatrix = np.array(bcmatrix)

        return bcmatrix


    def distxy(self,x,y):

        if x.shape != y.shape:
            print 'can not compare two matrix'
            exit()
    	d = np.linalg.norm(x-y)
    	return d

    def dit0(self,x):

        a = np.linalg.norm(x)

        return a


   
