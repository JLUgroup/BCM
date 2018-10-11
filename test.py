from pbcm import Bcm
#from read import Read
import fbcm
import os

from matplotlib import pyplot as plt
from scipy.cluster.hierarchy import dendrogram, linkage
import numpy as np

#import numpy as np


def distribute_calc(folderpath):
	a = open('distances.txt','w')
	b = open('distfrom0.txt','w')
	bcmstore = {}
	diststore = []
	dist0store = []
	k = 0
	for root, dirs, files in os.walk(folderpath):
		for file in files:
			if file != 'POSCAR':
				continue
			k = k + 1
			filepath = os.path.join(root, file)
			print filepath
			
			bcmatrix = Bcm(filepath, 'poscar').bcm_calc()
			bcmstore[k] = bcmatrix
			bcmstore[-k] = filepath

	print 'total num = ',k

	for i in range(1,k):
		for j in range(i+1,k+1):
			dist = Bcm().distxy(bcmstore[i],bcmstore[j])
			diststore.append(dist)

	for i in range(1,k+1):
		dist0 = Bcm().dit0(bcmstore[i])
		dist0store.append(dist0)

	diststore.sort()
	dist0store.sort()

	for num in diststore:
		num = str(num)
		a.write(num)
		a.write('\n')

	for num in dist0store:
		num = str(num)
		b.write(num)
		b.write('\n')


	a.close()
	b.close()



def __cluster(folderpath):
	bcmstore = {}
	k = 0
	for root, dirs, files in os.walk(folderpath):
		for file in files:
			if file != 'POSCAR':
				continue
			k = k + 1
			filepath = os.path.join(root, file)
			print filepath

			bcmatrix = Bcm(filepath, 'poscar').bcm_calc()
			bcmstore[k] = bcmatrix
			bcmstore[-k] = filepath

	print 'total num = ', k





if __name__ == '__main__':
	path = '/home/jhxie/1e/'
	distribute_calc(path)










#tau=[[0.1,0.2,0.3],[0.5,0.6,0.7],[0.8,0.9,0.0]]
#lattice=[[1,2,3],[4,5,6],[7,8,9]]
#nele=1
#natom=3
#ele=[3]
#a=fbcm.bcm(1,3,tau,lattice,ele)

#print a


#a = Read('str/0.vasp','poscar').getStructure()
#a = Bcm('str/0.vasp','poscar').bcm_calc()
#b = Bcm('str/1.vasp','poscar').bcm_calc()

#d = Bcm().distxy(a,b)
#a = np.array(a)
#print a
#print d
#print a.ndim
#print a.shape
#print a.size
#,a.shape,a.size,a.dtype,a.itemsize,a.data


'''
for i in a:
	for j in i:
		for k in j:
			print k
'''
