$env:PYTHONPATH="src"
pylint $(git ls-files '*.py')
