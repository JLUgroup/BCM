  


def data_calculate(partnum = None):
    a = open('distances.txt', 'r')
    b = open('calout.txt', 'w')

    numcount = []  
    for i in range(partnum):
        numcount.append(0)

    for data in a:
        pass
    length = float(data) / partnum
    a.seek(0,0)
    for data in a:
        data = float(data)
        for i in range(partnum):
            if  i*length < data < (i+1)*length:
                numcount[i]+=1
                break
    for i in range(partnum):
        b.write(str(numcount[i])+' '+str((i+1)*length))
        b.write('\n')

    b.close()
    a.close()

if __name__ == '__main__':
    data_calculate(10000)


