.PHONY: run test clean
# make необходимо установить и добавить в переменные среды (Path)
# чтоб запустить комманду необходимо в консоли набрать: make run
run:
	pyinstaller -F -w -n "Downloader" --icon=./src/data/favicon.ico src/main.py

test:
	python3 -m unittest discover -s tests

clean:
	rm -rf build Downloader.spec

