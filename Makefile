env:
	python2 -m virtualenv env --prompt="[gdr]"
	pip install -r requirements.txt
	pip install pytest
	pip install -e .

clean:
	rm -rf env

run: env
	./run defaults.env local.env web
