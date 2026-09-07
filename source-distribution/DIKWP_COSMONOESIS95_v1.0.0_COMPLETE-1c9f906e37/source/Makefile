.PHONY: doctor test demo verify wheel clean

doctor:
	python run.py doctor

test:
	PYTHONPATH=src python -m unittest discover -s tests -v

demo:
	python run.py demo --out outputs/cosmonoesis_demo

verify:
	python run.py verify outputs/cosmonoesis_demo

wheel:
	python -m pip wheel . --no-deps -w dist

clean:
	rm -rf build *.egg-info src/*.egg-info dist/*.whl
