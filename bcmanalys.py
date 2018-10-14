# coding: utf-8
import os

import numpy as np
from matplotlib import pyplot as plt
from scipy.cluster.hierarchy import dendrogram, linkage

import fbcm
from clusteranalys import __genget
from pbcm import Bcm


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
	for i in range(k-1):
		for j in range(i+1,k):
			dist = Bcm().distxy(bcmstore[i],bcmstore[j])
			diststore.append(dist)

	for i in range(1,k+1):
		dist0 = Bcm().dist0(bcmstore[i])
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


def distribute_analys(partnum=None):
    a = open('distances.txt', 'r')
    b = open('calout.txt', 'w')

    numcount = []
    for i in range(partnum):
        numcount.append(0)

    for data in a:
        pass
    length = float(data) / partnum
    a.seek(0, 0)
    for data in a:
        data = float(data)
        for i in range(partnum):
            if i*length < data < (i+1)*length:
                numcount[i] += 1
                break
    for i in range(partnum):
        b.write(str(numcount[i])+' '+str((i+1)*length))
        b.write('\n')

    b.close()
    a.close()

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
	namef = open('clusterlist.txt','r')
	clusters = []
	cluster = []
	repreclusters = []
	clusbcmstore = []
	ns = open('represent_cluster.txt','w')
	for name in namef:
		if name != '\n':
			cluster.append(name)
		else:
			clusters.append(cluster)
			cluster = []
	
	for cluste in clusters:
		for struct in cluste:
			struct = struct.strip('\n')
			bcm = Bcm().bcm_calc(struct)
			clusbcmstore.append(bcm)

		sumdists = []
		k = len(cluste)
		for i in range(k):
			sumdist = 0 
			for j in range(k):
				dist = Bcm().distxy(clusbcmstore[i], clusbcmstore[j])
				sumdist += dist
			sumdists.append(sumdist)

		mindist = min(sumdists)
		minindex = sumdists.index(mindist)
		reprecluster = cluste[minindex]
		repreclusters.append(reprecluster)
		ns.write(reprecluster)
		print sumdists
		print minindex
		print reprecluster
		
	ns.close()
	print len(repreclusters)

	






		






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
