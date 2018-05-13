from util import *
from plot import *
from collections import deque

def getNDF(filename):
	L = processInput(filename)
	L1 = sorted(L, key=lambda x:x[0][1], reverse=True)
	L2 = sorted(L, key=lambda x:x[0][0])

	ndf = []
	checked = []

	for si in L1:
		checked.append(si)
		s_r = si
		newNdf = []
		for sj in L2:
			if s_r is None:
				break
			elif sj not in checked:
			#elif sj != si:
				#print(sj, s_r, 'current')
				covermode = coverMode(s_r, sj)
				if covermode == 1:
					break
				elif covermode == 0:
					ndf.append(s_r)
					newNdf.append(s_r)
				else:
					s_ndf, s_r = intercept(s_r, sj)

					if s_ndf is not None:
						ndf.append(s_ndf)
						newNdf.append(s_ndf)
			
		if s_r is not None:
			ndf.append(s_r)
			newNdf.append(s_r)
		L2.extend(newNdf)
		L2 = sorted(L2, key=lambda x:x[0][0])
		print('L2', L2)


	myPlot(L, ndf)
	return ndf

def intercept(si, sj):
	# si = list(set(si))
	# sj = list(set(sj))
	sndf = []
	s_r = si
	covermode = coverMode(si,sj)
	if covermode == 0:
		sndf = si
		s_r = None
	elif covermode == 1:
		sndf = None
		s_r = None
	else:
		p_intercept = sliceIntercept(si, sj)
		if len(p_intercept) == 0:
			pix = between_z1(si, sj[0])
			piy = between_z2(si, sj[-1])
			s_ndf, s_r = split(si, pix, piy)
			sndf.extend(s_ndf)


		else:
			for i in range(len(p_intercept)):
				if s_r is None:
					break
				mode, intercept, pi = p_intercept[i]
				if mode == 0:
					pix = between_z1(s_r, pi)
					s_ndf, s_r = split(s_r, pix, intercept)
					sndf.extend(s_ndf)
				elif mode == 1:
					piy = between_z2(s_r, pi)
					s_ndf, s_r = split(s_r, intercept, piy)
					sndf.extend(s_ndf)
	return (sndf, s_r)

def between_z1(s, p): # vertical split
	indices = inbetween(p[0], s, 0)

	if indices is not None:
		x,y = pointOnSegment(s[indices[0]], s[indices[1]], p[0], 0)
		if y >= p[1]:
			return (x,y)
		elif y < p[1]:
			return 'OPPO'
	return None

def between_z2(s, p): # horizontal split
	indices = inbetween(p[1], s, 1)

	if indices is not None:
		x,y = pointOnSegment(s[indices[0]], s[indices[1]], p[1], 1)
		if x >= p[0]:
			return (x,y)
		elif x < p[0]:
			return 'OPPO'
	return None

def intercept2(si, pj0, pj1):
	intercept = None
	i = 0
	pi0 = None
	pi1 = None
	mi = None
	while i < len(si)-1 and intercept is None:
		pi0 = si[i]
		pi1 = si[i+1]
		intercept = getIntercept(pi0, pi1, pj0, pj1)
		i += 1
	if intercept is not None:
		mi = getLineExpression(pi0, pi1)[0]
	return (intercept, mi)

def split(s, px=None, py=None):
	s_ndf = None
	s_r = None

	if px == 'OPPO' and py == 'OPPO':
		s_ndf = s
		s_r = None
	else:
		if px == 'OPPO':
			px = None
		if py == 'OPPO':
			py = None

		if px is not None:
			print(s, px, py)
			index_1 = inbetween(px[1], s, 1)[0]
			s_ndf = s[:index_1+1]
			s_ndf.append(px)

		if py is not None:
			index_2 = inbetween(py[1], s, 1)[1]
			s_r = [py]
			s_r.extend(s[index_2:])

	return (s_ndf, s_r)

if __name__ == '__main__':
	getNDF('test.csv')

		