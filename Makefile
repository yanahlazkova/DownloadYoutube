.PHONY: run test clean
<<<<<<< HEAD

=======
# make необходимо установить и добавить в переменные среды
# чтоб запустить комманду необходимо в консоли набрать: make run
>>>>>>> my-changes
run:
	pyinstaller -F -w -n "Downloader" --icon=./src/data/favicon.ico src/main.py

test:
	python3 -m unittest discover -s tests

clean:
<<<<<<< HEAD
	rm -rf build Downloader.spec


=======
	rm -rf build Downloader.spec
>>>>>>> my-changes
