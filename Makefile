TUSRC=$(wildcard *.t*)
PYSRC=tron_sample.py tron.py
SRC=$(TUSRC) $(PYSRC)
OUT=tron.zip tron-win32.zip negamax
all:$(OUT)
tron-win32-support/__main__.py:tron.py
	cp $< $@
tron-win32:tron-win32-support/__main__.py $(SRC)
	rm -rf tron-win32/
	mkdir tron-win32/
	cp tron_sample.py $(TUSRC) tron-win32/
	cp tron-win32.py tron-win32/tron.py
	cd tron-win32-support/ && zip -rq ../tron-win32/tron-win32-support.zip * -x \*.pyc
tron-win32.zip:tron-win32
	zip -rq $@ $<
tron.zip:$(SRC)
	zip tron.zip $(SRC)
mainline:
	git clone git://gitorious.org/shedskin/mainline.git
	cd mainline && python setup.py build
negamax/negamax.cpp:negamax.py mainline
	rm -rf negamax
	mkdir -p negamax
	cp negamax{.py,}
	cd negamax && PYTHONPATH=../mainline/build/lib python -c 'import shedskin;shedskin.main()' negamax.py
negamax/negamax:negamax/negamax.cpp
	cd negamax && make
negamax:negamax/negamax
	cp {negamax/,}negamax
clean:
	rm -f $(OUT) $(wildcard tron-win32-support/__*__.py)
	rm -rf tron-win32/
	find -name \*.pyc -delete
.PHONY:clean all
