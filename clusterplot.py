from matplotlib import pyplot as plt
from scipy.cluster.hierarchy import dendrogram, linkage
import numpy as np


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

if __name__ == '__main__':
    plotcluster()
    #plotZ()
