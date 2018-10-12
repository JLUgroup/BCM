from pbcm import Bcm
#from read import Read
import fbcm
import os

from matplotlib import pyplot as plt
from scipy.cluster.hierarchy import dendrogram, linkage
import numpy as np
from clusterplot import __genget


def distribute_calc(folderpath):
	a = open('distances.txt','w')
	b = open('distfrom0.txt','w')
	bcmstore = []
	diststore = []
	dist0store = []
	
	resultmat = Bcm().calc_folder(folderpath)
	for result in resultmat:
		bcmstore.append(result[0])	
	k = len(bcmstore)
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
	bcmstore = []
	resultmat = Bcm().calc_folder(folderpath)
	ns = open('name.txt','w')
	for result in resultmat:
		aresult = np.array(result[0])
		aresult = aresult.flatten()
		bcmstore.append(aresult)
		ns.write(result[1])
		ns.write('\n')
	ns.close()
	Z = linkage(bcmstore,'ward')
	np.save('cluster_result.npy', Z)
	np.savetxt('cluster.txt', Z)

	return Z


def __reprecluster():
	namef = open('finallist.txt','r')
	for name in namef:
		print str(name)





		






if __name__ == '__main__':
	path = '/home/jhxie/1e/'
#	distribute_calc(path)
	#a = __cluster(path)
	__reprecluster()
	#b = open('cluster_result.txt','w')
	#for i in a:
#		b.write(i)
#		b.write('\n')
#	b.close()












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
