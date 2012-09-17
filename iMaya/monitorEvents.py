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
import panelWindow 
reload (panelWindow)
import string

class EventMonitor( object ):
    
    #  Class globals
    eventID = dict()
    eventRecord = []
    RecStatus = False
    _UIobject = None
    _FuncFrame = 'FuncPanel'
    _recButton = ''
    _playButton = ''
    _optionInspectWidth = 300
    _optionInspectHeight = 100
    _optionFuncHeight = 80
    _optionMarginWidth = 2
    
    # ------------
    def __init__(self, instance, windowObj, namespace=__name__):
        """install event monitoring"""
        
        self._UIobject = windowObj
        self._module = namespace
        self.__name__ = instance
        self._instance = str(self._module) + '.' + self.__name__
        
        if windowObj is None:
            print "UI Element does not exist: %s" % UIpath
            return 
        else: 
            if not mel.scriptedPanel (windowObj.__name__, exists=True):
                return
            
            control = mel.scriptedPanel (windowObj.__name__, q=True, control=True)
            print "Panel Name: %s" % control
            mel.setParent (control) 
            parent = str(mel.setParent (upLevel=True))
    
         
    #    list maya events
        scriptJobs = mel.scriptJob(listEvents=True)
        jobIdList = []
        
        for job in scriptJobs:
    #    create alerts for all events except the "idle*" events
            if "idle" not in job:
                
                jobId = mel.scriptJob(p=parent, e=[job, "%s._eventCallup('%s','%s')" 
                                                   % (self._instance, str(job), windowObj.__name__)])
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
        
        message = "Gathered events by '%s':\n" % instance
            
    #    get the Id for the key
        inverseID=dict(zip(self.eventID.values(),self.eventID.keys()))
    
    #    prompt Result
        for Id in self.eventRecord:
            token = str(" ID %4d Event: %s \n" % (Id, inverseID.get(Id,0)))
            message = message + token
               
    #    --------------create new UI entry---------------
        objUI = self._UIobject.createTextfieldObj(message, "eventID: %s" % inverseID.get(self.eventRecord[0],0),True)
        mel.setParent(objUI)
        
        mel.frameLayout(mw=self._optionMarginWidth,l = 'Command Inspect', collapse = True, collapsable = True) 
        mel.columnLayout('subCol',adj=True)
        mel.separator(h=self._optionMarginWidth,style="none")
        mel.scrollField(numberOfLines=3, editable=False, 
                        wordWrap=False, h = self._optionInspectHeight, w = self._optionInspectWidth, text = "place Holder"  )
        mel.separator(h=self._optionMarginWidth,style="none")
        
        
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
    def _buttonRecord (self, UIpath):
        print "REC pressed: %s" % UIpath 
        if self.RecStatus:
            self.RecStatus = False
            label = "RECORD"
        else:
            self.RecStatus = True
            label = "RECORDING"
        mel.button(self._recButton, edit=True, l=label)    
            
        return
    
    # ------------
    def _buttonPlay (self, UIpath):
        print "PLAY pressed: %s" % UIpath        
        return
    
    # ------------
    def createFunctions(self, windowObj):
        
        if windowObj is None:
            print "UI Element does not exist: %s" % UIpath
            return 
        else:
            mel.setParent(windowObj._wName)
            mel.columnLayout('funcCol',adj=False,height=self._optionFuncHeight)
            self._FuncFrame = mel.frameLayout( self._FuncFrame, l='Function Frame' ,lv=True, bv=True )
            mel.columnLayout('fileCol',adj=True)
            mel.rowColumnLayout( 'funcRowColumn', numberOfColumns=2)
            self._recButton = mel.button( label="RECORD", command = mel.Callback( self._buttonRecord, self._FuncFrame ) )
            self._playButton = mel.button( label="EXECUTE", command = mel.Callback( self._buttonPlay, self._FuncFrame ) )
            mel.setParent('..') 
            mel.columnLayout('fileCol',adj=True)
            mel.textFieldButtonGrp( label='File Name:', fileName='Path/file.txt', buttonLabel='Import/Export' )  
     

# ------------  
def iMayaUI():
    """Main STARTUP Function"""
    
    panelObj = panelWindow.openTestPanel()
    
#    create Events watching
    global monitorEvents
    monitorEvents=EventMonitor( 'monitorEvents', panelObj )
    monitorEvents.createFunctions(panelObj) 
    
    return monitorEvents



