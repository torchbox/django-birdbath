.PHONY: publish

publish:
	pip install twine wheel
	python setup.py sdist bdist_wheel
	twine check dist/*
	twine upload --repository pypi dist/*