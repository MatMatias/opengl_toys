SHELL := /bin/bash

setup: requirements.txt
	pip install -r requirements.txt

run_dice:
	python ./dice/dice.py

run_globe:
	python ./globe/globe.py

run_prism:
	python ./prism/prism.py

run_paraboloid:
	python ./paraboloid/paraboloid.py

run_sphere:
	cd ./sphere && python SphereApp.py

clean:
	rm -rf __pycache__
