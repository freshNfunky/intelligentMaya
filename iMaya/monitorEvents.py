"""
*********************
Event Monitor v 0.0.3
Info: callsup event alert when an action is made
creator: Felix Schaller - www.felixschaller.com
**********************

"""
# import maya.standalone
# maya.standalone.initialize()

import pymel.core as mel


class EventMonitor( object ):
    
    #  Class globals
    eventID = dict()
    eventRecord = []
    
    # ------------
    def __init__(self, instance, UIpath, namespace=__name__):
        """install event monitoring"""
        
        self._module = namespace
        self.__name__ = instance
        self._instance = str(self._module) + '.' + self.__name__
        
      # check the right use of this Function
        panelName = UIpath.split('|')[-1]
        if mel.scriptedPanel( panelName, ex=True,):
            control = mel.scriptedPanel (panelName, q=True, control=True)
            print "Panel Name: %s" % control
            mel.setParent (control) 
            parent = str(mel.setParent (upLevel=True))
            print "Parent Name: %s" % parent
            if not parent: return 
        else: 
            print "UI Element does not exist: %s" % UIpath
            return 
    
         
    #    list maya events
        scriptJobs = mel.scriptJob(listEvents=True)
        jobIdList = []
        
        for job in scriptJobs:
    #    create alerts for all events except the "idle*" events
            if "idle" not in job:
                
                jobId = mel.scriptJob(p=parent, e=[job, "%s._eventCallup('%s','%s')" 
                                                   % (self._instance, str(job), UIpath)])
                jobIdList.append(jobId)
    
            else: 
                jobIdList.append(0)
        
    #    assign events as keys with id's    
    #    load global eventID
            
        self.eventID = dict(zip(scriptJobs,jobIdList))
        for (key,value) in self.eventID.iteritems():
            print "Key: %30s Value: %d" % (key, value)
            #print "Key:  " + str(key) + "  Value:" + str(value)

    # ------------ 
    def _gatherEvents(self, instance):
        """event collector called once after the first Idle Event"""
        
        print ("Gathered events by '"+instance+"':")
            
    #    get the Id for the key
        inverseID=dict(zip(self.eventID.values(),self.eventID.keys()))
    
    #    prompt Result
        for Id in self.eventRecord:
            print " ID %4d Event: %s" % (Id, inverseID.get(Id,0))
        
    #    reset Event Collection
        self.eventRecord = []
        self.eventID["idle"] = 0
        
        
    # ------------  
    def _eventCallup(self, event, message):
        """little helper proc who helps to record events"""
                
        if self.eventID.get(event, 0):
            # print "Event: %30s ID: %4d " % (event, eventID.get(event))
            self.eventRecord.append(self.eventID.get(event))
        
    #    install Event gather at the next idle event 
        if not self.eventID.get('idle'): self.eventID["idle"] = mel.scriptJob(ro=True, ie=("%s._gatherEvents('%s')"
                                                                                       % (self._instance, message)))
        
 

# ------------  
def iMayaUI():
    """Main STARTUP Function"""
    
#  define UI Element Names    
    panelType = 'iMayaScriptedPanelType'
    panelName = 'iMayaScriptedPanel'
    winName = 'iMayaUIWin'
    panelWrapName = 'frm'
    
#  define scripted Panel if it doesn't exist
#
    if not mel.scriptedPanelType(panelType, ex=True):
		mel.scriptedPanelType( panelType, \
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
    if not mel.scriptedPanel(panelName, ex=True):
        wPanel = mel.scriptedPanel(  panelName, unParent=True, type='iMayaScriptedPanelType', label='iMaya' )
        print "##### Panel Name Created %s" % wPanel
#  --- yet no check implemented where Proc checks false panel assignment 
		
		
#    Create a couple of windows and parent the scripted panel to the first.
#
    wName = mel.window( winName, t='iMayaUI Window' )
    wFrame = mel.frameLayout( panelWrapName, l='iMayaUIPanel',lv=True, bv=True )
    panelParent = (winName+'|'+panelWrapName)
    mel.scriptedPanel( panelName, e=True, parent=panelParent )
    panelUIpath = mel.scriptedPanel( panelName, q=True, control=True )
    mel.showWindow()
    
#    create Events watching
    global monitorEvents
    monitorEvents=EventMonitor( 'monitorEvents', panelUIpath )
    
    return monitorEvents



