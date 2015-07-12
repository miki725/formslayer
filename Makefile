lint:
	flake8 formslayer

format:
	importanize formslayer

clean-coverage:
	rm -rf .coverage

test: clean-coverage
	env PYTHONPATH=formslayer py.test -sv --cov=pdf --cov=formslayer --cov-report=term-missing

check: lint test

manage:
	env PYTHONPATH=formslayer formslayer/manage.py $(filter-out $@,$(MAKECMDGOALS))
