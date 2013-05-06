TUSRC=$(wildcard *.t*)
PYSRC=tron_sample.py tron-win32.py
SRC=$(TUSRC) $(PYSRC)
OUT=tron.zip tron-win32.zip
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
clean:
	rm -f $(OUT) $(wildcard tron-win32-support/__*__.py)
	rm -rf tron-win32/
	find -name \*.pyc -delete
.PHONY:clean all
