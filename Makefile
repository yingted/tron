TUSRC=$(wildcard *.t*)
PYSRC=tron_sample.py tron.py tron_tester.py
SRC=$(TUSRC) $(PYSRC)
OUT=tron.zip tron-win32.zip negamax/negamax negamax_bin negamax4_bin
CPPFLAGS=-Ofast -ffast-math -fomit-frame-pointer
export CPPFLAGS
all:$(OUT)
tron-win32-support/__main__.py:tron.py
	cp $< $@
tron-win32:tron-win32-support/__main__.py $(SRC)
	rm -rf tron-win32/
	mkdir tron-win32/
	cp tron_{sample,tester}.py $(TUSRC) tron-win32/
	cp tron-win32.py tron-win32/tron.py
	cd tron-win32-support/ && zip -rq ../tron-win32/tron-win32-support.zip * -x \*.pyc
tron-win32.zip:tron-win32
	rm -f $@
	cd $</ && zip -rq ../$@ .
tron.zip:$(SRC)
	rm -f $@
	zip $@ $(SRC)
mainline:
	git clone git://gitorious.org/shedskin/mainline.git
	cd mainline && python setup.py build
negamax/negamax.cpp:negamax.py mainline
	rm -rf negamax
	mkdir -p negamax
	cp negamax{.py,}
	cd negamax && PYTHONPATH=../mainline/build/lib python -c 'import shedskin;shedskin.main()' -bors negamax.py
negamax/negamax:negamax/negamax.cpp
	cd negamax && $(MAKE)
gprof2dot.py:
	wget 'http://gprof2dot.jrfonseca.googlecode.com/git/gprof2dot.py'
clean:
	rm -f $(OUT) $(wildcard tron-win32-support/__*__.py) negamax_prof negamax_debug
	rm -rf tron-win32/
	find -name \*.pyc -delete
.PHONY:clean all
SHEDSKIN_LIBDIR=mainline/build/lib/shedskin/lib
CC=g++
CCFLAGS=-O2 -march=native -Wno-deprecated $(CPPFLAGS) -I. -I${SHEDSKIN_LIBDIR} -D__SS_NOBOUNDS -D__SS_FASTRANDOM -D__SS_NOASSERT -D__SS_FASTHASH
LFLAGS=-lgc -lpcre $(LDFLAGS)

CPPFILES=negamax.cpp \
	${SHEDSKIN_LIBDIR}/time.cpp \
	${SHEDSKIN_LIBDIR}/sys.cpp \
	${SHEDSKIN_LIBDIR}/struct.cpp \
	${SHEDSKIN_LIBDIR}/socket.cpp \
	${SHEDSKIN_LIBDIR}/re.cpp \
	${SHEDSKIN_LIBDIR}/random.cpp \
	${SHEDSKIN_LIBDIR}/math.cpp \
	${SHEDSKIN_LIBDIR}/builtin.cpp

HPPFILES=negamax.hpp \
	${SHEDSKIN_LIBDIR}/time.hpp \
	${SHEDSKIN_LIBDIR}/sys.hpp \
	${SHEDSKIN_LIBDIR}/struct.hpp \
	${SHEDSKIN_LIBDIR}/socket.hpp \
	${SHEDSKIN_LIBDIR}/re.hpp \
	${SHEDSKIN_LIBDIR}/random.hpp \
	${SHEDSKIN_LIBDIR}/math.hpp \
	${SHEDSKIN_LIBDIR}/builtin.hpp

negamax_bin:	$(CPPFILES) $(HPPFILES)
	$(CC)  $(CCFLAGS) $(CPPFILES) $(LFLAGS) -o negamax_bin

negamax4_bin:	$(CPPFILES) $(HPPFILES)
	$(CC)  $(CCFLAGS) $(CPPFILES) $(LFLAGS) -DDEPTH=4 -o negamax4_bin

negamax_prof:	$(CPPFILES) $(HPPFILES)
	$(CC) -pg -ggdb $(CCFLAGS) $(CPPFILES) $(LFLAGS) -o negamax_prof

negamax_debug:	$(CPPFILES) $(HPPFILES)
	$(CC) -g -ggdb $(CCFLAGS) $(CPPFILES) $(LFLAGS) -o negamax_debug
