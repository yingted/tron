module tron
    export var x,var y,var t,var show,full,outcome,start,startlogin,ended
    var _x,_y,_t,x,y,t,fd,dropped:int
    var full:array 1..50,1..49 of boolean
    var buf:array 0..(50*49-1)div 8 of char
    var outcome:string
    var show:=false
    var win:=-1
    var OUTCOME:array 0..3 of string:=init("tie","win","lose","tie")
    proc zero
	_t:=0
	_x:=0
	_y:=0
	t:=0
	x:=0
	y:=0
	fd:=0
	dropped:=0
	outcome:="ongoing"
	for i:1..50
	    for j:1..49
		full(i,j):=false
	    end for
	end for
	if win~=-1 then
	    Window.Close(win)
	    win:=-1
	end if
    end zero
    zero
    proc reset
	pre fd>0
	Net.CloseConnection(fd)
	zero
    end reset
    proc recv
	pre fd>0%check ended first
	handler(e)
	    case e of
		label 2300:
		    reset
		    outcome:="socket closed"
		label:
		    quit >
	    end case
	end handler
	external fcn net_connectionstatus(fd:int):int
	var rc:int
	const __x:=_x
	const __y:=_y
	const __t:=_t
	loop%this is what Turing does anyways; hope you have >1 physical core
	    exit when Net.BytesAvailable(fd)>0
	end loop
	read:fd:rc,_t,_x,_y,buf
	%rc=net_connectionstatus(fd)=0 always, but Net.BytesAvailable(fd)=1
	%when EOF has occurred. eof(fd) segfaults, so we do a sanity check
	if(rc~=0|net_connectionstatus(fd)~=0|Net.BytesAvailable(fd)=1)&(__t=0|(_t~=__t+1&(_x-__x)*(_x-__x)+(_y-__y)*(_y-__y)~=1))&_t>0&_x<1&_x>50&_y<1&_y>49 then
	    reset
	end if
	if __t~=0&(_x~=x|_y~=y)then
	    dropped+=1
	end if
	var s:=0
	for i:1..50
	    for j:1..49
		const k:=(i-1)*49+j-1
		const v:=(ord(buf(k div 8))shr(k mod 8))&1
		full(i,j):=v=1
		s+=v
	    end for
	end for
	if _x=0 then
	    const _outcome:=OUTCOME(_y)
	    reset
	    outcome:=_outcome
	elsif s-2*_t<0|s-2*_t>2 then
	    reset
	else
	    x:=_x
	    y:=_y
	    t:=_t+1
	end if
	if show&fd>0 then
	    const active:=Window.GetActive
	    if win=-1 then
		win:=Window.Open("position:top;right,graphics:201;197;offscreenonly")
	    else
		Window.SetActive(win)
	    end if
	    for i:1..50
		for j:1..49
		    var clr:=white
		    if i=_x&j=_y then
			clr:=cyan
		    elsif full(i,j)then
			clr:=grey
		    end if
		    drawfillbox(maxx*(i-1)div 50,maxy*(j-1)div 49,maxx*i div 50,maxy*j div 49,clr)
		    drawbox(maxx*(i-1)div 50,maxy*(j-1)div 49,maxx*i div 50,maxy*j div 49,black)
		end for
	    end for
	    View.Update
	    if active>=-1 then
		Window.SetActive(active)
	    end if
	elsif win~=-1 then
	    Window.Close(win)
	    win:=-1
	end if
    end recv
    proc connect(host:string,port:int)
	assert fd<=0
	external proc net_registeropen(fd:int)
	%Turing's text mode put/get is broken since the developer used
	%tail=(tail+1)%128*1024 instead of tail=(tail+1)%(128*1024)
	%This leads to an infinite loop
	open:fd,"%net(C:"+intstr(port)+":"+host+")",read,write
	if fd>0 then
	    net_registeropen(fd)%part of the contract
	else
	    Error.Halt("Could not connect to "+host+":"+intstr(port))
	end if
    end connect
    proc start(host:string,port:int)
	connect(host,port)
	const buf:='T'
	write:fd,buf
    end start
    proc startlogin(user:string,pass:string,host:string,port:int)
	connect(host,port)
	var buf:char(514)
	buf(1):='L'
	cheat(string,buf(2)):=user
	cheat(string,buf(258)):=pass
	buf(514):='T'%special code for turing-friendly connections
	write:fd,buf
    end startlogin
    fcn ended():boolean
	if fd<=0 then
	    result true
	end if
	assert abs(x-_x)+abs(y-_y)<=t-_t
	if t>0 then
	    var rc:int
	    var buf:char(12)
	    cheat(int,buf):=t
	    cheat(int,buf(5)):=x
	    cheat(int,buf(9)):=y
	    write:fd:rc,buf
	    if rc~=0 then reset end if
	end if
	recv
	result fd<=0
    end ended
end tron
