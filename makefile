SHELL := /bin/bash

setup: requirements.txt
	pip install -r requirements.txt

run_dice:
	python ./dice/dice.py

run_globe:
	python ./globe/globe.py

run_pyramid:
	python ./pyramid/pyramid.py

clean:
	rm -rf __pycache__
