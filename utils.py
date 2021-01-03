from numpy import *

def rand_pm():
    if random.random()<0.5:
        return -1
    else:
        return 1

def bool_pm(b):
    if b:
        return 1
    else:
        return -1

def w2s(a):
    #e.g., [-1,1,-1] -> 010 -> 2
    s = 0
    p = len(a)-1
    for i in a:
        if i == 1:
            s += 2**p
        p -= 1
    return s

def minority(d):
    if d<0:
        return 1
    elif d>0:
        return -1
    else:
        return rand_pm()
            
def max_idx(a):
    L = len(a)
    idx =[0]
    v = a[0]
    for i in range(1, L):
        if a[i] > v:
            idx = [i]
            v = a[i]
        elif a[i] == v:
            idx.append(i)
        else:
            continue
    i = random.randint(len(idx))
    return idx[i]