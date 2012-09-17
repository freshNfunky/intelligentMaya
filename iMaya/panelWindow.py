import pymel.core as mel


class PanelWindow( object ):

#------------------------------------------------------------------------    
    gSampleState = []
        
    _wName = ''
    _optionShowMenue = 1
    _scrollField = 'scrollField'
    _rowColumn = 'rowColumn'
    _ActionCol = ''
    _VariablesCol = ''
    windowTitle = 'iMayaUi Window'
    panelLabel = 'SamplePanel'
    panelWrapName = 'frm'
#------------------------------------------------------------------------    
    def __init__( self, name, title, namespace=__name__ ):
        
        # print "self instanceName: %s " % self.__class__.__name__
        self.__name__ = name
        self._title = title

        self.instance = str(namespace) + '.' + self.__name__
        
        if not mel.scriptedPanelType( self.__name__, query=True, exists=True ):
            mel.scriptedPanelType( self.__name__, unique=True )
        print self.instance 
        
        # convert into Python one day:
        jobCmd = '%s._setup()' % self.instance
        job = mel.scriptJob(replacePrevious=True, parent=self.__name__, event=["SceneOpened",jobCmd])
        # mel.mel.eval(job)

        result = mel.scriptedPanelType( self.__name__, edit=True,
                           unique=True,
                           createCallback='python("import %s ; %s._createCallback()")' %  (namespace, self.instance),
                           initCallback='python("import %s ; %s._initCallback()"  )' % (namespace, self.instance),
                           addCallback='python("import %s ; %s._addCallback()"   )' %  (namespace, self.instance),
                           removeCallback='python("import %s ; %s._removeCallback()")' % (namespace, self.instance),
                           deleteCallback='python("import %s ; %s._deleteCallback()")' % (namespace, self.instance),
                           saveStateCallback='python("import %s ; %s._saveCallback()")' % (namespace, self.instance)
                           )
        print "RESULT: %s " % result
#------------------------------------------------------------------------
    def _setup(self):
        """Command to be call for new scene"""
        print 'SETUP CALLED'
        gMainPane = mel.mel.eval( 'global string $gMainPane; $temp = $gMainPane;' )
        mel.sceneUIReplacement( update=gMainPane )
        panelName = mel.sceneUIReplacement( getNextScriptedPanel=(self.__name__, self._title) )
        
        # print "-->Panel Name: %s" % panelName
        
        if panelName == '':
            try:
                panelName = mel.scriptedPanel(self.__name__, mbv=self._optionShowMenue, unParent=True, type=self.__name__, label=self._title )
                mel.scriptedPanel( panelName, e=True, parent=self.panelParent)
                print "sceneUIreplacement has FAILED finding something - however: %s" % panelName
            except:
                pass
        else:
            try:
                pLabel = panel( self.__name__, query=True, label=True )
                panelName = mel.scriptedPanel( self.__name__, edit=True,  label=pLabel )
                mel.scriptedPanel( panelName, e=True, parent=self.panelParent)
                print "sceneUIreplacement has found something: %s" % pLabel
            except:
                pass

#------------------------------------------------------------------------
    def _createCallback(self):
        """Create any editors unparented here and do any other initialization required."""
        print 'CREATE CALLBACK'
        self.gSampleState = {'fsg1':0, 'fsg2':1, 'fsg3':3, 'rbg':1, 'rbg1':2}

#------------------------------------------------------------------------
    def _initCallback(self):
        """Re-initialize the panel on file -new or file -open."""
        print 'INIT CALLBACK'
        # needs to be filled out when more advanced with save, new, open etc.

#------------------------------------------------------------------------
    def _addCallback(self):
        """Create UI and parent any editors."""
        print 'ADD CALLBACK'
        #
        #  Description:  Create UI and parent any editors.
        #
        if not self.gSampleState.__len__() : 
            self._createCallback()
            print "---->gSampleState was Empty"
            
            
        # restore content from database
        # self._scrollField =
         
        mel.scrollLayout(self._scrollField, horizontalScrollBarThickness=16, 
                           verticalScrollBarThickness=16)
        
        # mel.columnLayout('topCol',adj=True)
        mel.rowColumnLayout( self._rowColumn, numberOfColumns=2 )
        self._ActionCol = mel.columnLayout('ActionCol',adj=True)
        mel.setParent('..')
        self._VariablesCol = mel.columnLayout('VariablesCol',adj=True)
        # print "scrollLayout UI path: %s" % self._scrollField 
                         
       
       
#------------------------------------------------------------------------
    def _removeCallback(self):
        """Unparent any editors and save state if required."""
        if not mel.scriptedPanel(self.__name__, ex=1):
            return                                  # no common call 
        print 'REMOVE CALLBACK: %s' % self.__name__
        
        # control=str(mel.scriptedPanel(self.__name__,
        #                           q=1,control=1))
        mel.setParent(self._ActionCol)
        #------------------------------- testmodule
        self.gSampleState['fsg1']=float(floatSliderGrp('fsg1',q=1,v=1))
        self.gSampleState['fsg2']=float(floatSliderGrp('fsg2',q=1,v=1))
        self.gSampleState['fsg3']=float(floatSliderGrp('fsg3',q=1,v=1))
        self.gSampleState['rbg']=float(radioButtonGrp('rbg',q=1,sl=1))
        self.gSampleState['rbg1']=float(radioButtonGrp('rbg2',q=1,sl=1))
        #------------------------------- testmodule
#------------------------------------------------------------------------
    def _deleteCallback(self):
        """Delete any editors and do any other cleanup required."""
        print 'DELETE CALLBACK'

#------------------------------------------------------------------------
    def _saveCallback(self):
        """Save Callback."""
        print 'SAVE CALLBACK'
        indent="\n\t\t\t"
        reCreateCommand = 'python("print \\"RECREATE COMMAND %s\\" % '+ self.instance + ' ")' 
        print "prepared recreate Command: %s" % reCreateCommand
        return reCreateCommand
        
#------------------------------------------------------------------------
    def show( self ):
        #mel.scriptedPanel( self._title, edit=True, tearOff=True )
        print "SHOW PANEL"
        # print "self?: %s" % self.__name__
        if not mel.window(self._wName, exists=True ):          
            print "fenster existiert nicht: %s" % self._wName
            try: 
                wPanel = mel.scriptedPanel(  self.__name__, mbv=self._optionShowMenue, unParent=True, type=self.__name__, label=self._title )
            except:
                pLabel = mel.panel( self.__name__, query=True, label=True )
                wPanel = mel.scriptedPanel( self.__name__, edit=True,  label=pLabel )
            
            self._wName = mel.window( self._title, t=self.windowTitle )
        
            wFrame = mel.frameLayout( self.panelWrapName, l=self.panelLabel ,lv=True, bv=True ) ## get external definitions
            # print "Frame Name %s" % wFrame
            #panelParent = (wName+'|'+wFrame)
            self.panelParent = wFrame
            mel.scriptedPanel( wPanel, e=True, parent=self.panelParent)
            self.panelUIpath = mel.scriptedPanel( self.__name__, q=True, control=True )
            
        mel.showWindow(self._wName)

#------------------------------------------------------------------------
    def createSliderObj( self ):
        """ creates a Slider Element """
        
        # control=str(mel.scriptedPanel(self.__name__,
        #                          q=1,control=1))
        # mel.setParent(control)
        # mel.setParent(self.panelUIpath)
        if mel.scrollLayout(self._scrollField, ex=True):
            
            # mel.setParent(control+'|'+self._scrollField+'|'+self._rowColumn)
            mel.setParent( self._ActionCol)
                       
            mel.separator(h=10,style="none")
            ObjUIpath = mel.frameLayout(mw=10,l="Sliders")
            mel.columnLayout('sampleCol',adj=True)
            mel.separator(h=10,style="none")
            
            mel.floatSliderGrp('fsg1',v=self.gSampleState['fsg1'],
                l="Property A",f=True)
            mel.floatSliderGrp('fsg2',v=self.gSampleState['fsg2'],
                l="Property B",f=True)
            mel.floatSliderGrp('fsg3',v=self.gSampleState['fsg3'],
                l="Property C",f=True)
            
            mel.separator(h=10,style="none")
            # mel.setParent('..')
            # mel.setParent('..')
            
            
            return ObjUIpath
        
#------------------------------------------------------------------------        
    def createRadioBtnObj( self ):
        """ creates a RadioButton Element """    
        
        if mel.scrollLayout(self._scrollField, ex=True):
            
            mel.setParent( self._ActionCol)
            
            mel.separator(h=10,style="none")    
                         
            ObjUIpath = mel.frameLayout(mw=10,l="Radio Buttons")
            mel.columnLayout('sampleCol')
            mel.separator(h=10,style="none")
            
            mel.radioButtonGrp('rbg',nrb=3,
                l="Big Options",
                select=self.gSampleState['rbg'],
                la3=("Option 1", "Option 2", "Option 3"))
            mel.radioButtonGrp('rbg2',nrb=3,
                l="Little Options",
                select=self.gSampleState['rbg'],
                la3=("Option 4", "Option 5", "Option 6"))
            
            mel.separator(h=10,style="none")
            
            return ObjUIpath

#------------------------------------------------------------------------        
    def createTextfieldObj( self , content):
        """ creates a TextBox Element """
                        
        if mel.scrollLayout(self._scrollField, ex=True):
            
            mel.setParent( self._ActionCol)
            
            mel.separator(h=10,style="none")
                             
            ObjUIpath = mel.frameLayout(mw=10,l="TextField")
            mel.columnLayout('sampleCol',adj=True)
            mel.separator(h=10,style="none")
                    
            mel.scrollField(numberOfLines=3, editable=False, 
                            wordWrap=False, h=100, text = content )
            
            mel.separator(h=10,style="none")
                        
            return ObjUIpath
        
#------------------------------------------------------------------------        
    def createVariableObj( self , name):
        """ creates a TextBox Element """
        
        if mel.scrollLayout(self._scrollField, ex=True):
            
            mel.setParent( self._VariablesCol )
            
            ObjUIpath = mel.button(label="button %s" % name)
            
            return ObjUIpath
            

def openTestPanel():
    
    # global testPanel
    global PanelObj                                             #PanelObj must be a global variable to make the CallbackFunktions work
    
    PanelObj = PanelWindow( 'PanelObj','Panel Obj Window' ) 
    PanelObj.show()
    
    return PanelObj