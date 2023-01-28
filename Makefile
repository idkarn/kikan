clean:
	rm -rf dist

run:
	python3 src/kikan/main.py

watch:
	python3 monitor.py src/kikan/main.py
