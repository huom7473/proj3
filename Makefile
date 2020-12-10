# NAME: Michael Huo, Tygan Zeng
# EMAIL: huom7473@ucla.edu, zengtygan@gmail.com
# ID: 705408359, 705391071

.PHONY: clean dist default

default: lab3b

lab3b:
	@ln -s lab3b.py lab3b

clean:
	@rm -f lab3b lab3b-705408359.tar.gz

dist:
	@tar -czf lab3b-705408359.tar.gz lab3b.py Makefile README
