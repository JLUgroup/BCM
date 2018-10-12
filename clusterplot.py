from matplotlib import pyplot as plt
from scipy.cluster.hierarchy import dendrogram, linkage
import numpy as np
from compiler.ast import flatten

def plotcluster():
    Z = np.load('cluster_result.npy')
    plt.figure(figsize=(25, 10))
    plt.title('Hierarchical Clustering Dendrogram')
    plt.xlabel('sample index')
    plt.ylabel('distance')
    dendrogram(
        Z,
        leaf_rotation=90.,  # rotates the x axis labels
        leaf_font_size=8.,  # font size for the x axis labels
    )
    plt.show()

def plotZ():
   Z = np.load('cluster_result.npy')
   y = Z[:,2]
   x = range(len(y))
   plt.scatter(x,y,alpha=0.6)
   plt.show()


def __genget(generation):
    Z = np.load('cluster_result.npy')
    ns = open('name.txt', 'r')
    #lengt = len(Z)
    namelist = []
    nameresult = []
    for line in ns:
        namelist.append(line)

    for i in range(generation):
        index1 = int(Z[i, 0])
        index2 = int(Z[i, 1])
        temp = []
        temp.append(namelist[index1])
        temp.append(namelist[index2])
        namelist[index1] = 'be merged'
        namelist[index2] = 'be merged'
        namelist.append(temp)
    finallist = open('finallist.txt', 'w')
    k = 0
    for a in namelist:
        if a != 'be merged':
            k = k+1
            a = flatten(a)
            nameresult.append(a)
        
            for b in a:
                finallist.write(b)
            finallist.write('\n')
    #finallist.write('result cluster num = ')
    #finallist.write(str(k))
    finallist.close()
    print k,len(nameresult)

    return nameresult
		#print namelist[index1], namelist[index2]


    


if __name__ == '__main__':
    #plotcluster()
    #plotZ()
    __genget(2865)
