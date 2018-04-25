def lofBin(x):
    return len(bin(abs(x))[2:])

if __name__=='__main__':
    x = 13
    print(lofBin(x))