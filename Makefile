docs:
	python setup.py upload_docs --upload-dir docs/_build/html

upload:
	make clean
	python3 setup.py sdist bdist_wheel && twine upload dist/*

clean:
	python setup.py clean --all
	pyclean .
	rm -rf *.pyc __pycache__ build dist lumixmaptool.egg-info lumixmaptool/__pycache__ tests/__pycache__ tests/reports docs/build

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
