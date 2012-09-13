
import pymel.core 
import string 
import os,sys

print os.getcwd()

if not os.getcwd() in sys.path:
    sys.path.append(os.getcwd())

import monitorEvents
reload(monitorEvents)

print monitorEvents.iMayaUI()