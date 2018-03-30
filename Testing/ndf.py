from util import *
from plot import *

def getNDF(filename):
    L = processInput(filename)
    oriPlot(L)
    L1 = sorted(L, key=lambda x:x[0][1], reverse=True)
    L2 = sorted(L, key=lambda x:x[0][0])
    checked = []
    ndf = []

    for si in L1:
        checked.append(si)
        for sj in L2:
            if sj not in checked:
                if si is not None:
                    if si[0] != sj[0] or si[1] != sj[1]:
                        while si is not None:
                            s_ndf,s_r = intercept(si, sj)
                            si = s_r
                            if s_ndf is not None:
                                ndf.append(s_ndf)
    #myPlot(L, ndf)
    return(ndf)

'''
split s1 based on points in s2

input:
    si, sj -> slices
output:
    s_ndf: the nondominated frontier from splitting si by sj
    s_r: the remaining slice from si after the split
'''
def intercept(si, sj):
    s_ndf = []
    s_r = si

    k = 0

    while s_r is not None and len(s_r) > 0 and k <= len(sj):
        pix = between_z1(si, sj[k])
        piy = between_z2(si, sj[k])
        pn = intercept2(si, sj, k)
        print('pn', pn, pix, piy)
        ndf = None
        r = None

        if pix is not None or piy is not None:
            if pn is not None:
                if pix is None:
                    ndf,r = split(si, k+1, pn, piy)
                if piy is None:
                    ndf,r = split(si, k+1, pix, pn)
            else:
                ndf,r = split(si, k+1, pix, piy)

        k += 1
        if ndf is not None:
            s_ndf.append(ndf)
        s_r = r
    return (s_ndf, s_r)

'''
find the vertical intercept of a point and a slice (a line segment on the slice)

input:
    s -> a slice, list of points
    p -> a point, tuple of z1-coordinates and z2-coordinates
output:
    1) a point if there is a vertical intercept, the intercepting point
    2) None otherwise

*** can merge with between_z2
'''
def between_z1(s, p):
    indices = inbetween(p[0], s, 0)
    if indices is not None:
        x,y = pointOnSegment(s[indices[0]], s[indices[1]], p[0], 0)
        if y > p[1]:
            return (x,y)
        else:
            return None
    else:
        return None

'''
find the horizontal intercept of a point and a slice (a line segment on the slice)

input:
    s -> a slice, list of points
    p -> a point, tuple of z1-coordinates and z2-coordinates
output:
    1) a point if there is a horizontal intercept, the interception point
    2) None otherwise

*** can merge with between_z1
'''
def between_z2(s, p):
    indices = inbetween(p[1], s, 1)
    if indices is not None:
        x,y = pointOnSegment(s[indices[0]], s[indices[1]], p[1], 1)
        if x > p[0]:
            return (x,y)
        else:
            return None
    else:
        return None

'''
find the interception of a slice and a line segment (made by the current point and the next point)

input:
    si -> a slice
    sj -> another slice, slice j
    index_j -> index of the current point on slice
output:
    1) a point if there is an interception, the intercepting point
    2) None otherwise
'''
def intercept2(si, sj, index_j):
    if index_j >= len(sj):
        return None
    else:
        pj0 = sj[index_j]
        pj1 = sj[index_j+1]
        for i in range(len(si)-1):
            pi0 = si[i]
            pi1 = si[i+1]
            return getIntercept(pi0, pi1, pj0, pj1)
'''
split the current slice into non-domindated slice and remaining slice

input:
    s -> current slice
    index -> the index of the ending point of a slice segment that px or py is on
    px -> point resulting from a vertical intercept
    py -> point resulting from a horizontal intercept
output:
    s_ndf: the slice that is part of the non-dominated frontier
    s_r: the remaining slice
    None if the inputs are invalid (px and py are both None)
'''
def split(s, index, px=None, py=None):
    s_ndf = None
    s_r = None
    if px is not None or py is not None:
        if px is None:
            s_r = [py]
            s_r.append(s[index:])
        if py is None:
            i = index - 1
            s_ndf = s[:i]
            s_ndf.append(px)
    return (s_ndf, s_r)

if __name__ == '__main__':
    getNDF('test.csv')



