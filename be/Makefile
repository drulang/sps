env:
	sudo easy_install pip && \
	pip install virtualenv && \
	virtualenv venv && \
	. venv/bin/activate && \
	make deps

deps:
	pip install -r requirements.txt

test:
	cd integration-tests && ./run_tests

doc:
	./gen-docs.sh

spsdb:
	sh ./db/install_db.sh

devdata:
	sh ./db/devdata_db.sh

start:
	./startdev.sh

