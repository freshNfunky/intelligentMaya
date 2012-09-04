"""
*********************
Event Monitor v 0.0.3
Info: callsup event alert when an action is made
creator: Felix Schaller - www.felixschaller.com
**********************

"""
# import maya.standalone
# maya.standalone.initialize()

from pymel.all import *

#  globals

eventID = dict()
eventRecord = []

# ------------ event collector called once after the first Idle Event
def gatherEvents(instance):
    print ("Gathered events by '"+instance+"':")
    global eventID
    global eventRecord
    
#    get the Id for the key
    inverseID=dict(zip(eventID.values(),eventID.keys()))
    for Id in eventRecord:
        print " ID %4d Event: %s" % (Id, inverseID.get(Id,0))
    
#    reset
    eventRecord = []
    eventID["idle"] = 0
    
    
# ------------ little helper proc who helps to record events 
def eventCallup(event, message):
    global eventID
    if eventID.get(event, 0):
        # print "Event: %30s ID: %4d " % (event, eventID.get(event))
        global eventRecord
        eventRecord.append(eventID.get(event))
    
#    install Event gather at the next idle event 
    if not eventID.get('idle'): eventID["idle"] = scriptJob(ro=True, ie=("gatherEvents('"+message+"')"))
    
# ------------ install event monitoring
def monitorEvents(instance):

	# check the right use of this Function
	panelName = instance.split('|')[-1]
	if scriptedPanel( panelName, ex=True,):
		control = scriptedPanel (panelName, q=True, control=True)
		print "Panel Name: %s" % control
		setParent (control) 
		parent = str(setParent (upLevel=True))
		print "Parent Name: %s" % parent
		if not parent: return 
	else: 
		print "instance does not exist: %s" % instance
		return 

     
#    list maya events
	scriptJobs = scriptJob(listEvents=True)
	jobIdList = []
    
	for job in scriptJobs:
#    create alerts for all events except the "idle*" events
		if "idle" not in job:
            
			jobId = scriptJob(p=parent, e=[job, "eventCallup('" + str(job) + "','"+instance+"')"])
			jobIdList.append(jobId)

		else: 
			jobIdList.append(0)
    
#    assign events as keys with id's    
#    load global eventID
	global eventID    
	eventID = dict(zip(scriptJobs,jobIdList))
	for (key,value) in eventID.iteritems():
		print "Key: %30s Value: %d" % (key, value)
		#print "Key:  " + str(key) + "  Value:" + str(value)

# ------------ Main STARTUP Function 
def iMayaUI():
    
#  define UI Element Names    
	panelType = 'iMayaScriptedPanelType'
	panelName = 'iMayaScriptedPanel'
	winName = 'iMayaUIWin'
	panelWrapName = 'frm'
    
#  define scripted Panel if it doesn't exist
#
	if not scriptedPanelType(panelType, ex=True):
		scriptedPanelType( panelType, \
                            ccb='iMayaCreateCallback', \
                            icb='iMayaInitCallback', \
                            acb='iMayaAddCallback', \
                            rcb='iMayaRemoveCallback', \
                            dcb='iMayaDeleteCallback', \
                            scb='iMayaSaveStateCallback', \
                            unique=True )
		print "##### Panel TYPE Created"


#  create an unparented scripted panel, place it
#  in one window, 
#
#  Create unparented scripted panel
#
	if not scriptedPanel(panelName, ex=True):
		wPanel = scriptedPanel(  panelName, unParent=True, type='iMayaScriptedPanelType', label='iMaya' )
		print "##### Panel Name Created %s" % wPanel
#  --- yet no check implemented where Proc checks false panel assignment 
		
		
#    Create a couple of windows and parent the scripted panel to the first.
#
	wName = window( winName, t='iMayaUI Window' )
	wFrame = frameLayout( panelWrapName, l='iMayaUIPanel',lv=True, bv=True )
	panelParent = (winName+'|'+panelWrapName)
	scriptedPanel( panelName, e=True, parent=panelParent )
	panelUIpath = scriptedPanel( panelName, q=True, control=True )
	showWindow()
    
#    create Events watching
	monitorEvents(panelUIpath)


iMayaUI()
