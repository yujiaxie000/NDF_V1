

def getNDF(filename):
	L = processInput(filename)
	L1 = sorted(L, key=lambda x:x[0][1], reverse=True)
	L2 = sorted(L, key=lambda x:x[0][0])
	ndf = []
	#checked = []

	for si in L1:
		s_r = si
		#checked.append(si)
		for sj in L2:
			if s_r is None:
				break
			elif sj != si:
				covermode = coverMode(s_r, sj)
				if covermode == 1:
					break
				elif covermode == 0:
					ndf.append(s_r)
				else:
					sndf, s_r = intercept(s_r, sj)
					if sndf is not None:
						ndf.append(sndf)
		if s_r is not None:
			ndf.append(s_r)

	myPlot(L, ndf)

	return ndf

def getNDF(filename):
	L = processInput(filename)
	L1 = sorted(L, key=lambda x:x[0][1], reverse=True)
	L2 = sorted(L, key=lambda x:x[0][0])
	checked = []
	ndf = []

	for si in L1:
		s_r = si
		s_ndf = None

		for sj in L2:
			if s_r is not None and si != sj:
				print(si, sj)
				if si is not None:
				 	s_r_min = s_r[0]
					s_r_max = s_r[-1]
					sj_min = sj[0]
					sj_max = sj[-1]

					if s_r_max[0] < sj_min[0] and s_r_max[1] > sj_min[1]:
						ndf.append(s_r)
					elif s_r_min[0] < sj_min[0] and s_r_max[1] > sj_min[1]:
						s_r = None
					else:
						s_ndf, s_r = intercept(s_r, sj)
						print(s_ndf, s_r, 'NDF')
						if s_ndf is not None:
							ndf.extend(s_ndf)
		if s_r is not None:
			ndf.append(s_r)

		checked.append(si)


	myPlot(L, ndf)
	return(ndf)

def intercept(si, sj):
	s_ndf = []
	s_r = si 

	k = 0

	while k < len(sj) - 1 and s_r is not None and len(s_r) > 0:
		#print(k, 'ks')

		pix = between_z1(s_r, sj[k])
		piy = between_z2(s_r, sj[k+1])
		pn, mi = intercept2(s_r, sj[k], sj[k+1])


		if pn is not None:
			mj = getLineExpression(sj[k], sj[k+1])[0]
			if mi < mj:
				ndf, r = split(si, pix, pn)
			else:
				ndf, r = split(si, pn, piy)
		else:
			print(si, pix,piy, 'INTERCEPT')
			if
			ndf, r = split(si, pix, piy)

		k += 1
		if ndf is not None:
			s_ndf.append(ndf)
		s_r = r
	return (s_ndf, s_r)