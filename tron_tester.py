#!/usr/bin/python2
from tron import TronClient,STRUCT_UP_MOVE,pack
from thread import start_new_thread,allocate_lock
from Tkinter import Tk,Canvas
NAME="testbot-0.1"
tron=TronClient(NAME,"d5663c28-a8d1-487b-a878-f2f99355b3f2","localhost")
d=None
lock=allocate_lock()
def move_by(delta):
	global x,y,d
	msg=None
	with lock:
		x=tron.x+delta[0]
		y=tron.y+delta[1]
		d=delta
		if 0<=x<50 and 0<=y<49 and not tron.full[x][y]:
			msg=pack(STRUCT_UP_MOVE,tron.t+1,x+1,y+1)
	if msg is not None:
		try:
			tron.sock.sendall(msg)
		except IOError:
			tron._close()
def move(name,delta):
	def cb(e):
		move_by(delta)
	return cb
root=Tk()
root.resizable(0,0)
root.protocol("WM_DELETE_WINDOW",root.destroy)
root.wm_title(NAME)
cvs=Canvas(root,width=201,height=197,highlightthickness=0)
cvs.pack()
rects=[[cvs.create_rectangle(4*i,4*j,4*(i+1),4*(j+1))for j in reversed(xrange(49))]for i in xrange(50)]
if not tron.ended():
	for name,dx,dy in("Right",1,0),("Up",0,1),("Left",-1,0),("Down",0,-1):
		root.bind("<%s>"%name,move(name,(dx,dy)))
	tron._t+=1
	x=tron.x
	y=tron.y
	def main(tron):
		global x,y,d
		for tron in tron:#interferes with mainloop
			tron._t+=1
			with lock:
				if(x==tron.x and y==tron.y)or not d:
					continue
			move_by(d)
	def update():
		with lock:
			for i in xrange(50):
				for j in xrange(49):
					cvs.itemconfig(rects[i][j],fill="#088"if i==tron.x and j==tron.y else"#ccc"if tron.full[i][j]else"white")
		root.after(1,update)
	start_new_thread(main,(tron,))
	update()
	root.mainloop()
print tron
