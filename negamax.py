#!/usr/bin/python
from tron import TronClient
from random import choice
a=[[False]*49 for _ in xrange(50)]
def near(x,y):
	for nx,ny in(x-1,y),(x+1,y),(x,y-1),(x,y+1):
		if 0<=nx<50 and 0<=ny<49 and not a[nx][ny]:
			yield nx,ny
def near_ordered(me,you):
	return[p for _,p in sorted([(-val(p,you),p)for p in near(*me)])]
def bfs(me,inf=float("inf")):
	q=[me]
	dist=[[inf]*49 for _ in xrange(50)]
	dist[me[0]][me[1]]=0
	seen={me}
	for x,y in q:
		d=dist[x][y]+1
		for nx,ny in near(x,y):
			if dist[nx][ny]is inf:
				dist[nx][ny]=d
				q.append((nx,ny))
	return dist
def val(me,you):
	dme=bfs(me)
	dyou=bfs(you)
	if dyou[me[0]][me[1]]is None:
		return 20*(sum(not v for row in dyou for v in row)-sum(not v for row in dme for v in row))
	return sum(cmp(x,y)for row in map(zip,dyou,dme)for x,y in row)
def negamax((mex,mey),(youx,youy),depth,alpha,beta):
	if not depth:
		return val((mex,mey),(youx,youy))
	a[mex][mey]=True
	you=youx,youy
	for nx,ny in near_ordered((mex,mey),you):
		if not a[nx][ny]:
			v=-negamax(you,(nx,ny),depth-1,-beta,-alpha)
			if v>=beta:
				a[mex][mey]=False
				return v
			if v>alpha:
				alpha=v
	a[mex][mey]=False
	return alpha
def alphabeta(me,you,alpha=-float("inf")):
	"""gets moves from negamax by expanding out the first 2 plies"""
	moves=[]
	for mex,mey in near_ordered(me,you):
		if not a[mex][mey]:
			pos=mex,mey
			beta=float("inf")
			for nx,ny in near_ordered(you,pos):
				if not a[nx][ny]:
					v=negamax(pos,(nx,ny),2,alpha,beta)
					if v<beta:
						beta=v
					if v<=alpha:
						break
			if beta>alpha:
				alpha=beta
				moves=[]
			if beta==alpha:
				moves.append((mex,mey))
	print"hoped alpha",alpha
	return moves
for tron in TronClient("negamax-0.1","35fad903-2ed3-4c95-8e91-bae44dbc52c3","192.168.0.4"):
	me=tron.x,tron.y
	you=next((i,j)for i in xrange(50)for j in xrange(49)if tron.full[i][j]and not a[i][j]and(i,j)!=me)
	a=[[v for v in row]for row in tron.full]
	print"val",val(me,you)
	try:
		tron.x,tron.y=choice(alphabeta(me,you))
	except IndexError:
		pass
print tron
