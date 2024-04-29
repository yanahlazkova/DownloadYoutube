.PHONY: run test clean

run:
	pyinstaller -F -w -n "Downloader" --icon=./src/data/favicon.ico src/main.py

test:
	python3 -m unittest discover -s tests

clean:
	rm -rf build Downloader.spec


