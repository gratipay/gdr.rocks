env:
	python2 -m virtualenv env --prompt="[gdr]"
	pip install -r requirements.txt

	# Uninstall leftovers from bandersnatch's over-eager install_requires, to
	# avoid test failures. https://bitbucket.org/pypa/bandersnatch/issues/79
	pip uninstall --yes pytest-capturelog pytest-codecheckers pytest-timeout pytest-cache

	pip install -r requirements/development.txt
	pip install -e .

clean:
	rm -rf env

run: env
	./run defaults.env local.env web
