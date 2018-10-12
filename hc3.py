#!/usr/bin/env python
#-*- coding:utf-8 -*-


#hc3

from matplotlib import pyplot as plt
from scipy.cluster.hierarchy import dendrogram, linkage
import numpy as np
from scipy.cluster.hierarchy import cophenet
from scipy.spatial.distance import pdist
from scipy.cluster.hierarchy import _order_cluster_tree
import os
import os.path
import shutil
import fnmatch

#Matplotlib inline
np.set_printoptions(precision=5, suppress=True)

rootdir = os.getcwd()
path = rootdir+'/'+'BDOFILE'

data=[]
dataset=[]
cifname=[]

for root,dirnames,filenames in os.walk(path):
    for filename in fnmatch.filter(filenames,'*.bdo'):
        with open(path+'/'+filename,'r') as f:
            for i in f.readlines():
                data.append(float(i.strip()))
        dataset.append(data)
        cifname.append(filename.replace('.bdo',''))
        data=[]



X=np.array(dataset)
Xlen=len(dataset)

print "The dataset X:"
print X
print "       "
print "The sample number of the dataset is:",Xlen
print "       "
print "The dataset X's shape:",X.shape
print "                        "

#Generate the linkage matrix
Z = linkage(X, method='average', metric='euclidean',optimal_ordering='True')
#c, coph_dists = cophenet(Z, pdist(X))
#print "The clusteing score(the full is 1.0):",c
#print "                        "
print "The linkage chain Z(type 'numpy.ndarray'):\n",Z
print "                        "

#Resolve linkage chain Z
ZZ=Z.tolist()
ob=[]
C=[]
for i in range(len(ZZ)):
    for j in range(2):
        ob.append(int(ZZ[i][j]))
    C.append(ob)
    ob=[]


def resolve(index):
    if index>=Xlen:
        index-=Xlen
    return index

D=C
inx=0

for i in range(len(C)):
    for j in range(2):
        if C[i][j]>=Xlen:
            inx=resolve(C[i][j])
            D[i][j]=C[inx]

print "The simplified linkage chain C:"
for c in range(len(C)):
    print C[c]

print '-------------------------------------------------------------'

#Set the threshold value "THV" and get the corresponding index clusters F
'''
algorithm1:

zlen=len(Z)
THV=1
if Z[zlen-1][2]==0.0 or zlen==1:
    THV=1
    max_d=Z[zlen-1][2]
else:
    if Z[zlen-1][2]-Z[zlen-2][2]>=Z[zlen-2][2]:
        max_d = 0.6*Z[zlen-1][2]
        for td in range(zlen):
            if (Z[td][2]<=max_d) and (Z[td+1][2]>=max_d):
                THV=zlen-td
                break
    else:
        max_d = 0.8*Z[zlen-2][2]
        for tdd in range(zlen):
            if (Z[tdd][2]<=max_d) and (Z[tdd+1][2]>=max_d):
                THV=zlen-tdd
                break
E=range(Xlen)
F=[]
'''

#algorithm2:
rate=[]
zlen=len(Z)
THV=1
BTM=0
CUT=2
if zlen==1:
    THV=1
    max_d=0.99*Z[zlen-1][2]
else:
    if Z[zlen-1][2]<=0.55:
        THV=1
        max_d=0.99*Z[zlen-1][2]
    else:
        if CUT>zlen:
            BTM=0
        else:
            BTM=int(zlen/CUT)-1

        for ri,rj in zip(range(BTM,zlen-1),range(BTM+1,zlen)):
            tmpr=(Z[rj][2]-Z[ri][2])/(Z[ri][2]+1)
            rate.append(tmpr)
        ratemax=np.max(rate)
        print rate
        print ratemax
        for ti,tj in zip(range(BTM,zlen-1),range(BTM+1,zlen)):
            tmp=(Z[tj][2]-Z[ti][2])/(Z[ti][2]+1)
            if abs(ratemax-tmp)<=0.00001:
                THV=zlen-ti
                max_d=0.99*Z[tj][2]
                break
print "  "
print "maxd=",max_d
print "The threshold value is:",THV

def flatten(ll):
    if isinstance(ll, list):
        for i in ll:
            for element in flatten(i):
                yield element
    else:
        yield ll

#cluster
E=range(Xlen)
F=[]
print "The index clusters F:"
for d in range(Xlen-THV):
    E.append(D[d])
    for e in range(2):
        E.remove(D[d][e])

for e in range(len(E)):
    F.append(list(flatten(E[e])))
    print F[e]

print '-----------------------------------------------------------'

#Get the cif file name clusters G
G=[]
tep=[]
DD=cifname
for f in range(len(F)):
    for g in range(len(F[f])):
        tep.append(DD[F[f][g]])
    G.append(tep)
    tep=[]
    print G[f]

#Make figure directory
if not os.path.isdir(rootdir+'/'+'figure'):
    os.mkdir(rootdir+'/'+'figure')

#Calculate full dendrogram
plt.figure(figsize=(19.2, 10.8))
plt.title('Hierarchical Clustering Dendrogram')
plt.xlabel('sample index')
plt.ylabel('distance')
R=dendrogram(
    Z,
    leaf_rotation=90.,  # rotates the x axis labels
    leaf_font_size=8.,  # font size for the x axis labels
          )
plt.savefig(rootdir+'/'+'figure'+'/'+'p'+str(THV)+'.png',dpi=100)
plt.close()
#plt.show()

#Dendrogram Truncation
plt.title('Hierarchical Clustering Dendrogram (truncated)')
plt.xlabel('sample index')
plt.ylabel('distance')
'''
dendrogram(
    Z,
    truncate_mode='lastp',  # show only the last p merged clusters
    p=20,  # show only the last p merged clusters
    #show_leaf_counts=False,  # otherwise numbers in brackets are counts
    leaf_rotation=90.,
    leaf_font_size=12.,
    show_contracted=True,  # to get a distribution impression in truncated branches
    orientation='top',
          )
#plt.show()
'''

def fancy_dendrogram(*args, **kwargs):
    max_d = kwargs.pop('max_d', None)
    if max_d and 'color_threshold' not in kwargs:
        kwargs['color_threshold'] = max_d
    annotate_above = kwargs.pop('annotate_above', 0)

    ddata = dendrogram(*args, **kwargs)

    if not kwargs.get('no_plot', False):
        plt.title('Hierarchical Clustering Dendrogram (truncated)')
        plt.xlabel('sample index or (cluster size)')
        plt.ylabel('distance')
        for i, d, c in zip(ddata['icoord'], ddata['dcoord'], ddata['color_list']):
            x = 0.5 * sum(i[1:3])
            y = d[1]
            if y > annotate_above:
                plt.plot(x, y, 'o', c=c)
                plt.annotate("%.3g" % y, (x, y), xytext=(0, -5),
                             textcoords='offset points',
                             va='top', ha='center')
        if max_d:
            plt.axhline(y=max_d, c='k')
    return ddata
'''
fancy_dendrogram(
    Z,
    truncate_mode='lastp',
    p=20,
    leaf_rotation=90.,
    leaf_font_size=12.,
    show_contracted=True,
    annotate_above=0.0001,  # useful in small plots so annotations don't overlap
                )   
#plt.show()
'''

#Set cut-off line
plt.figure(figsize=(19.2, 10.8))
fancy_dendrogram(
    Z,
    truncate_mode='lastp',
    p=40,
    leaf_rotation=90.,
    leaf_font_size=12.,
    show_contracted=True,
    annotate_above=0.0001,
    max_d=max_d, # plot a horizontal cut-off line
    orientation='top',
                )
plt.savefig(rootdir+'/'+'figure'+'/'+'t'+str(THV)+'.png')
plt.close()
#plt.show()

'''
#Elbow method
last = Z[-10:, 2]
last_rev = last[::-1]
idxs = np.arange(1, len(last) + 1)
plt.plot(idxs, last_rev)

acceleration = np.diff(last, 2)  # 2nd derivative of the distances
acceleration_rev = acceleration[::-1]
plt.plot(idxs[:-2] + 1, acceleration_rev)
plt.show()
k = acceleration_rev.argmax() + 2  # if idx 0 is the max of this we want 2 clusters
print "clusters:", k
'''

#CIF file cluster
if not os.path.isdir(rootdir+'/'+'cluster'+'/'+str(THV)):
    os.makedirs(rootdir+'/'+'cluster'+'/'+str(THV))
for i in range(len(G)):
    os.mkdir(rootdir+'/'+'cluster'+'/'+str(THV)+'/'+str(i+1))
    for j in range(len(G[i])):
        shutil.copy(rootdir+'/'+'source'+'/'+G[i][j]+'.cif',rootdir+'/'+'cluster'+'/'+str(THV)+'/'+str(i+1))

#Cluster log
with open(rootdir+'/'+'hc3log.doc','w') as fl:
    fl.write("The threshold value is %d\n" %THV)
    fl.write("    \n")
    fl.write("The max distance is %f\n" %Z[zlen-1][2])
    fl.write("    \n")
    fl.write("The cutoff distance is %f\n" %max_d)
    fl.write("    \n")
    fl.write("The clustered cif files:\n")
    for cn in G:
        fl.write(str(cn)+"\n")
    fl.write("    \n")
    fl.write("The number of each cluster:\n")
    for cn in G:
        fl.write(str(len(cn))+"\n")
    fl.write("    \n")
    fl.write("The number of all cif files:\n")
    fl.write(str(len(X)))
