docs:
	python setup.py upload_docs --upload-dir docs/_build/html

update:
	python setup.py sdist upload --sign
	sudo pip install lumixmaptool --upgrade

test:
	nosetests --with-coverage --cover-erase --cover-package lumixmaptool --logging-level=INFO --cover-html

testall:
	make test
	cheesecake_index -n lumixmaptool -v

count:
	cloc . --exclude-dir=docs,cover,dist,lumixmaptool.egg-info

countc:
	cloc . --exclude-dir=docs,cover,dist,lumixmaptool.egg-info,tests

countt:
	cloc tests