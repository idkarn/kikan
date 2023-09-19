PYTHON := python

empty:
	

clean:
	rm -rf dist

run:
	${PYTHON} src/kikan/main.py

watch:
	${PYTHON} monitor.py examples/example.py __pycache__,dist,logs

build:
	${PYTHON} -m build

publish:	
	${PYTHON} -m twine upload dist/*
