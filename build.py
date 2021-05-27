import os
from random import choice
os.system('rm *.pyc')
os.system('rm -rf __pycache__')
os.system('git init')
os.system('git add .')
os.system('git commit -m "{}"'.format(choice(range(1000,10000))))
os.system('git push heroku master')
