>>> import pymel.tools.mel2py as mel2py
>>> print mel2py.mel2pyStr('paneLayout -e -configuration "top3" test;')
from pymel import *
paneLayout('test',configuration="top3",e=1)
<BLANKLINE>