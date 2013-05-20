#!/usr/bin/python2
from tron import TronClient
from random import random
for tron in TronClient("pysamplebot-1.0","will never change: d9c77f23-ffac-4a1e-9f7b-f12b747895ce","localhost"):#authentication is not encrypted
	tron.show=True
	q=[]
	for dx,dy in(-1,0),(1,0),(0,-1),(0,1):
		for i in xrange(1,50):
			x=tron.x+i*dx
			y=tron.y+i*dy
			if not(0<=x<50 and 0<=y<49)or tron.full[x][y]:
				break
		q.append((i-1,random(),tron.x+dx,tron.y+dy))
	tron.x,tron.y=max(q)[2:]
	#print"\n".join([" ".join("#"if y else" "for y in x)for x in reversed(zip(*tron.full))])
print tron
