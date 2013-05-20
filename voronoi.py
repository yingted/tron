#!/usr/bin/python2
from tron import TronClient
from random import choice
from signal import signal,setitimer,SIGALRM,SIG_IGN,SIG_DFL,ITIMER_REAL
class FrameSkip(Exception):pass
def raise_frameskip(signum,frame):
	raise FrameSkip()
class guard(object):
	def __enter__(self):
		signal(SIGALRM,raise_frameskip)
	def __exit__(*args):
		signal(SIGALRM,SIG_IGN)
class every(object):
	def __init__(self,*spec):
		self.spec=spec
	def __enter__(self):
		signal(SIGALRM,SIG_IGN)
		setitimer(ITIMER_REAL,*self.spec)
		return guard()
	def __exit__(*args):
		setitimer(ITIMER_REAL,0)
		signal(SIGALRM,SIG_DFL)
a=[[False]*49 for _ in xrange(50)]
def good(x,y):
	return 0<=x<50 and 0<=y<49 and not a[x][y]
def circle((x,y)):
	return(x+1,y),(x,y+1),(x-1,y),(x,y-1)
def near(x,y):
	#return[(nx,ny)for nx,ny in circle((x,y))if good(nx,ny)]
	return[(nx,ny)for nx,ny in circle((x,y))if(0<=nx<50 and 0<=ny<49 and not a[nx][ny])]
def bfs(me,inf=float("inf")):
	q=[me]
	dist=[[inf]*49 for _ in xrange(50)]
	dist[me[0]][me[1]]=0
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
	for x,y in near(*me):
		if dyou[x][y]!=float("inf"):
			return sum(cmp(x,y)for row in map(zip,dyou,dme)for x,y in row),False
	return 20*(sum(v==float("inf")for row in dyou for v in row)-sum(v==float("inf")for row in dme for v in row)),True
def goodmoves(me,you):
	moves=[]
	best=-float("inf"),False
	for mex,mey in near(*me):
		#assert not a[mex][mey]
		a[mex][mey]=True
		v=val((mex,mey),you)
		a[mex][mey]=False
		if v>best:
			best=v
			moves=[]
		if v==best:
			moves.append((mex,mey))
	if best[1]and len(moves)>1:
		moves=wallhug(me,10)or wallhug(me,3)
	return moves or wallhug(me,1)
def wallhug(me,depth=3,theta=None):
	if theta is None:
		theta=angle
	pts=circle(me)
	for phi,(x,y)in enumerate(pts[theta-1:]+pts[:theta-1],theta-1):
		if good(x,y):
			if depth!=1:
				a[x][y]=True
				bad=not wallhug((x,y),depth-1,phi%4)
				a[x][y]=False
				if bad:
					continue
			return[(x,y)]
	return[]
angle=None
from time import time
def mainloop(tron):
	global angle,me,a
	starttime=time()
	try:
		if angle is None:
			angle=cmp(tron.x,24)+1
		me=tron.x,tron.y
		for i in xrange(50):
			for j in xrange(49):
				if tron.full[i][j]and not a[i][j]and(i,j)!=me:
					you=i,j
					break
		a=[row[:]for row in tron.full]
		try:
			tron.x,tron.y=choice(goodmoves(me,you))
			#assert a==[[v for v in row]for row in tron.full]
			#assert not tron.full[tron.x][tron.y]
			angle=circle(me).index((tron.x,tron.y))
		except IndexError:
			print"no good moves"
			tron.x+=1
		#print"\n".join([" ".join("#"if y else" "for y in x)for x in reversed(zip(*tron.full))])
	except FrameSkip:
		a=[row[:]for row in tron.full]
		tron.x,tron.y=(wallhug(me)or[(me[0]+1,me[1])])[0]
		print"frameskip"
	print time()-starttime
import platform
from sys import argv,setcheckinterval
from select import select
setcheckinterval(2**31-1)
if platform.python_implementation()=="PyPy":
	print"warmup start"
	for i in xrange(30):
		a[i][i]=True
	for _ in xrange(20):
		st=time()
		goodmoves((0,0),(20,20))
		print time()-st
	for i in xrange(30):
		a[i][i]=False
	print"warmup end"
args=argv[1:3]or["localhost"]
if len(args)>1:
	args[1]=int(args[1])
tron=TronClient("voronoi-0.1","35fad903-2ed3-4c95-8e91-bae44dbc52c3",*args)
if"-g"in argv[3:]:
	if not tron.ended():
		with every(.09,.1)as guard:
			with guard:
				mainloop(tron)
			for tron in tron:
				with guard:
					mainloop(tron)
else:
	for tron in tron:
		mainloop(tron)
print tron
