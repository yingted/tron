#!/usr/bin/python2
from struct import calcsize,unpack,pack
import socket
TCP_NODELAY=1
STRUCT_DOWN_FRAME="<iii307s"
STRUCT_UP_MOVE="<iii"
STRUCT_UP_LOGIN="<256s256s"
IPPROTO_TCP=6
TCP_NODELAY=1
TCP_QUICKACK=12
SHUT_RDWR=2
PORT=12345
OO=float("inf")
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
                err=False
                if self.t>=0:
                        assert abs(self._x-self.x)+abs(self._y-self.y)<=self.t-self._t and(self.t!=self._t+1 or(self._x-self.x)**2+(self._y-self.y)**2==1)
                        try:
                                self.sock.sendall(pack(STRUCT_UP_MOVE,self.t+1,self.x+1,self.y+1))
                        except IOError:
                                err=True
                try:
                        self._recv()
                except IOError:
                        err=True
                if err:
                        self._close()
                return not self.sock
	def _close(self):
		self.sock.shutdown(SHUT_RDWR)
		try:
			self.sock.close()
		except:
			pass
		self.sock=None
	def __repr__(self):
		return"<%s@%d/%d (%d,%d) %s>"%(self.__class__.__name__,self.dropped,self.t,self.x,self.y,self.outcome)
from random import choice
a=[[False]*49 for _ in xrange(50)]
def near(x,y):
	return[(nx,ny)for nx,ny in(x-1,y),(x+1,y),(x,y-1),(x,y+1)if 0<=nx<50 and 0<=ny<49 and not a[nx][ny]]
def bfs(me):
	q=[me]
	dist=[[OO]*49 for _ in xrange(50)]
	dist[me[0]][me[1]]=0.
	for x,y in q:
		d=dist[x][y]+1.
		for nx,ny in near(x,y):
			#if dist[nx][ny]is OO:
			if dist[nx][ny]==OO:
				dist[nx][ny]=d
				q.append((nx,ny))
	return dist
def val(me,you):
	dme=bfs(me)
	dyou=bfs(you)
	for x,y in near(me[0],me[1]):
		if dyou[x][y]is not OO:
			s=0
			for i in xrange(50):
				for j in xrange(49):
					dx=dyou[i][j]
					dy=dme[i][j]
					s+=(dx>dy)-(dy>dx)
			return s
	return 20*(sum(v==OO for row in dyou for v in row)-sum(v==OO for row in dme for v in row))+88*(sum(len(near(i,j))for i in xrange(50)for j in xrange(49)if dme[i][j]!=OO)-sum(len(near(i,j))for i in xrange(50)for j in xrange(49)if dyou[i][j]is not OO))
	#return 20*(sum(v is OO for row in dyou for v in row)-sum(v is OO for row in dme for v in row))+88*(sum(len(near(i,j))for i in xrange(50)for j in xrange(49)if dme[i][j]is not OO)-sum(len(near(i,j))for i in xrange(50)for j in xrange(49)if dyou[i][j]is not OO))
def negamax((mex,mey),(youx,youy),depth,alpha,beta):
	if not depth:
		return val((mex,mey),(youx,youy))
	you=youx,youy
	for nx,ny in near(mex,mey):
		a[nx][ny]=True
		v=-negamax(you,(nx,ny),depth-1,-beta,-alpha)
		a[nx][ny]=False
		if v>=beta:
			return v
		if v>alpha:
			alpha=v
	return alpha
def alphabeta(me,you,alpha=-OO):
	"""gets moves from negamax by expanding out the first ply"""
	moves=[]
	for x,y in near(me[0],me[1]):
		pos=x,y
		assert not a[x][y]
		a[x][y]=True
		v=-negamax(you,pos,3,-OO,1-alpha)
		a[x][y]=False
		if v>alpha:
			alpha=v
			moves=[]
		if v==alpha:
			moves.append(pos)
	print"hope for",alpha
	return moves
from time import time
import sys
#{
sys.setcheckinterval(2**31-1)
def main():
	"""
#}
if True:
#{
"""
	global a
	#}
	tron=TronClient()
	host="localhost"
	port=PORT
	if len(sys.argv)>1:
		host=sys.argv[1]
		if len(sys.argv)>2:
			port=int(sys.argv[2])
	tron.start("negamax-0.1","35fad903-2ed3-4c95-8e91-bae44dbc52c3",host,port)
	while not tron.ended():
		starttime=time()
		me=tron.x,tron.y
		you=next((i,j)for i in xrange(50)for j in xrange(49)if tron.full[i][j]and not a[i][j]and(i,j)!=me)
		a=[row[:]for row in tron.full]
		#print"val",val(me,you)
		moves=alphabeta(me,you)
		if moves:
			tron.x,tron.y=choice(moves)
		else:
			print"no moves"
			tron.x+=1
		print time()-starttime
	print tron
#{
main()
#import cProfile
#cProfile.run("main()")
#}
