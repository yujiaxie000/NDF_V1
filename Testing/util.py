import csv
from sets import Set

'''
convert the data in the csv file to the appropriate format
L: list,  list of slices [s1, s2, ...]
si: list, the i-th slice, list of points [p1, p2, ...] in nondecreasing z1(x) order and in nonincreasing z2(y) order
pi: tuple, the i-th point, (pi1, pi2)

input: CSV filename
output: L
'''
def processInput(filename):
    Ltemp = []
    L = []
    with open(filename, 'r') as fin:
        csvReader = csv.reader(fin)
        for aLine in csvReader:
            if len(Ltemp) < int(aLine[4]):
                Ltemp.append([])
            Ltemp[int(aLine[4])-1].append((float(aLine[2]), float(aLine[3])))
    for ele in Ltemp:
        L.append(sortSlice(ele))
    return L
            
'''
sort the list of points in a slice in the nondecreasing z1(x) order and nonincreasing z2(y) order

input: a slice, list of tuples representing points
output: the ordered slice
'''
def sortSlice(aSlice):
    aSlice = sorted(aSlice, key=lambda x:(float(x[0]), -float(x[1])))
    return unique(aSlice)

'''
get the unique elements in a list

input: aList -> original list (with duplicates)
output: a list with unique elements
'''
def unique(aList):
    returned = []
    for element in aList:
        if (element[0], element[1]) not in returned:
            returned.append(element)
    return returned


'''
get the indices of two numbers from a List, which the aNum value falls between

input: 
    aNum -> a float
    aList -> list of tuple of float
    mode -> 0 if we want to compare aNum with the first element in the tuple; 1 if we want the second elemet
output:
    1) a tuple of indices if aNum falls between two numbers in aList
    2) None otherwise
'''
def inbetween(aNum, aList, mode):
    index = -1
    for num in aList:
        if mode == 0:
            if aNum >= num[0]:
                index += 1
        elif mode == 1:
            if aNum <= num[1]:
                index += 1
    if index == -1 or index >= len(aList)-1:
        return None
    else:
        return (index, index+1)

'''
given the coordinate (x or y) and a segment (defined by two points), find the point on the segment corresponding to that coordinate

input:
    p0, p1 -> end points of a segment
    coord -> x or y coordinate of the new point
    mode -> 0 if x-coordinate; 1 if y-coordinate
output:
    the point on the segment with the given coordinate
    None if the inputs are invalid
'''
def pointOnSegment(p0, p1, coord, mode):
    if mode == 0:
        lam = (coord - p1[0])/(p0[0]-p1[0])
        y = lam * p0[1] + (1-lam) * p1[1]
        return (coord, y)
    elif mode == 1:
        lam = (coord - p1[1])/(p0[1]-p1[1])
        x = lam * p0[0] + (1-lam) * p1[0]
        return (x, coord)
    else:
        return None 

'''
find the slope-intercept expression of a line given two end points

intput:
    p0, p1 -> two points
output:
    m -> slope of the line
    b -> incercept of the line
'''
def getLineExpression(p0, p1):
    x0,y0 = p0
    x1,y1 = p1
    m = (y0-y1)/(x0-x1)
    b = -x1 / (x0-x1) * (y0-y1) + y1
    return (m,b)

def getIntercept(pi0, pi1, pj0, pj1):
    xi0,yi0 = pi0
    xi1,yi1 = pi1
    xj0,yj0 = pj0
    xj1,yj1 = pi1
    print(pi0, pi1, pj0, pj1)
    print(max(xi0, xi1), min(xj0, xj1), )
    if max(xi0, xi1) < min(xj0, xj1) or max(xj0, xj1) < min(xi0, xi1):
        return None
    elif max(yi0, yi1) < min(yj0, yj1) or max(yj0, yj1) < min(yi0, yi1):
        return None
    else:
        mi,bi = getLineExpression(pi0, pi1)
        mj,bj = getLineExpression(pj0, pj1)
        if (mi-mj) < 0.01:
            return None
        x = (bj-bi)/(mi-mj)
        y = mi*x + bi
        print(mi, mj)
        print(x,y)
        return (x,y)

# if __name__ == '__main__':
#     processInput('dat.csv')
