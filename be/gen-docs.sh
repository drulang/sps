. venv/bin/activate
cd documentation
PYTHONPATH=..:../lib make clean 
PYTHONPATH=..:../lib make html
