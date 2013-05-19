include"tron.tu"
tron.startlogin("samplebot-1.0",
    "will never change: d9c77f23-ffac-4a1e-9f7b-f12b747895ce",%authentication is not encrypted
    "localhost",
    12345)
tron.show:=true
loop
    exit when tron.ended()
    var random:real
    var bestd:=0
    const ox:=tron.x
    const oy:=tron.y
    for dx:-1..1
	for dy:-1..1
	    const r:=Rand.Real
	    if dx*dx+dy*dy=1 then
		for i:1..49
		    const x:=ox+i*dx
		    const y:=oy+i*dy
		    exit when x<1 or x>50 or y<1 or y>49 or tron.full(x,y)
		    if i>bestd or(i=bestd and r>random)then
			bestd:=i
			random:=r
			tron.x:=ox+dx
			tron.y:=oy+dy
		    end if
		end for
	    end if
	end for
    end for
end loop
put tron.outcome
