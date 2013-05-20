#!/usr/bin/python2
from twisted.internet import reactor
from twisted.internet.protocol import Factory
from twisted.internet.task import LoopingCall
from twisted.protocols.stateful import StatefulProtocol
from random import shuffle
from threading import Lock
from struct import calcsize,unpack,pack
from socket import create_connection,SHUT_RDWR,error
from collections import Counter,Iterable
from hashlib import sha512
from base64 import urlsafe_b64encode
import socket
for const in"IPPROTO_TCP","TCP_QUICKACK","TCP_NODELAY":
	globals()[const]=getattr(socket,const)if hasattr(socket,const)else 0
def setsockopt(sock,level=IPPROTO_TCP,option=TCP_QUICKACK,value=1):
	if level and option:
		sock.setsockopt(level,option,value)
try:
	from Tkinter import Tk,Canvas,ALL
except ImportError:
	pass
from sys import argv
STRUCT_DOWN_FRAME="<iii%ds"%((50*49+7)/8)
STRUCT_UP_MOVE="<iii"
STRUCT_UP_LOGIN="<256s256s"
PORT=12345
def synchronized(func):
	lock=Lock()
	def synchronized(*args,**kwargs):
		with lock:
			return func(*args,**kwargs)
	return synchronized
def reads(spec):
	def decorator(func):
		def handler(self,data):
			return func(self,*unpack(spec,data))
		handler.size=calcsize(spec)
		return handler
	return decorator
def getstate(handler):
	return handler,handler.size
salt=sha512()
salt.update("5c425c0e-c1bc-4165-8735-690e80bdf19a")
def pw_hash(pw):
	m=salt.copy()
	m.update(pw)
	return urlsafe_b64encode(m.digest())
class Event(object):
	def __init__(self):
		self.handlers=[]
	def __iadd__(self,cb):
		self.handlers.append(cb)
		return self
	def __isub__(self,cb):
		self.handlers.remove(cb)
		return self
	def __call__(self,*args,**kwargs):
		for cb in self.handlers:
			cb(*args,**kwargs)
class Game(object):
	"""delay between frames or none if falsy"""
	def __init__(self,**kwargs):
		self.delay=.1
		self.lock=Lock()
		self.next=Event()
		self.start=Event()
		self.next+=self._advance
		self.end=Event()
		self.log=None
		self.users=[]
		self.grid=[[False]*49 for _ in xrange(50)]
		self.state=[(11,24,12,24),(38,24,37,24)]
		init=kwargs.pop("__init__",None)
		for k,v in kwargs.iteritems():
			attr=getattr(self,k)
			if isinstance(attr,Event):
				if not isinstance(v,Iterable):
					v=v,
				for v in v:
					attr+=v
			else:
				setattr(self,k,v)
		shuffle(self.state)
		if init:
			init(self)
		if self.log is not None:
			for i,st in enumerate(self.state):
				self.log[i,-1]=st[:2]
				self.log[i,0]=st[2:]
		self.t=-1
		if not self.delay:
			self.ready=[False]*2
	@synchronized
	def _advance(self):
		self.t+=1#advance time anyway
		if not self.over():
			for i,(x,y,nx,ny)in enumerate(self.state):
				self.state[i]=nx,ny,nx*2-x,ny*2-y
			count=Counter(state[:2]for state in self.state)
			for i,(x,y,nx,ny)in enumerate(self.state):
				if not(0<=x<50 and 0<=y<49)or self.grid[x][y]or count[x,y]>1:
					self.state[i]=None
		if self.over():
			if self.delay:
				self.loop.stop()
			if self.end:
				self.end(self)
				self.end=None
		else:
			for x,y,nx,ny in self.state:
				self.grid[x][y]=True
			a=[v for row in self.grid for v in row]
			self.bitmap="".join([chr(reduce(lambda s,v:s*2+v,a[i:i+8][::-1]))for i in xrange(0,len(a),8)])
	@synchronized
	def join(self,user=None,pw=None,andQuit=False):
		"""yields the id and joins; if play is false, then invalidate"""
		i=len(self.users)
		self.users.append((user,pw))
		if andQuit:
			self.state[i]=False
			return
		yield i
		if len(self.users)==2:
			self.start(self)
			if self.delay:
				self.loop=LoopingCall(self.next)
				self.loop.start(self.delay)
			else:
				self.next()
	def update(self,i,t,nx,ny):
		if t==self.t+1 and self.state[i]:
			x,y,_,_=self.state[i]
			if(x-nx)**2+(y-ny)**2==1:
				self.state[i]=x,y,nx,ny
				if self.log is not None:
					self.log[i,t]=nx,ny
				if not self.delay:
					self.ready[i]=True
					if all(self.ready):
						self.ready=[False]*len(self.ready)
						self.next()
		else:
			print"received frame",t,"@",self.t
	def over(self):
		return None in self.state
class Tron(StatefulProtocol):
	def __init__(self,game):
		self.game=game
		self.id=None
		self.turing=False
		self.user=self.pw=None
		game.next+=self._updateRemote
	def connectionMade(self):
		setsockopt(self.transport.socket,option=TCP_NODELAY)
	def _updateRemote(self):
		if self.id is None:
			return
		if self.game.over():
			pos=-1,-1+self.game.state.count(None)+(self.game.state[self.id]is None)
		else:
			pos=self.game.state[self.id]
		self.transport.write(pack(STRUCT_DOWN_FRAME,self.game.t+1,pos[0]+1,pos[1]+1,self.game.bitmap))
		if self.game.over()and not self.turing:
			self.transport.loseConnection()
	def getInitialState(self):
		return getstate(self._switch)
	@reads("c")
	def _switch(self,cmd):
		if cmd=='L':
			return getstate(self._login)
		elif cmd in"ST":
			if cmd=='T':
				self.turing=True
			for i in self.game.join(self.user,self.pw):
				self.id=i
			return getstate(self._updateLocal)
		else:
			self.transport.loseConnection()
	@reads(STRUCT_UP_MOVE)
	def _updateLocal(self,t,x,y):
		setsockopt(self.transport.socket)
		self.game.update(self.id,t-1,x-1,y-1)
	@reads(STRUCT_UP_LOGIN)
	def _login(self,user,pw):
		self.user=None if user is None else user.rstrip('\0')
		self.pw=None if pw is None else pw_hash(pw.rstrip('\0'))
		return getstate(self._switch)
	def connectionLost(self,reason):
		self.game.next-=self._updateRemote
		if self.id is None:
			self.game.join(andQuit=True)
		else:
			self.game.state[self.id]=None
		if not self.game.delay:
			self.game.next()
		self.game=None
class TronFactory(Factory):
	def __init__(self,prefs={}):
		self.game=None
		self.prefs=prefs
	@synchronized
	def buildProtocol(self,addr):
		print"client from",addr
		if self.game and self.game.over():
			self.game=None
		if self.game:
			tron=Tron(self.game)
			self.game=None
			return tron
		else:
			self.game=Game(**self.prefs)
			return Tron(self.game)
class TronClient(object):
	"""non-threadsafe client which mimics the Turing API"""
	OUTCOME="tie","win","lose","tie"
	def __init__(self,*args):
		self._t=self._x=self._y=self.t=self.x=self.y=-1
		self.outcome="ongoing"
		self.sock=None
		self.full=[[False]*49 for _ in xrange(50)]
		self.show=False
		self.root=self.cvs=None
		self.dropped=0
		if args:
			self.start(*args)
	def start(self,user=None,pw=None,host="",port=PORT):
		if isinstance(user,str)and not isinstance(pw,str):
			user,pw,host,port=None,None,user,pw if pw is not None else port
		self.sock=create_connection((host,port))
		setsockopt(self.sock,option=TCP_NODELAY)
		buf=""
		if user is not None:
			buf+='L'+pack(STRUCT_UP_LOGIN,user,pw)
		buf+='S'
		self.sock.sendall(buf)
	startlogin=start
	def _recv(self):
		self._t,self._x,self._y,a=unpack(STRUCT_DOWN_FRAME,self.sock.recv(calcsize(STRUCT_DOWN_FRAME)))
		setsockopt(self.sock)
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
			outcome=self.OUTCOME[self._y+1]
			self.__init__()
			self.outcome=outcome
		for i in xrange(50):
			for j in xrange(49):
				k=i*49+j
				self.full[i][j]=(ord(a[k/8])>>(k%8))&1==1
		if self.show:
			if not self.root:
				self.root=Tk()
				self.root.resizable(0,0)
				self.root.protocol("WM_DELETE_WINDOW",self._close)
				self.root.wm_title(argv[0])
				self.cvs=Canvas(self.root,width=201,height=197,highlightthickness=0)
				self.cvs.pack()
				self.rects=[[self.cvs.create_rectangle(4*i,4*j,4*(i+1),4*(j+1))for j in reversed(xrange(49))]for i in xrange(50)]
			for i in xrange(50):
				for j in xrange(49):
					self.cvs.itemconfig(self.rects[i][j],fill="#088"if i==self.x and j==self.y else"#ccc"if self.full[i][j]else"white")
			self.root.update()
		elif self.root:
			self.root.destroy()
			self.root=self.cvs=self.rects=None
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
		if self.sock:
			try:
				self.sock.shutdown(SHUT_RDWR)
			except error:
				pass
		try:
			self.sock.close()
		except:
			pass
		self.sock=None
	def __iter__(self):
		while not self.ended():
			yield self
	def __repr__(self):
		return"<"+self.__class__.__name__+"@%(dropped)d/%(t)d (%(x)d,%(y)d) %(outcome)s>"%self.__dict__
if __name__=="__main__":
	from argparse import ArgumentParser
	p=ArgumentParser()
	p.add_argument("-d","--delay",dest="delay",action="store",const=0,type=float,nargs="?",help="max frame delay or 0 for none")
	p.add_argument("-l","--log",dest="log_prefix",action="store",const="tron-",nargs="?",help="produce game logs")
	p.add_argument("-p","--port",dest="port",action="store",default=PORT,type=int,help="custom game port")
	args=p.parse_args()
	prefs=dict((k,v)for k,v in vars(args).iteritems()if k in"delay",)
	if prefs["delay"]is None:
		del prefs["delay"]
	if args.log_prefix is not None:
		from json import dump
		from datetime import datetime
		from itertools import groupby
		def makelog(self):
			self.log={}
		prefs["__init__"]=makelog
		def compress(self):
			rle=[0]if self.grid[0][0]else[]
			rle.extend([len(list(g))for k,g in groupby([v for row in self.grid for v in row])])
			self._compressed_map=rle
		prefs["start"]=compress
		def save(self):
			log=[[]for _ in self.state]
			for k,v in self.log.iteritems():
				log[k[0]].append((k[1],v[0],v[1]))
			winner=None
			for i,v in enumerate(self.state):
				if v:
					winner=i
					break
			data={
				"users":map(list,self.users),
				"winner":winner,
				"log":log,
				"len":self.t,
				"map":self._compressed_map,
				"delay":args.delay,
			}
			with open("%s%d-%d.json"%(args.log_prefix,PORT,round((datetime.now()-datetime.fromtimestamp(0)).total_seconds()*1000000)),"w")as log:
				dump(data,log,separators=(",",":"))
		prefs["end"]=save
	reactor.listenTCP(args.port,TronFactory(prefs=prefs))
	reactor.run()
