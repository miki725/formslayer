lint:
	flake8 formslayer

test:
	env PYTHONPATH=formslayer py.test -v --cov=pdf --cov=formslayer --cov-report=term-missing

check: lint test

manage:
	env PYTHONPATH=formslayer formslayer/manage.py $(filter-out $@,$(MAKECMDGOALS))
