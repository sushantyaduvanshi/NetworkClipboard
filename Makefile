install:
	@if [ "$(python3 -m pip freeze | grep -i ^virtualenv)" = '' ]; \
	then \
	echo "\n Installing Virtaulenv (Python Package) for creating the virtual environment..!! \n"; \
	python3 -m pip install virtualenv; \
	fi
	@if [ "$(ls | grep ^clipboard_venv$)" = '' ]; \
	then \
	echo "\n Creating virtual environment..!! \n"; \
	virtualenv -p python3 clipboard_venv; \
	fi
	source clipboard_venv/bin/activate
	python3 -m pip install -r requirements.txt

run:
	source clipboard_venv/bin/activate
	@screen -ls &> /dev/null ; \
	if [ $$? -eq 127 ]; \
	then \
	echo "\033[0;35m\n If you want to run this programm in background, \n Then Kindly install \033[1;36m SCREEN \033[0;35m command tool in your system. \n After installation restart this program again. \n\033[0m"; \
	python3 network_clipboard_sync.py; \
	elif [ $(screen -ls | grep NetworkClipboard) = "" ]; \
	then \
	screen -S NetworkClipboard -dm python3 network_clipboard_sync.py; \
	else \
	echo "\033[0;31m\n Program in Already running in Screen..!! \n\033[0m"; \
	fi