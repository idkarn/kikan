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

test:
	tox run -e py

format:
	tox run -e format

lint:
	tox run -e lint

type:
	tox run -e type