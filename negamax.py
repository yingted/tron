#!/usr/bin/python
from struct import calcsize,unpack,pack
TCP_NODELAY=1
import socket
STRUCT_DOWN_FRAME="<iii307s"#"<iii%ds"%((50*49+7)/8)
STRUCT_UP_MOVE="<iii"
STRUCT_UP_LOGIN="<256s256s"
IPPROTO_TCP=6
TCP_NODELAY=1
TCP_QUICKACK=12
SHUT_RDWR=2
PORT=12345
class TronClient(object):
	"""non-threadsafe client which mimics the Turing API"""
	OUTCOME="tie","win","lose","tie"
	def __init__(self):
		self._t=self._x=self._y=self.t=self.x=self.y=-1
		self.outcome="ongoing"
		self.sock=None
		self.full=[[False]*49 for _ in xrange(50)]
		self.dropped=0
	def start(self,user=None,pw=None,host="",port=PORT):
		self.sock=socket.socket()
		self.sock.connect((host,port))
		self.sock.setsockopt(IPPROTO_TCP,TCP_NODELAY,1)
		buf=""
		if user is not None:
			buf+='L'+pack(STRUCT_UP_LOGIN,user,pw)
		buf+='S'
		self.sock.sendall(buf)
	def _recv(self):
		self._t,self._x,self._y,a=unpack(STRUCT_DOWN_FRAME,self.sock.recv(calcsize(STRUCT_DOWN_FRAME)))
		self.sock.setsockopt(IPPROTO_TCP,TCP_QUICKACK,1)
		self._t-=1
		self._x-=1
		self._y-=1
		if self._x!=-1:
			self.t=self._t+1
			if self._t>1 and(self.x!=self._x or self.y!=self._y):
				self.dropped+=1
			self.x=self._x
			self.y=self._y
		else:
			self._close()
			outcome=TronClient.OUTCOME[self._y+1]
			self.__init__()
			self.outcome=outcome
		for i in xrange(50):
			for j in xrange(49):
				k=i*49+j
				self.full[i][j]=(ord(a[k/8])>>(k%8))&1==1
	def ended(self):
		if not self.sock:
			return True
		try:
			if self.t>=0:
				assert abs(self._x-self.x)+abs(self._y-self.y)<=self.t-self._t
				self.sock.sendall(pack(STRUCT_UP_MOVE,self.t+1,self.x+1,self.y+1))
			self._recv()
		except IOError:
			self._close()
		return not self.sock
	def _close(self):
		self.sock.shutdown(SHUT_RDWR)
		try:
			self.sock.close()
		except:
			pass
		self.sock=None
from random import choice
a=[[False]*49 for _ in xrange(50)]
def near(x,y):
	for nx,ny in(x-1,y),(x+1,y),(x,y-1),(x,y+1):
		if 0<=nx<50 and 0<=ny<49 and not a[nx][ny]:
			yield nx,ny
def near_ordered(me,you):
	pts=[]
	for p in near(me[0],me[1]):
		a[p[0]][p[1]]=True
		pts.append((-val(p,you),p))
		a[p[0]][p[1]]=False
	return[x[1]for x in sorted(pts)]
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
	for x,y in near(me[0],me[1]):
		if dyou[x][y]!=float("inf"):
			return sum(cmp(x,y)for row in map(zip,dyou,dme)for x,y in row)
	return 20*(sum(v==float("inf")for row in dyou for v in row)-sum(v==float("inf")for row in dme for v in row))+88*(sum(len(list(near(i,j)))for i in xrange(50)for j in xrange(49)if not a[i][j]))
def negamax((mex,mey),(youx,youy),depth,alpha,beta):
	if not depth:
		return val((mex,mey),(youx,youy))
	you=youx,youy
	for nx,ny in near_ordered((mex,mey),you):
		a[nx][ny]=True
		v=-negamax(you,(nx,ny),depth-1,-beta,-alpha)
		a[nx][ny]=False
		if v>=beta:
			return v
		if v>alpha:
			alpha=v
	return alpha
def alphabeta(me,you,alpha=-float("inf")):
	"""gets moves from negamax by expanding out the first ply"""
	moves=[]
	for x,y in near_ordered(me,you):
		pos=x,y
		assert not a[x][y]
		a[x][y]=True
		v=-negamax(you,pos,3,-float("inf"),1-alpha)
		a[x][y]=False
		if v>alpha:
			alpha=v
			moves=[]
		if v==alpha:
			moves.append(pos)
	print"hope for",alpha
	return moves
tron=TronClient()
tron.start("negamax-0.1","35fad903-2ed3-4c95-8e91-bae44dbc52c3","192.168.0.4")
while not tron.ended():
	me=tron.x,tron.y
	you=next((i,j)for i in xrange(50)for j in xrange(49)if tron.full[i][j]and not a[i][j]and(i,j)!=me)
	a=[[v for v in row]for row in tron.full]
	print"val",val(me,you)
	try:
		tron.x,tron.y=choice(alphabeta(me,you))
	except IndexError:
		print"no good moves"
		tron.x+=1
print tron
